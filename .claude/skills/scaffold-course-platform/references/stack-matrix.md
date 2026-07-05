# Course Platform Stack Matrix

Approved tech stack defaults per layer for the scaffold-course-platform skill.
Read this file; override any layer deliberately and record in audit-log.

## Full Stack Default

| Layer | Default | Rationale |
|-------|---------|-----------|
| Framework | Next.js 14 (App Router) | SSR + routing + API routes in one |
| Language | TypeScript | Type safety across the stack |
| Styling | Tailwind CSS + shadcn/ui | Fast, consistent token system |
| Database | PostgreSQL (Supabase / Neon) | JSON columns for flexible schemas |
| Auth | Supabase Auth (email + OAuth) | Built-in RLS, session mgmt |
| Payments | Stripe | checkout.session webhooks + webhook signature verify |
| Storage | Supabase Storage / S3 | Video thumbnails, user avatars |
| Video | Mux / Cloudflare Stream | HLS streaming + analytics |
| Email | Resend / Supabase Email | Transactional emails |
| ORM | Drizzle ORM | Type-safe, lightweight |
| Validation | Zod | Runtime + static validation |

## Override Record

If an intentional override is made, log it in audit-log before continuing.
| Layer | Override | Reason |
|-------|----------|--------|
| (none yet) | | |

## Minimal Viable Overrides

- Stripe → LemonSqueezy: supported but webhook handler differs
- Supabase → Neon: swap connection string, keep RLS
- shadcn → Radix primitives: still works but loses shadcn token system
