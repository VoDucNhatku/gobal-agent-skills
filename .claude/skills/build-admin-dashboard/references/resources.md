# Admin Dashboard — Resource Patterns

Layout patterns and component defaults for build-admin-dashboard.
Read this file; reference it, never inline it.

## Layout Shell

- Sidebar nav: fixed left, collapsible, role-filtered menu items
- Top bar: breadcrumbs, user menu, notifications badge
- Main content: scrollable, max-width container for readability
- Responsive: sidebar collapses to hamburger < 1024px

## Data Table Defaults

- Sortable on first click, sort direction toggled on second
- Filter: text filter across all text columns; date range where applicable
- Pagination: 20 rows/page, show "showing X-Y of Z"
- Row actions: view, edit, delete (gated by role matrix)

## Role Matrix

| Role | View | Create | Edit | Delete |
|------|------|--------|------|--------|
| Admin | All | All | All | All |
| Instructor | Own resources | Own | Own | Own |
| Student | Own progress | None | None | None |

## Analytics Snapshot

Top cards: total count, active count, growth rate (period comparison).
Chart: bar/line for trend over time.
