# Repository instructions

## Issue-based workflow

- Every repository change must be associated with a GitHub issue, including documentation, configuration, copy, maintenance, and agent-rule changes.
- Before editing, find an existing issue that covers the work or create one. Do not create duplicate issues for follow-up fixes within the same scope.
- Start from the latest default branch and create or switch to a dedicated issue branch before making changes. Prefer `<issue-number>-<short-description>`.
- Keep unrelated work in separate branches and pull requests. Preserve uncommitted work belonging to other tasks.
- Reference the issue in the pull request. Use `Closes #N` only when the change completes its scope; otherwise use `Related to #N` and state what remains.
- Check review feedback and CI before reporting a change as ready. Report any verification that could not run.

## Pull request attribution

- Every PR created or substantially implemented by Codex must include a concise footer: **AI assistance:** Implemented with OpenAI Codex `<verified version>`; opened through Garett’s connected GitHub account.
- Include verified model names inline when available and relevant. Omit unavailable metadata, unknown-field placeholders, and metadata tables. Never guess versions/models or apply today's metadata to earlier work without evidence.
- Preserve credit for Garett's supplied writing, palette, designs, and decisions. Adapt the contribution wording when needed; GitHub's author remains the authenticated account.
- Add the footer when opening the PR and retain it when updating the description.

## Copy and content

- Use Garett's supplied and approved drafts as the baseline. Make focused edits instead of replacing his voice with generic portfolio or résumé language.
- Keep current work, technical experience, leadership experience, and education status accurate. Ask about missing personal details rather than inventing them.
- Do not publish private workplace incidents or infer permission to publish contact details from source material.

## Jekyll base paths

- Honor `baseurl`/`SITE_BASEURL` in tooling, previews, navigation, and asset URLs. Use Jekyll's `relative_url` filter for site-relative template links.
- Jekyll writes files directly beneath its destination; a public URL prefix such as `/portfolio` is not an extra output directory. A preview/audit server must mount that destination at the matching URL prefix, and browser URLs must use the same prefix.
- When changing build, serving, link-checking, or preview infrastructure, verify both the domain root and a nonempty subpath. Keep build, server, and checker settings synchronized; never assume the site is always served at `/`.
- Use the existing link-checker regression tests and CI's configured/alternate browser audits; see [audit commands](docs/accessibility.md). Keep alternate test output separate from the production artifact.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, checks, publication, and content authoring. Run checks appropriate to the change; do not add tests merely to mirror prose edits.
