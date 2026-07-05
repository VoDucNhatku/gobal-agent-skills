---
name: "security-review"
description: "Security audit Worker — threat-models a change or surface, then scores it against the OWASP-grounded hardening rubric as binary pass/fail findings, severity-coded, each with a real file:line and a concrete fix. Theme-neutral; infers the stack. Runs STRIDE over each trust boundary (input validation, injection, auth/authz/IDOR, secrets, SSRF, headers, rate limiting, supply chain, LLM surface) plus the Always/Ask/Never check. Modes — audit (default; findings, no edits) and fix (apply only high-confidence Always-violations surgically via Edit, never a rewrite; Ask-First items flagged). Triggers — security review, security audit, kiểm tra bảo mật, đánh giá bảo mật, threat model, is this secure, có an toàn không, check for vulnerabilities, tìm lỗ hổng, OWASP, SQL injection, XSS, IDOR, SSRF, secrets in code, auth review, kiểm tra phân quyền. It judges/repairs security posture; it does NOT design or build features (use backend-engineer / build-ui) or do general correctness review (use code-senior review)."
argument-hint: "<diff | endpoint/area/file> [audit|fix]"
allowed-tools: "Read Edit Glob Grep Bash"
---

# Security Review (threat-model + audit + surgical fix)

Theme-neutral security audit: infer the stack from the project, threat-model the surface, and score
it against a concrete OWASP-grounded rubric as pass/fail findings — then optionally fix the
high-confidence ones surgically. This is the security counterpart of [[review-frontend]] (slop/a11y)
and is distinct from [[code-senior]] `review` (general correctness). It judges/repairs; it does not
design or build.

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — findings/identifiers English,
the chat report Vietnamese; preview-not-dump §3; fidelity §8 — every finding cites a real file:line,
no invented vulnerabilities). For course/LMS work the server-side-authz + entitlement rules are in
`~/.claude/rules/course-domain-model.md`. Read at run time; do not inline.

## Procedure

### Phase 0 — Resolve scope + mode + threat-model
Parse mode: `audit` (default) | `fix`. Resolve the target: a diff (`git diff` / changed region), an
endpoint, an area, or a file. Infer the stack by reading the project. **Threat-model first** (the
design gate, ~5 min): name each **trust boundary** where untrusted data enters (HTTP request, form,
upload, webhook, queue, third-party API, **LLM output**), the **assets** worth stealing
(credentials, PII, payment, admin actions), and run **STRIDE** as a quick lens over each boundary.
Read only the relevant regions (ranged reads for large files) — do not ingest the whole codebase.

### Phase 1 — Rubric pass (binary findings)
Score each axis pass/fail; any failure is a finding with `file:line`, severity, and a one-line fix.

1. **Input validation** — all external input validated at the boundary (schema/type), incl.
   third-party + LLM responses? Size caps + timeouts on untrusted input?
2. **Injection** — every DB query parameterized; no string-built SQL/NoSQL/shell with user data;
   no `eval`/`innerHTML` with user input?
3. **Auth / authz / IDOR** — every protected op checks the authenticated user OWNS / may access the
   resource, **server-side**? No access gated only on a client-supplied role? Admin paths verify role?
4. **Secrets** — none in code or git history; not logged; loaded from env; sensitive fields stripped
   from responses?
5. **SSRF** — server fetches of user-influenced URLs allowlist scheme+host and reject any private/
   reserved resolved IP, no redirects?
6. **Transport / headers** — HTTPS; security headers (CSP, HSTS, X-Frame-Options, X-Content-Type);
   CORS restricted to known origins (no wildcard with credentials)?
7. **Rate limiting / DoS** — auth + expensive endpoints rate-limited; input size + loop/recursion
   bounded?
8. **Supply chain** — lockfile committed, CI installs pinned (`npm ci` / equivalent); no known
   critical/high CVE reachable in a prod path; wary of typosquats / postinstall.
9. **LLM surface (if any)** — model output treated as untrusted (no eval/SQL/shell/markup); secrets
   + cross-tenant data kept out of prompts; tool permissions scoped; consumption bounded.

Map each finding to its **Always / Ask / Never** tier: Always-violation = should-fix/blocker;
Never-violation = blocker; Ask-First item = flag for human approval (do not auto-change).

### Phase 2 — `fix` (only if mode = fix)
Apply ONLY the high-confidence **Always-violations** via surgical `Edit` (parameterize a query, add
the ownership check, move a secret to env, add the missing header, tighten CORS). Never rewrite a
file; one concern per edit; read-before-edit. **Do NOT auto-change Ask-First items** (auth-flow
changes, new integrations, CORS posture shifts that alter behavior) — list them for approval. After
fixing, re-run the relevant check (request / test / `npm audit`) and report the REAL result.

### Phase 3 — Report (§3)
Print a **6-9 line** Vietnamese report: counts by severity (blocker / should-fix / nit), the top
findings (`file:line` + one-line each), what `fix` changed (if any) + its verify result, and the
remaining Ask-First items awaiting a decision. Write the full findings table to
`notes/security-review-<slug>.md`. Do NOT dump code or the full table into chat — paths + key lines.

## Gotchas
- **Threat-model before scoring** — controls without a threat model are guesses (OWASP A04).
- **Authentication ≠ authorization.** The most common real bug is a missing ownership check (IDOR),
  not a missing login. Check every protected op, server-side.
- **No invented findings (§8).** Every finding cites a real `file:line`; if a check can't be
  verified from the code, say `chưa xác minh được (not verifiable from source)`, don't guess.
- **`fix` is surgical + conservative** — Always-violations only; Ask-First items are flagged, never
  auto-applied; never a rewrite.
- **Don't dump to chat (§3).** Findings table → file; chat gets the path + severity counts + top items.
- **Stay in scope (§10).** This skill audits/repairs security posture:
  - `→ dùng backend-engineer cho` thiết kế/dựng endpoint hoặc làm cứng có cấu trúc.
  - `→ dùng code-senior review cho` đánh giá đúng-sai/chất lượng chung (không phải bảo mật).
  - `→ dùng review-frontend cho` audit slop + a11y giao diện.
