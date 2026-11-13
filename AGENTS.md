# Repository instructions

## Issue-based workflow

- Every repository change must be associated with a GitHub issue, including documentation, configuration, copy, maintenance, and agent-rule changes.
- Before editing, find an existing issue that covers the work or create one. Do not create duplicate issues for follow-up fixes within the same scope.
- Start from the latest default branch and create or switch to a dedicated issue branch before making changes. Prefer `<issue-number>-<short-description>`.
- Keep unrelated work in separate branches and pull requests. Preserve uncommitted work belonging to other tasks.
- Reference the issue in the pull request. Use `Closes #N` only when the change completes its scope; otherwise use `Related to #N` and state what remains.
- Check review feedback and CI before reporting a change as ready. Report any verification that could not run.

## Copy and content

- Use Garett's supplied and approved drafts as the baseline. Make focused edits instead of replacing his voice with generic portfolio or résumé language.
- Keep current work, technical experience, leadership experience, and education status accurate. Ask about missing personal details rather than inventing them.
- Do not publish private workplace incidents or infer permission to publish contact details from source material.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, checks, publication, and content authoring. Run checks appropriate to the change; do not add tests merely to mirror prose edits.
