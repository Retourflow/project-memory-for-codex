# Architecture Decisions

## ADR-002: Trigger Notifications In The Service Layer

- Status: Accepted

Notifications are triggered in the service layer, not HTTP handlers. This keeps
completion behavior consistent for future CLI or background-job adapters.

## ADR-001: Keep SQLite Behind A Repository

- Status: Accepted

SQLite is the persistence boundary. Application behavior depends on
`TaskRepository`, not SQL statements.
