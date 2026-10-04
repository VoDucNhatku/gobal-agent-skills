# Component Catalog

Canonical component patterns for build-ui-component.
Read this file; reference it, never inline it.

## Naming Convention

PascalCase for component files, kebab-case for CSS classes.
Component directory: `components/<component-name>/index.tsx`

## Pattern: Accessible Button

Required props: `variant` (primary/secondary/ghost/destructive), `size` (sm/md/lg), `disabled`, `aria-label`.
All variants share base: `inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50`.

## Pattern: Accessible Card

Requires: heading hierarchy (h2 or h3), body text, optional footer actions.
Use `<article>` semantic element. Minimum padding: p-6.

## Pattern: Data Table

Columns defined as array of `{key, label, sortable, render}`.
Supports: sort, filter, pagination. Empty/loading/error states required.
Accessibility: `role="grid"`, `aria-sort`, `aria-colindex`.

## Pattern: Form Input

Always paired with a `<label>` using `htmlFor`.
Error state: red border + `aria-invalid="true"` + `aria-describedby` pointing to error text.
Helper text: `aria-describedby` pointing to helper paragraph.

## Variant Naming

`<Component>-<variant>` for compound components, e.g. `Dialog-Trigger`, `Dialog-Content`.
