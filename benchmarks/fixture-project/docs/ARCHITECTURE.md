# Architecture

Last verified: 2026-06-20

## System Overview

StudyFlow is a layered Python service. `src/studyflow/api.py` is the HTTP entry
point. API handlers translate requests and call the application service.

## Components

- `api.py` calls `TaskService`.
- `TaskService` calls `TaskRepository`.
- `TaskService` calls `NotificationPort` after a task is completed.
- `SqliteTaskRepository` owns task persistence.

## Data Flow

1. The API validates a request.
2. `TaskService` applies task rules.
3. `TaskRepository` persists the result.
4. `NotificationPort` receives the completion event.

## Interfaces And Contracts

The v1 task response contains `id`, `title`, and `completed`.

## Data And Storage

SQLite is the persistence boundary.
