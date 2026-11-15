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

- Use GitHub's standard issue types `Bug`, `Feature`, and `Task`; issue types are separate from the PR change-type labels below. Use the configured issue fields `Priority`, `Effort`, `Start date`, and `Target date` when available. Record effort and dates only when established; do not invent estimates or deadlines.
- Set one priority per issue, preferring the configured Priority field. If unavailable through the current account or tool, use exactly one existing priority label. If neither can be set, use a Priority section in the body with a brief rationale (`## Priority` for API-created issues; `### Priority` from issue forms is accepted). Report unavailable fields/types and the setup or permissions needed; do not claim a label or form answer sets a native field.
- Keep field, label, and body values consistent when more than one is present. Read the native Priority field first, then the priority label, then the body fallback. If any explicit values conflict, resolve the discrepancy before starting or labeling a PR; do not silently overwrite an owner decision. Preserve existing P0–P3 priorities using this equivalent mapping:

| Priority field | Existing label | Use for |
| --- | --- | --- |
| Urgent | `priority:P0` | Release/promotion blockers and problems preventing basic use, including foundational usability/accessibility |
| High | `priority:P1` | Near-term functionality, professional content, discovery, documentation, or workflow improvements |
| Medium | `priority:P2` | Follow-up polish, secondary content/improvements, or organization |
| Low | `priority:P3` | Optional exploration |

- Before starting, confirm priority, scope, dependencies, and missing inputs. Choose the highest-priority actionable work or unblock its prerequisite. Priority is separate from effort and readiness; it does not imply user input is required.
- Preserve explicit priorities unless Garett authorizes reprioritization; record the rationale for deliberate changes. Do not rewrite completed issues' historical priorities.
- When triaging, audit all open issues for missing or ambiguous priority values across fields, labels, and fallback bodies. API-created issues need their own metadata assignment; issue-form dropdowns do not validate API requests. Do not rewrite completed issues' historical priorities or bulk-migrate metadata without an explicit request.

## Pull request labels

- Apply exactly one change-type label and one priority label when opening or updating a PR; follow the catalog and examples in [CONTRIBUTING.md](CONTRIBUTING.md#pull-request-labels).
- Mirror the linked issue's resolved priority using the mapping above, choosing the highest priority for multiple issues (Urgent/P0 first). Resolve missing or ambiguous priorities rather than guessing. Recheck labels when scope changes and remove stale type/priority labels.
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
