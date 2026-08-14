# `.github/` Agent Instructions

- Treat workflow, ownership, publication, and repository-policy changes as consequential research-integrity changes.
- Declare explicit least-privilege workflow `permissions`; begin with `contents: read` and add write scopes only where required.
- Pin remote actions and reusable workflows to reviewed full 40-character commit SHAs; keep release tags only as comments.
- Never execute untrusted pull-request code in a privileged `pull_request_target` context.
- Keep private correspondence, personal data, source credentials, and secret values out of workflows, logs, artifacts, prompts, and state files.
- Automation must preserve source provenance, retrieval-completeness limits, contradictory evidence, owner criteria, and distinctions between raw evidence and synthesis.
- PR templates must request exact research/validation evidence, claim/provenance changes, privacy risk, final-diff review, continuity updates, and residual uncertainty.
- CODEOWNERS does not prove branch protection. Do not claim rulesets, secret scanning, or push protection are enabled without GitHub settings/API evidence.
- Do not impose software-only checks where they are not applicable; use exact citation, link, schema, data, or editorial gates actually maintained by the project.
