# Connecting garettloghry.com

Primary address: https://garettloghry.com. GitHub Pages continues to host the site.

Repository changes set Jekyll's canonical URL and public links. They do not change DNS or the Pages custom-domain setting. Complete the dashboard steps before treating the migration as live.

## 1. Verify domain ownership in GitHub

Open [personal account Pages settings](https://github.com/settings/pages), add `garettloghry.com`, and follow GitHub's instructions to add its TXT record at your DNS provider. For this account the record name is `_github-pages-challenge-gloghry`; use the exact name and verification value shown by GitHub. Some providers append `.garettloghry.com` automatically.

Return to GitHub and verify the domain. Keep the TXT record after verification. Account verification is separate from the repository's custom-domain field.

## 2. Set the repository's custom domain

Open [repository Settings → Pages](https://github.com/gloghry/gloghry.github.io/settings/pages). Enter `garettloghry.com` under Custom domain and save. Do this before pointing website DNS records at GitHub.

This repository publishes through a custom GitHub Actions workflow. GitHub's documentation says a source `CNAME` file is ignored for this workflow; the Pages dashboard setting is what connects the domain.

## 3. Add DNS records

In the DNS dashboard serving garettloghry.com, create these records. `@` means the root domain; some dashboards use an empty host or the full domain instead.

| Type | Host/name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | gloghry.github.io |

Use the default TTL. The CNAME target has no scheme or path. Replace conflicting parking/website records for the root and www, but preserve unrelated TXT and email records. An unrelated existing root AAAA record also needs removal or correction. Do not use registrar URL forwarding in place of these DNS records.

IPv6 is optional. If enabled, add these four `AAAA` records at `@` in addition to the A records:

```text
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

If your DNS dashboard offers proxying, use DNS-only for initial setup and certificate provisioning.

## 4. Finish HTTPS and deployment

Wait for the Pages DNS check and certificate provisioning, then enable **Enforce HTTPS** in repository Pages settings. GitHub says DNS propagation and HTTPS availability can take up to 24 hours.

Merge the domain configuration PR and confirm the Pages deployment succeeds. No additional hosting plan is needed for this public repository.

## 5. Verify the result

- https://garettloghry.com loads the site and its local fonts, CSS, and scripts.
- https://www.garettloghry.com redirects to the primary domain.
- https://gloghry.github.io redirects to the custom domain.
- Pages settings show the expected custom domain and enforced HTTPS.
- Canonical/social URLs, `/sitemap.xml`, `/feed.xml`, and the robots sitemap reference use the custom domain.

On a system with DNS tools, use `dig garettloghry.com A` and `dig www.garettloghry.com CNAME`. On Windows, use PowerShell `Resolve-DnsName garettloghry.com -Type A` and `Resolve-DnsName www.garettloghry.com -Type CNAME`.

## References

- [GitHub: manage a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub: verify domain ownership](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [GitHub: HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)

Issue #21 remains open until DNS, certificate, redirects, and live deployment are verified.
