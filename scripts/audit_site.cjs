/* Browser checks for issues #9 and #10. Runs against the generated site only. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const { spawn } = require('node:child_process');
const os = require('node:os');
const { chromium, webkit } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;

const origin = 'http://127.0.0.1:4173';
const basePath = (process.env.SITE_BASEURL || '').replace(/\/+$/, '');
const segments = basePath.split('/').filter(Boolean);
assert(basePath === '' || (basePath.startsWith('/') && segments.length > 0 &&
  segments.every(segment => /^[A-Za-z0-9._~-]+$/.test(segment) && segment !== '.' && segment !== '..')),
  'SITE_BASEURL must be empty or an absolute URL path without dot segments');
const base = origin + basePath;
const siteDirectory = path.resolve(process.env.SITE_DIRECTORY || '_site');
const output = path.resolve(process.env.AUDIT_OUTPUT_DIR || 'audit-results');
const routes = ['/', '/about/', '/projects/', '/writing/', '/404.html'];
const widths = [320, 390, 768, 1024, 1440];
const results = [];
const failures = [];
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function scenario(name, work) {
  try {
    await work();
    results.push({ name, status: 'passed' });
    console.log('PASS ' + name);
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    console.error('FAIL ' + name + ': ' + error.message);
  }
}

async function loaded(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all(Array.from(document.images, image => image.decode()));
  });
}

async function layout(page) {
  const measurements = await page.evaluate(() => {
    const root = document.documentElement;
    const targets = Array.from(document.querySelectorAll('.site-header nav a, #theme-toggle'));
    return {
      overflow: root.scrollWidth - root.clientWidth,
      targets: targets.filter(el => el.getClientRects().length).map(el => {
        const box = el.getBoundingClientRect();
        return { label: el.textContent.trim() || el.getAttribute('aria-label'),
          x: box.x, right: box.right, width: box.width, height: box.height };
      }),
      images: Array.from(document.images, image => ({
        loaded: image.complete && image.naturalWidth > 0,
        dimensions: Number(image.getAttribute('width')) > 0 && Number(image.getAttribute('height')) > 0,
        eager: image.loading !== 'lazy'
      }))
    };
  });
  assert(measurements.overflow <= 1, 'Page overflows horizontally by ' + measurements.overflow + 'px');
  for (const target of measurements.targets) {
    assert(target.x >= -1 && target.right <= page.viewportSize().width + 1, target.label + ' is outside viewport');
    assert(target.width >= 44 && target.height >= 44, target.label + ' needs a 44px touch target');
  }
  assert(measurements.images.every(image => image.loaded && image.dimensions && image.eager),
    'Portrait failed loading, lacks intrinsic dimensions, or is lazy loaded');
}

async function auditBrowser(browserType) {
  const name = browserType.name();
  const browser = await browserType.launch();
  try {
    for (const theme of ['light', 'dark']) {
      const context = await browser.newContext({ colorScheme: theme });
      const page = await context.newPage();
      page.setDefaultTimeout(15000);
      for (const route of routes) {
        for (const width of widths) {
          await scenario(name + ' ' + theme + ' ' + width + ' ' + route, async () => {
            await page.setViewportSize({ width, height: 900 });
            const response = await page.goto(base + route);
            assert.equal(response.status(), 200);
            await loaded(page);
            assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
            assert.equal(await page.locator('h1').count(), 1);
            await layout(page);
            if (width === 390) {
              const accessibility = await new AxeBuilder({ page })
                .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
              assert.deepEqual(accessibility.violations.map(v => ({
                id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target)
              })), [], 'Automated accessibility findings');
            }
            if ((width === 320 || width === 1440) && (route === '/' || route === '/about/')) {
              const slug = route === '/' ? 'home' : 'about';
              await page.screenshot({ path: path.join(output, name + '-' + theme + '-' + width + '-' + slug + '.png'), fullPage: true });
            }
            if (route === '/about/') {
              await page.evaluate(() => {
                document.querySelector('h1').textContent = 'A deliberately long technical title ' + 'unbroken'.repeat(25);
                const block = document.createElement('pre');
                block.textContent = 'long_code_identifier_'.repeat(70);
                document.querySelector('main').append(block);
              });
              await layout(page);
            }
          });
        }
      }
      await scenario(name + ' ' + theme + ' 200% text reflow', async () => {
        await page.setViewportSize({ width: 390, height: 900 });
        await page.goto(base + '/about/');
        await loaded(page);
        await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
        await layout(page);
      });
      await context.close();
    }

    await scenario(name + ' keyboard and saved theme', async () => {
      const context = await browser.newContext({ colorScheme: 'light', viewport: { width: 390, height: 900 } });
      try {
        const page = await context.newPage();
        await page.goto(base);
        await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(() => document.activeElement.className), 'skip-link');
        const focus = await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle);
        assert.notEqual(focus, 'none');
        await page.keyboard.press('Enter');
        assert.equal(await page.evaluate(() => document.activeElement.id), 'main');
        const button = page.getByRole('button', { name: 'Switch to dark mode', exact: true });
        await button.focus();
        await page.keyboard.press('Enter');
        await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
        assert.equal(await page.evaluate(() => localStorage.getItem('theme')), 'dark');
        await page.reload();
        await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
        assert(await page.locator('.theme-icon-sun').isVisible());
        assert(!(await page.locator('.theme-icon-moon').isVisible()));
        await page.getByRole('button', { name: 'Switch to light mode', exact: true }).click();
        assert(await page.locator('.theme-icon-moon').isVisible());
        await page.getByRole('link', { name: 'Projects', exact: true }).click();
        await page.waitForURL(base + '/projects/');
        assert.equal(await page.getByRole('link', { name: 'Projects', exact: true }).getAttribute('aria-current'), 'page');
      } finally { await context.close(); }
    });

    await scenario(name + ' system changes and unavailable storage', async () => {
      const context = await browser.newContext({ colorScheme: 'light' });
      try {
        await context.addInitScript(() => Object.defineProperty(window, 'localStorage', {
          get() { throw new Error('Storage unavailable'); }
        }));
        const page = await context.newPage();
        await page.goto(base);
        await page.emulateMedia({ colorScheme: 'dark' });
        await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
        await page.getByRole('button', { name: 'Switch to light mode', exact: true }).click();
        await page.waitForFunction(() => document.documentElement.dataset.theme === 'light');
        await page.emulateMedia({ colorScheme: 'light' });
        await page.emulateMedia({ colorScheme: 'dark' });
        assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
      } finally { await context.close(); }
    });

    for (const theme of ['light', 'dark']) {
      await scenario(name + ' no JavaScript ' + theme, async () => {
        const context = await browser.newContext({ javaScriptEnabled: false, colorScheme: theme, viewport: { width: 320, height: 900 } });
        try {
          const page = await context.newPage();
          assert.equal((await page.goto(base + '/about/')).status(), 200);
          assert(!(await page.locator('#theme-toggle').isVisible()));
          assert(await page.getByRole('link', { name: 'Projects', exact: true }).isVisible());
          await layout(page);
        } finally { await context.close(); }
      });
    }
  } finally { await browser.close(); }
}

async function main() {
  await fs.mkdir(output, { recursive: true });
  let temporaryRoot;
  let server;
  try {
    // baseurl changes emitted URLs, not Jekyll's destination directory.
    // Mount that directory at the matching URL prefix for browser requests.
    let serveDirectory = siteDirectory;
    if (basePath) {
      temporaryRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'site-browser-audit-'));
      serveDirectory = temporaryRoot;
      const mount = path.join(temporaryRoot, ...segments);
      await fs.mkdir(path.dirname(mount), { recursive: true });
      await fs.symlink(siteDirectory, mount, 'dir');
    }
    server = spawn('python3', ['-m', 'http.server', '4173', '--bind', '127.0.0.1',
      '--directory', serveDirectory], { stdio: 'ignore' });
    let ready = false;
    for (let attempt = 0; attempt < 40; attempt++) {
      try { ready = (await fetch(base + '/')).ok; } catch (_) {}
      if (ready) break;
      await delay(250);
    }
    assert(ready, 'Generated-site server did not start at ' + base + '/');
    for (const browser of [chromium, webkit]) await auditBrowser(browser);
  } finally {
    if (server) server.kill();
    if (temporaryRoot) await fs.rm(temporaryRoot, { recursive: true, force: true });
    await fs.writeFile(path.join(output, 'report.json'),
      JSON.stringify({ basePath, passed: results.length, failures, results }, null, 2));
  }
  if (failures.length) throw new Error(failures.length + ' browser audit scenario(s) failed; see ' + output);
  console.log(results.length + ' browser audit scenarios passed at ' + (basePath || '/') + '.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
