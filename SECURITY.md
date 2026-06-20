# Security Policy

## Supported Versions

Security fixes are applied to the latest version on the default branch.

## Data And Privacy

Project Memory for Codex is a local, file-based toolkit:

- It does not make network requests.
- It does not collect telemetry or analytics.
- It does not require API keys, account credentials, or a hosted service.
- It writes only to the target project selected by the user.
- Initialization preserves existing files unless `--force` or `-Force` is
  explicitly supplied.

The toolkit cannot guarantee that an agent will never place sensitive content
in a project-memory document. Users and maintainers should review generated
content before committing or publishing it.

Never store the following in project memory:

- passwords, API keys, access tokens, private keys, or session cookies;
- personal, medical, financial, or regulated data;
- private repository URLs, internal hostnames, or local machine paths that
  should not be shared;
- proprietary source excerpts that should not be committed to the repository.

Use a dedicated secret manager or ignored local configuration for sensitive
values. Record only the name and purpose of a required secret, not its value.

## Safe Use

- Inspect scripts before running them in an untrusted fork.
- Use initialization without force first.
- Review the generated diff before committing project-memory files.
- Keep Codex sandboxing, approvals, and repository permissions enabled.
- Do not add instructions that bypass user confirmation, security controls, or
  source-system permissions.

## Reporting A Vulnerability

Do not open a public issue for an unpatched vulnerability or exposed secret.
Use GitHub's private vulnerability reporting for this repository when
available. Include:

- the affected file or component;
- reproduction steps;
- the expected security impact;
- any suggested mitigation.

If private reporting is unavailable, open a minimal issue asking the maintainer
for a private contact channel without disclosing exploit details.

## Scope

Security reports should concern this repository's scripts, templates,
validators, benchmark tooling, or Skill instructions. Vulnerabilities in Codex,
GitHub, operating systems, or third-party tools should be reported to their
respective maintainers.
