# Course Domain Model (binding LMS entity model)

Binding entity model for the course-selling / LMS platform skills. Pulled by
`scaffold-course-platform`, `build-admin-dashboard`, and `build-ui-component`
(where domain-aware). It defines the entities, their relations, and role-gating
semantics. Skills cite this file in one line and read it at run time only — they
do not inline it. Entity, field, and identifier names are **English** (per
`~/.claude/rules/workbench-conventions.md` §1); human-facing prose stays Vietnamese.

---

## CRITICAL RULE — authorization & entitlement are SERVER-SIDE only

**Never gate access on a client-side role check.** A role claim in the browser
(JWT in localStorage, a React `useUser().role`, a hidden CSS class) is a *UI hint*,
not a security boundary. Anyone can forge it.

- **Entitlement = a real row in the database**, not a flag the client sends. A user
  may view/play a paid `Lesson` only if a matching `Enrollment` (backed by a `paid`
  `Order`) exists for `(user_id, course_id)`, verified on the **server** for every
  request.
- **The payment provider's webhook is the source of truth.** A successful Stripe
  `checkout.session.completed` / `invoice.paid` webhook (verified by signature,
  idempotent on `event.id`) is what **writes** the `Order` (`status = paid`) and
  **creates/activates** the `Enrollment`. A client redirect to `/success` MUST NOT
  grant access — the user can hit that URL without paying.
- **Every mutation and every gated read** (admin CRUD, lesson content, video URL,
  progress write) is authorized server-side: route handler / server action / RLS
  policy / middleware. Client role only decides what to *render*, never what to
  *allow*.
- Role escalation (`student → instructor → admin`) is set **server-side** by an
  authorized admin path, never self-asserted by the client.

---

## Entities & relations

| Entity | Key fields | Relations |
|---|---|---|
| **User** | `id`, `email` (unique), `password_hash`/`oauth`, `name`, `avatar_url`, `created_at` | has many `Enrollment`, `Order`, `Progress`, `Review`; has many `Role` (via `UserRole`); as instructor owns many `Course` |
| **Role** | `id`, `name` enum `student\|instructor\|admin` | many-to-many with `User` via `UserRole`; server-assigned only |
| **Course** | `id`, `slug` (unique), `title`, `description`, `price_cents`, `currency`, `thumbnail_url`, `status` enum `draft\|published\|archived`, `instructor_id`→User, `created_at` | belongs to instructor `User`; has many `Module`, `Enrollment`, `Review`; referenced by `Order`, `Coupon` |
| **Module** (Section) | `id`, `course_id`→Course, `title`, `position` (int order) | belongs to `Course`; has many `Lesson`; ordered by `position` |
| **Lesson** | `id`, `module_id`→Module, `title`, `position`, `content_type` enum `video\|article\|quiz`, `video_asset_id`, `duration_sec`, `is_free_preview` (bool) | belongs to `Module`; has many `Progress`; gated unless `is_free_preview` |
| **Enrollment** | `id`, `user_id`→User, `course_id`→Course, `status` enum `active\|refunded\|expired`, `source` enum `purchase\|coupon\|admin_grant`, `order_id`→Order (nullable for grants), `created_at`; unique `(user_id, course_id)` | the **entitlement** linking `User`↔`Course`; created by paid `Order` (webhook) or admin grant |
| **Order** (Payment) | `id`, `user_id`→User, `course_id`→Course, `amount_cents`, `currency`, `status` enum `pending\|paid\|failed\|refunded`, `provider` enum `stripe\|lemonsqueezy`, `provider_session_id`, `provider_event_id` (idempotency), `coupon_id`→Coupon (nullable), `created_at` | belongs to `User` + `Course`; on `paid` (via webhook) creates the `Enrollment`; may apply one `Coupon` |
| **Coupon** | `id`, `code` (unique), `discount_type` enum `percent\|fixed`, `discount_value`, `course_id`→Course (nullable = global), `max_redemptions`, `redeemed_count`, `expires_at`, `active` (bool) | optionally scoped to one `Course`; applied by `Order`; validity enforced **server-side** at checkout |
| **Progress** | `id`, `user_id`→User, `lesson_id`→Lesson, `status` enum `not_started\|in_progress\|completed`, `last_position_sec`, `completed_at`; unique `(user_id, lesson_id)` | belongs to `User` + `Lesson`; writable only if the user is entitled to the lesson's course |
| **Review** | `id`, `user_id`→User, `course_id`→Course, `rating` (1–5), `body`, `created_at`; unique `(user_id, course_id)` | belongs to `User` + `Course`; **creatable only if an `Enrollment` exists** (verified server-side) |

---

## Relationship summary

```
User 1───* Enrollment *───1 Course 1───* Module 1───* Lesson 1───* Progress *───1 User
User 1───* Order      *───1 Course                                  Lesson *───1 (entitled) User
Order *───0..1 Coupon         Coupon 0..1───1 Course
User *───* Role (UserRole)    Course *───1 User (instructor)
User 1───* Review *───1 Course
```

- An **`Enrollment`** is the join that proves entitlement; it is the row every gated
  read/write checks. A paid **`Order`** (or explicit admin grant) is the *only* thing
  that creates one.
- A **`Course`** is owned by one instructor `User`, organized into ordered `Module`s,
  each holding ordered `Lesson`s. Only `is_free_preview` lessons are viewable without
  an `Enrollment`.

---

## Role-gating semantics (enforced server-side)

| Capability | student | instructor | admin |
|---|---|---|---|
| Browse marketing pages, free-preview lessons | ✅ | ✅ | ✅ |
| Purchase a course (create `Order`) | ✅ | ✅ | ✅ |
| View paid `Lesson` content / video URL | only if entitled (own `Enrollment`) | own courses + entitled | ✅ all |
| Write own `Progress` | only for entitled lessons | own courses | ✅ |
| Write a `Review` | only if entitled | only if entitled | ✅ |
| Create/edit/publish a `Course`, `Module`, `Lesson` | ❌ | ✅ own courses only | ✅ any |
| Manage `Enrollment`, `Order`, refunds, `Coupon` | ❌ | own courses (read/limited) | ✅ |
| Admin-grant an `Enrollment`, assign `Role` | ❌ | ❌ | ✅ |
| Access admin/management dashboard | ❌ | ✅ scoped to own courses | ✅ |

- "Entitled" everywhere means **a server-verified `Enrollment` row** for
  `(user.id, course.id)`, not a client-supplied role or course-id.
- Instructors are scoped to **their own** `Course` rows (`instructor_id = user.id`),
  enforced in the query/RLS policy — never by a client-side filter.
- The client may hide a button it expects the user can't use, but the **server still
  re-checks** on the actual request. UI gating and security gating are separate
  layers; the server layer is authoritative.

---

## Notes for generators

- Default money handling: integer `*_cents` + ISO `currency`; never floats.
- Idempotency: webhook handlers dedupe on `provider_event_id`; `Order`→`Enrollment`
  creation is transactional and idempotent.
- Soft states (`draft`/`archived`, `refunded`/`expired`) are filtered server-side so
  unpublished or revoked content never reaches an unentitled client.
