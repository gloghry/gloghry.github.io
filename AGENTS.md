# Repository instructions

## GitHub workflow

- The default branch is `main`; preserve its protection and required PR/check rules. Do not rename the branch or change protection as routine setup.
- Every repository change must be associated with a GitHub issue, including code, documentation, configuration, copy, maintenance, and agent-rule changes.
- Before editing, find an existing issue that covers the work or create one. Do not create duplicate issues for follow-up fixes within the same scope.
- Start from the latest default branch and create or switch to a dedicated issue branch before making changes. Prefer `<issue-number>-<short-description>`.
- Keep unrelated work in separate branches and pull requests. Preserve uncommitted work belonging to other tasks.
- Every PR description must reference at least one existing issue. Use `Closes #N` only when the PR completes its scope and targets the default branch; otherwise use `Related to #N` and state what remains. A non-closing reference satisfies the requirement for partial work.
- Check review feedback and CI before reporting a change as ready. Report any verification that could not run.

## Issue priorities

- Use GitHub's standard issue types `Bug`, `Feature`, and `Task`; issue types are separate from the PR change-type labels below. Fill the native `Priority` and `Effort` fields. Estimate effort from scope, separately from priority: Low for focused edits, Medium for bounded features or substantial writing, High for larger work or unresolved integrations. Identify estimates as provisional and revise when scope becomes clearer.
- Set `Start date` when work actually begins, using established history for existing work. Leave unstarted work undated; do not substitute the issue creation date unless it marks the start of work. Garett does not require an end/Target date; leave that field unchanged unless explicitly requested.
- Set exactly one priority in the native Priority field on each issue. Priority labels are retired: do not create, apply, or recreate them. If a tool cannot read or set fields, use another authorized tool; otherwise report the limitation and record a temporary Priority section in the body with a brief rationale (`## Priority` for API-created issues; `### Priority` from issue forms is accepted). A body fallback is not a native field assignment; reconcile it when field access is available.
- The native Priority field is the source of truth. Resolve conflicting explicit body values before starting; do not silently overwrite an owner decision. Historical P0–P3 body values remain valid context, using this mapping:

| Priority field | Historical equivalent | Use for |
| --- | --- | --- |
| Urgent | P0 | Release/promotion blockers and problems preventing basic use, including foundational usability/accessibility |
| High | P1 | Near-term functionality, professional content, discovery, documentation, or workflow improvements |
| Medium | P2 | Follow-up polish, secondary content/improvements, or organization |
| Low | P3 | Optional exploration |

- Before starting, confirm priority, scope, dependencies, and missing inputs. Choose the highest-priority actionable work or unblock its prerequisite. Priority is separate from effort and readiness; it does not imply user input is required.
- Preserve explicit priorities unless Garett authorizes reprioritization; record the rationale for deliberate changes. Do not rewrite completed issues' historical priorities.
- When triaging, audit all open issues for missing or ambiguous native priorities and conflicting fallback bodies. API-created issues need their own metadata assignment; issue-form dropdowns do not validate API requests. Do not rewrite completed issues' historical priorities or bulk-migrate metadata without an explicit request.

## Pull request labels

- Apply exactly one change-type label when opening or updating a PR; follow the catalog and examples in [CONTRIBUTING.md](CONTRIBUTING.md#pull-request-labels). Preserve relevant area labels such as accessibility. Do not apply priority labels.
- Set the PR's native Priority field from its linked issue, choosing the highest priority for multiple issues (Urgent first). Resolve missing or ambiguous priorities rather than guessing. Recheck fields and change-type labels when scope changes; preserve unrelated field values.
- Verify applied labels. If a label is unavailable or setup cannot run, report that limitation and the setup step; do not claim completion. Preserve the attribution footer independently of labels.

## Pull request attribution

- Every PR created or substantially implemented by Codex must include a concise **AI assistance:** footer describing its actual contribution. When verified, use: **AI assistance:** Implemented with OpenAI Codex `<verified version>`; opened through Garett’s connected GitHub account. Adapt the wording for review or drafting work and identify the authenticated account only when verified.
- Include verified model names inline when available and relevant. Omit unavailable metadata, unknown-field placeholders, and metadata tables. Never guess versions/models or apply today's metadata to earlier work without evidence.
- Preserve credit for Garett's supplied writing, palette, designs, and decisions. Adapt the contribution wording when needed; GitHub's author remains the authenticated account.
- Add the footer when opening the PR and retain it when updating the description.

## Copy and content

- Use Garett's supplied and approved drafts as the baseline. Make focused edits instead of replacing his voice with generic portfolio or résumé language.
- Keep current work, technical experience, leadership experience, and education status accurate. Ask about missing personal details rather than inventing them.
- Do not publish private workplace incidents or infer permission to publish contact details from source material.
- Keep credentials, private records, email headers, and unapproved personal details out of public issues, PRs, logs, and artifacts. Review the exact staged diff and final output before publishing an export derived from private inputs. Public contact is `contact@garettloghry.com` and Garett's approved LinkedIn profile; private forwarding addresses are not public contact details.
- Preserve the approved Atkinson Hyperlegible Next font, slate/teal palette, and copy unless the scoped issue and owner review authorize a change.

## Permissions and publishing

- Change repository visibility, app permissions, collaborator access, or publishing credentials only with explicit authorization. Keep private inputs and credentials out of public workflows and PR validation jobs.
- Production is GitHub Pages at `https://garettloghry.com`; Cloudflare Pages is for PR previews. Do not change DNS or deployment settings without an explicit request. Do not merge PRs or publish unapproved personal content.
- Drafts and docs are excluded from site output, but source in this public repository is still public. Keep work-in-progress article content on its issue branch until approved.

## Jekyll base paths

- Honor `baseurl`/`SITE_BASEURL` in tooling, previews, navigation, and asset URLs. Use Jekyll's `relative_url` filter for site-relative template links.
- Jekyll writes files directly beneath its destination; a public URL prefix such as `/portfolio` is not an extra output directory. A preview/audit server must mount that destination at the matching URL prefix, and browser URLs must use the same prefix.
- When changing build, serving, link-checking, or preview infrastructure, verify both the domain root and a nonempty subpath. Keep build, server, and checker settings synchronized; never assume the site is always served at `/`.
- Use the existing link-checker regression tests and CI's configured/alternate browser audits; see [audit commands](docs/accessibility.md). Keep alternate test output separate from the production artifact.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, checks, publication, and content authoring. Run checks appropriate to the change; do not add tests merely to mirror prose edits. For prose-only work, review relevant documentation links and rendered output when it matters.
