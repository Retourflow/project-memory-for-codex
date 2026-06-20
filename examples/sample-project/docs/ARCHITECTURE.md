# Architecture

Last verified: 2026-06-20

## System Overview

The example is a single-process Python application with in-memory state.

## Components

| Component | Responsibility | Primary Files | Status |
|---|---|---|---|
| Application | Create and list tasks | `src/app.py` | Implemented |

## Data Flow

1. A caller submits a task title.
2. The application appends it to an in-memory list.
3. The caller can retrieve the current list.
