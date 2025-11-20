<!--
Sync Impact Report
Version change: (initial) → 1.0.0
Modified principles: (template placeholders replaced with concrete principles)
Added sections: Naming & Documentation Guidelines; Development Workflow & Gates
Removed sections: None (template placeholders consolidated)
Templates requiring updates: 
	.specify/templates/plan-template.md (⚠ pending update for gates)
	.specify/templates/tasks-template.md (⚠ pending update to enforce mandatory tests)
Deferred TODOs: None
-->

# spec-kit-task-manager Constitution

## Core Principles

### I. Clean Code & Clarity
Code MUST be readable, intentional, and minimal. Functions SHOULD NOT exceed 40 logical lines and MUST express a single responsibility. No anonymous magic: avoid implicit side effects and hidden globals. Public modules MUST expose explicit entry points; internal helpers stay private. Clarity outweighs cleverness.

### II. Test Coverage & TDD (Pytest)
All production code MUST be preceded by failing pytest tests (Red-Green-Refactor). Minimum coverage: 90% line, 85% branches for changed modules; new feature modules MUST begin at ≥90% line coverage. No merge if coverage regression occurs without approved justification. Integration tests MUST validate CLI behavior (human + JSON modes) and persistence edge cases.

### III. Data Persistence & Extensibility
Primary storage is a single JSON file (tasks.json) with a versioned schema field `schema_version`. Schema changes MUST be backward compatible for MINOR bumps; breaking schema changes REQUIRE MAJOR bump + migration script. Design data access through a repository layer to enable future SQLite (or other) migration without leaking storage details into models or CLI.

### IV. Minimal Dependencies & Maintainability
Dependencies MUST be justified: provide a measurable benefit (performance, reliability, clarity) over a standard library alternative. Adding a new dependency requires a PR justification section and MUST NOT duplicate existing functionality. Periodic audit quarterly; pin versions in lock files. Remove unused dependencies promptly.

### V. Explicit Error Handling & Responsibility Boundaries
All failures MUST surface explicit error messages (no silent pass). CLI layer: argument parsing, user feedback, exit codes. Repository layer: persistence, serialization, integrity checks. Model layer: domain invariants only (no I/O). Do not couple CLI with persistence or models with formatting. Logged errors MUST include operation context and not expose sensitive file paths.

## Naming & Documentation Guidelines

Naming MUST reflect purpose (verbs for commands, nouns for models). Python modules: snake_case; Classes: PascalCase; Functions & variables: snake_case; Constants: UPPER_SNAKE. Each public function/class MUST have a docstring describing intent, params, return, and error cases. Docstrings MUST specify raised exceptions. Inline comments are reserved for non-obvious rationale, not restating code. README and CLI `--help` MUST stay consistent with actual behavior.

## Development Workflow & Gates

1. Spec: Capture user stories + data needs using `spec-template.md`.
2. Plan: Enumerate structure, tasks, coverage targets in `plan-template.md` (Constitution Check section lists gates below).
3. Tests First: Write failing unit + integration tests with pytest.
4. Implement: Small commits; each passes existing tests; refactor only after green.
5. Review: Enforce principles (function size, coverage, dependency justification, clear naming, layer boundaries).
6. Persistence: All mutations route through repository; JSON file modifications atomic (write temp then replace).
7. Error Surfaces: Non-zero exit codes on failure; structured JSON errors when `--json` flag used.
8. Coverage Gate: CI job MUST fail if thresholds unmet.

Gates (Must Pass Before Merge):
- Function Size Gate: No function >40 lines (exceptions justified in PR).
- Coverage Gate: ≥90% line coverage for changed code; global line coverage MUST NOT drop below 85%.
- Dependency Gate: New dependency includes justification + security review note.
- Boundary Gate: CLI does not perform direct file writes (delegates to repository).
- Error Gate: All new public functions document raised exceptions.
- Persistence Gate: JSON schema version defined; migrations included for bumps.

## Governance

This constitution supersedes ad-hoc decisions. Amendments require: (1) written proposal summarizing change & rationale; (2) review approval; (3) semantic version increment per impact; (4) migration or deprecation notes if breaking. Violations discovered post-merge MUST be scheduled as priority remediation tasks within next sprint. Versioning follows Semantic Versioning: MAJOR for breaking API/storage changes; MINOR for backward-compatible features/principles; PATCH for clarifications/doc/test improvements. Reviewers MUST validate gates. Any dependency or schema change without proper version bump is considered a violation.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19

