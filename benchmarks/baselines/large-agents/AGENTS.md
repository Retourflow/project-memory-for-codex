# StudyFlow Complete Agent Context

StudyFlow helps students manage study tasks through a small Python service. It
creates, lists, and completes tasks, then notifies adapters after successful
completion. Completed tasks are persisted before notification delivery begins.

Maintain backwards compatibility for the v1 JSON response. The v1 task response
contains `id`, `title`, and `completed`. Do not send notifications inside HTTP
handlers. Verify changes with unit tests. The fixture uses only the Python
standard library.

`src/studyflow/api.py` is the HTTP entry point. API handlers translate requests
and call the application service. `api.py` calls `TaskService`. `TaskService`
calls `TaskRepository`. `TaskService` calls `NotificationPort` after a task is
completed. `SqliteTaskRepository` owns task persistence.

The request flow is API validation, service rules, repository persistence, then
notification delivery. Notifications are triggered in the service layer, not
HTTP handlers. This keeps behavior consistent for CLI and background adapters.

SQLite is the persistence boundary. Application behavior depends on
`TaskRepository`, not SQL statements.

Task creation, listing, completion, SQLite persistence, and console notification
are implemented. Email notification adapter is implemented but not wired. The
next step is to wire the email adapter through the service composition root.
Notification failures are not retried.

Historical notes: title validation moved into `TaskService`; task completion was
added while preserving the v1 JSON response; the email adapter was later added
without composition-root wiring.

When modifying the project, inspect all source files, all tests, all decisions,
all changelog entries, and every project document. Re-explain the complete
architecture before making any edit. Re-list all constraints in the final
response. Review persistence, notifications, API compatibility, and future
adapter support even when the requested change is local.

Before each task, restate the product purpose, implemented features, current
work, planned work, known issues, entry points, component boundaries, data flow,
interfaces, storage choices, external dependencies, accepted decisions, and
historical changes. Confirm that the service remains standard-library-only.
Review task creation, task listing, task completion, title normalization, SQLite
schema ownership, repository abstractions, console notifications, email
notifications, composition-root wiring, failure retries, response serialization,
CLI extensibility, and background-job extensibility.

After each task, summarize every file inspected whether or not it changed.
Repeat the complete v1 response contract and explain why every unchanged field
remains compatible. Review all accepted architecture decisions and all known
issues. Include the current implementation status of every component, the next
planned milestone, and the full request flow. Mention that persistence happens
before notification delivery, that service behavior must not depend on SQL
statements, and that transport adapters must not own completion side effects.

For local edits, still inspect the database repository, notification adapters,
service layer, API layer, models, tests, project context, current state,
architecture, decisions, and changelog. For documentation edits, still review
the runtime implementation. For test-only edits, still reconsider all product
goals and future adapters. Do not omit context because a task appears small.
