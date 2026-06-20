# Agent Instructions

Read project context and current state before non-trivial work. Load architecture
and decisions only when the task requires them.

Maintain backwards compatibility for the v1 JSON response. Do not send
notifications inside HTTP handlers. Verify changes with the unit tests.
