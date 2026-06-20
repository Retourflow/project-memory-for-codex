# Current State

Last verified: 2026-06-20

## Implemented

- Task creation, listing, and completion.
- SQLite repository and console notification adapter.

## In Progress

- Email notification adapter is implemented but not wired.

## Planned Next

1. Wire the email adapter through the service composition root.

## Known Issues

- Notification failures are not retried.

## Active Entry Points

- `src/studyflow/api.py`: HTTP-style request adapter.
- `src/studyflow/service.py`: application behavior.
