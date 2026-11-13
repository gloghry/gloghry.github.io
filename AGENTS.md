# Repository instructions

## Issue-based workflow

- Every repository change must be associated with a GitHub issue, including documentation, configuration, copy, maintenance, and agent-rule changes.
- Before editing, find an existing issue that covers the work or create one. Do not create duplicate issues for follow-up fixes within the same scope.
- Start from the latest default branch and create or switch to a dedicated issue branch before making changes. Prefer `<issue-number>-<short-description>`.
- Keep unrelated work in separate branches and pull requests. Preserve uncommitted work belonging to other tasks.
- Reference the issue in the pull request. Use `Closes #N` only when the change completes its scope; otherwise use `Related to #N` and state what remains.
- Check review feedback and CI before reporting a change as ready. Report any verification that could not run.

## Issue priorities

- Every issue must have exactly one P0/P1/P2/P3 value in a Priority section and a brief rationale. For API-created issues use `## Priority`; accept GitHub issue forms' generated `### Priority` heading too. The body is the source of truth; labels may mirror it.
- P0: highest priority, including foundational usability/accessibility or release/promotion blockers. P1: near-term functionality, professional content, discovery, or workflow improvements. P2: follow-up polish, secondary content, or organization. P3: optional exploration.
- Before starting, confirm priority, scope, dependencies, and missing inputs. Choose the highest-priority actionable work or unblock its prerequisite. Priority is separate from effort and readiness; it does not imply user input is required.
- Preserve explicit priorities unless Garett authorizes reprioritization; record the rationale for deliberate changes. Do not rewrite completed issues' historical priorities.
- When triaging, audit all open issues for missing or ambiguous priority values. Agents creating issues through the API must supply the field themselves; the web form does not validate API requests.

## Pull request attribution

- Every PR created or substantially implemented by Codex must include a concise footer: **AI assistance:** Implemented with OpenAI Codex `<verified version>`; opened through Garett’s connected GitHub account.
- Include verified model names inline when available and relevant. Omit unavailable metadata, unknown-field placeholders, and metadata tables. Never guess versions/models or apply today's metadata to earlier work without evidence.
- Preserve credit for Garett's supplied writing, palette, designs, and decisions. Adapt the contribution wording when needed; GitHub's author remains the authenticated account.
- Add the footer when opening the PR and retain it when updating the description.

## Copy and content

- Use Garett's supplied and approved drafts as the baseline. Make focused edits instead of replacing his voice with generic portfolio or résumé language.
- Keep current work, technical experience, leadership experience, and education status accurate. Ask about missing personal details rather than inventing them.
- Do not publish private workplace incidents or infer permission to publish contact details from source material.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, checks, publication, and content authoring. Run checks appropriate to the change; do not add tests merely to mirror prose edits.
