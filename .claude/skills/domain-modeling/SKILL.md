---
name: "domain-modeling"
description: "Domain modeling for GOBAL AGENT — creates domain models (entities, value objects, aggregates) from business requirements. Source: mattpocock (domain-modeling). Use when designing the data model for a new feature, refactoring existing entities, or aligning code with business rules."
argument-hint: "<feature | entity-name>"
allowed-tools: "Read Write Bash Glob WebSearch WebFetch"
---

# Domain Modeling

> **Source:** mattpocock (domain-modeling)
> **Purpose:** Translate business requirements into a precise, enforceable domain model.

## Overview

Domain modeling creates the vocabulary and rules that bridge business language and code. A good model makes invalid states unrepresentable and business rules self-enforcing.

**Announce at start:** "I'm using the domain-modeling skill to design the domain model."

---

## Core Concepts

| Concept | Definition | Example |
|---------|-----------|---------|
| **Entity** | Object with persistent identity | `User`, `Course`, `Order` |
| **Value Object** | Object defined by its attributes, no identity | `Money`, `Address`, `Email` |
| **Aggregate** | Cluster of entities/value objects with a root | `Order` + `OrderItem` + `Payment` |
| **Repository** | Collection-like interface for aggregates | `OrderRepository.findByUser()` |
| **Domain Event** | Something that happened in the domain | `OrderPaid`, `CoursePublished` |
| **Invariant** | Business rule that must always hold | "Order total ≥ 0" |

---

## Modeling Process

### Step 1: Extract Nouns from Requirements

Read the requirements/spec. List every noun that represents something in the business domain.

```
Requirements: "Students enroll in courses. Each enrollment has a status.
Instructors own courses. Courses have modules with lessons."

Nouns: Student, Course, Enrollment, Status, Instructor, Module, Lesson
```

### Step 2: Classify Each Noun

| Classification | Criteria | Action |
|---------------|----------|--------|
| Entity | Has identity, persists over time | Create entity class |
| Value Object | Defined by attributes, immutable | Create value object |
| Enum | Finite set of values | Create enum/union type |
| Ignore | Implementation detail, not domain | Skip |

### Step 3: Define Relationships

Map how entities relate:

```
User 1 ──── * Enrollment * ──── 1 Course
Course 1 ──── * Module 1 ──── * Lesson
```

**Relationship types:**
- `1:1` — One-to-one (rare)
- `1:*` — One-to-many (common)
- `*:*` — Many-to-many (via join entity)

### Step 4: Identify Aggregates

An aggregate is a consistency boundary. All invariants within an aggregate are enforced atomically.

```
Aggregate: Order
  Root: Order
  Members: OrderItem, Payment
  Invariant: "Order total = sum(OrderItem totals)"

Aggregate: Course
  Root: Course
  Members: Module, Lesson
  Invariant: "Lesson positions unique within module"
```

**Rule:** References between aggregates go through the root entity only.

### Step 5: Define Invariants

For each aggregate, list business rules that must always hold:

```markdown
## Order Invariants
1. Total amount ≥ 0
2. Cannot transition from `paid` to `pending`
3. Cannot have more redemptions than max

## Enrollment Invariants
1. Unique (user_id, course_id)
2. Cannot be active if order is not paid
3. Status transitions: pending → active → refunded/expired
```

### Step 6: Define Domain Events

Events that other parts of the system need to react to:

| Event | Trigger | Reactions |
|-------|---------|-----------|
| `OrderPaid` | Webhook confirms payment | Create Enrollment, send email |
| `CoursePublished` | Instructor publishes | Notify enrolled students |
| `EnrollmentRefunded` | Admin refunds | Revoke access, notify instructor |

---

## Output Format

### Entity Definition

```markdown
### Entity: <Name>

**Identity:** `<id_field>` (UUID)
**Lifecycle:** Created when [event], deleted when [event]
**Relationships:**
- Belongs to: [parent entity]
- Has many: [child entities]

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key |
| `field` | type | Yes/No | Description |

**Invariants:**
1. [Business rule]
2. [Business rule]
```

### Value Object Definition

```markdown
### Value Object: <Name>

**Definition:** [What it represents]
**Immutability:** Immutable — created once, never modified
**Equality:** By value (all fields equal)

**Fields:**
| Field | Type | Notes |
|-------|------|-------|
| `field` | type | Description |
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Anemic model (entities are just data bags) | Business logic scattered in services | Move logic into entities |
| God entity (does everything) | Hard to maintain, test | Split into aggregates |
| Primitive obsession (using `string` for email) | No validation, no type safety | Create value objects |
| Bidirectional references everywhere | Circular dependencies | Choose direction, use IDs |
| Ignoring invariants | Invalid state possible | Enforce in entity methods |
| Over-modeling (modeling everything) | Unnecessary complexity | Model only what has business rules |

---

## Integration

**Required workflow skills:**
- `brainstorming` → Requirements before modeling
- `spec-writer` → Formal specification input
- `writing-plans` → Plan implementation of the model
- `backend-engineer` → Implement the model

**Companion skills:**
- `course-domain-model` → Reference for LMS entities
- `security-review` → Authorization rules in model
- `tdd-enforcer` → Tests for model invariants

---

## Cross-References

- `brainstorming` → Requirements gathering
- `spec-writer` → Formal specification
- `writing-plans` → Implementation planning
- `backend-engineer` → Code implementation
- `course-domain-model` → GOBAL LMS entity reference
