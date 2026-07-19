---
name: review-frontend
description: Front-end audit Worker — scores a web surface against the anti-slop, accessibility, and token-consistency rubric, as binary pass/fail findings, then optionally fixes the high-confidence ones surgically. Runs the slop-cluster checklist (type, color, layout, components, icons, a11y/WCAG, copy, not-a-default-cluster) plus the quality floor (focus-visible, all states, responsive, reduced-motion). Modes — audit (default; pass/fail findings, severity-coded, no edits) and fix (apply only the high-confidence findings via surgical Edit, never a rewrite). Triggers — review the frontend, review the UI, đánh giá giao diện, kiểm tra UI, check for AI slop, chấm slop, a11y audit, kiểm tra accessibility, is this accessible, token consistency, design QA, audit the design. It judges/repairs an existing surface; it does NOT decide the look (use design-web) or build new components (use build-ui).
argument-hint: <file|url|component> [audit|fix]
allowed-tools: Read Edit Glob Grep WebFetch Bash
---

# Review Frontend (chấm anti-slop + a11y giao diện)

Audits a web surface against a mechanical rubric and reports binary pass/fail findings; in `fix`
mode, applies only the high-confidence repairs surgically. The goal is to catch generic "AI-slop"
UI and accessibility failures before ship.

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — report Vietnamese; preview §3;
scope handoff §10) and `~/.claude/rules/frontend-aesthetics.md` — the audit IS its §8 slop-cluster
checklist + §1 anti-slop list + §7 quality floor + §4 WCAG floor. Read at run time; never inline. If
a `notes/design-<slug>.md` exists, audit token-consistency AGAINST it (did the build drift from the
locked tokens?).

## Procedure

### Phase 0 — Resolve target + mode
Parse mode: `audit` (default) | `fix`. Target = a source file, a component, or a URL (WebFetch the
markup/CSS). Read the design-record if one exists (for token-drift checks).

### Phase 1 — Run the rubric as binary pass/fail (§8)
Score each, every failure is a finding with a severity (blocker / should-fix / nit):
1. **Type** — distinctive faces? real weight + size contrast? no bare Inter/Roboto/system-ui?
2. **Color** — 4-6 cohesive tokens, one dominant + one decisive accent? no SaaS-purple gradient?
   atmospheric (not flat) ground?
3. **Layout** — rhythm/asymmetry or generic stacked boxes? one signature element?
4. **Components** — branded, or untouched library defaults?
5. **Icons** — a real icon set, ZERO emoji-as-icons?
6. **A11y** — WCAG AA contrast (body ≥4.5:1, large/UI ≥3:1), focus-visible, reduced-motion, keyboard
   reachable, state not conveyed by color alone?
7. **Copy** — active voice, user-side labels, consistent verbs, actionable errors, inviting empty
   states?
8. **Slop clusters** — NOT the cream/serif/terracotta, near-black/acid, or broadsheet-rule default?
Each finding cites the exact place (file:line / selector) and the §-rule it fails, with the fix.

### Phase 2 — (fix mode only) Apply high-confidence repairs surgically
Apply ONLY the findings you are confident about (a wrong contrast value, a missing focus style, an
emoji-as-icon, a flat ground), using `Edit` with minimal unique spans — never a rewrite (anti-
runaway-edit). Leave judgment-call findings (a layout rethink) as report items for the user. Re-state
what you changed.

### Phase 3 — Report (§3)
- **audit:** a compact pass/fail table in chat — `| Rule | Pass | Severity | Chỗ | Sửa thế nào |` —
  capped at a 8-20 line preview (first rows + `(+N nữa)` if many); no file written.
- **fix:** the fix-log (what was edited) + which findings remain for the user.
End with the slop verdict (ship / rework) and the handoff.

## Output
Audit = chat report only (no file). Fix = in-place surgical edits + a chat fix-log.

## Gotchas
- **Binary, cited findings.** Each rule passes or fails, with the exact location + the §-rule + the
  fix — not vague impressions.
- **Audit ≠ fix.** Default `audit` never edits. `fix` edits ONLY high-confidence findings, surgically.
- **Token drift.** If a design-record exists, the build must match its locked tokens; flag drift.
- **Don't rewrite (anti-runaway-edit).** `fix` uses minimal `Edit` spans; a layout rethink is a
  report item, not an auto-rewrite.
- **Stay in scope (§10).** This skill JUDGES/REPAIRS:
  - `→ dùng design-web cho` quyết định lại hướng thiết kế nếu audit nói "rework".
  - `→ dùng build-ui cho` dựng/sửa lớn theo design-record.

## AI-Tell Blocklist (blocklist check — any match = finding)

Scan the target for these tell-tale AI-sloper patterns. Any match produces a critical or important finding:

| Pattern | Severity | Why it fires |
|---------|----------|---------------|
| Hero heading starts with "Welcome to" | Important | Generic SaaS opener |
| Body copy mentions "seamless" + "empower" in same paragraph | Important | Cliché AI-slop pairing |
| "99.9% uptime" or fake precision claims | Important | Fabricated metric without source |
| Placeholder photo "John Doe" / "Acme" / "Sample User" | Critical | Unreplaced placeholder shipped |
| "Lorem ipsum" anywhere in shipped content | Critical | Unreplaced placeholder shipped |
| Bare "#000" text (no font-family specified) on "#FFF" bg | Important | Inaccessible default, no atmosphere |
| Gradient-text headers (background-clip: text) | Important | Overused, fragile, often poor contrast |
| Three equal-width feature cards in a row | Important | Generic layout, no rhythm |
| Hand-rolled SVG icons mixed with a UI library | Minor | Inconsistent icon language |
| Emoji inside a `<button>` or `<nav>` element | Critical | Emoji-as-icon in interactive context |
| "Scroll down to learn more" text cue | Minor | Tells user they are missing context |
| Version/date label in hero ("v2.0 — 2026") | Minor | Leaks internal state to users |
| Fake product preview — colored `<div>` rectangles | Critical | Placeholder masquerading as real UI |
| Pure-text page claiming to be "minimalist" | Important | No design decisions made |

## Severity Classification

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Breaks a11y, unreplaced placeholder, violates hard rule | Must fix |
| **Important** | Slop pattern, poor contrast, generic layout | Should fix |
| **Minor** | Polish, style inconsistency | Fix when convenient |
| **FYI** | Suggestion, alternative approach | Note only |

## Pre-Flight Gate (before claiming "done")

- [ ] All 8 slop-cluster dimensions checked
- [ ] AI-Tell blocklist scanned
- [ ] Every finding has file:line or selector reference
- [ ] fix mode: re-audit after edits to verify
