# Implementation Plan: CLI Task Manager MVP

**Branch**: `001-cli-task-manager` | **Date**: 2025-11-19 | **Spec**: `specs/001-cli-task-manager/spec.md`
**Input**: Feature specification from `/specs/001-cli-task-manager/spec.md`

## Summary
MVP CLI for managing tasks (create, list, search) persisted in a single JSON file with atomic writes and a versioned schema. Emphasis on clean code, high test coverage (pytest), minimal dependencies, clear separation of layers (CLI, model, repository), and future extensibility to SQLite/Neo4J without changing CLI contract.

## Technical Context
**Language/Version**: Python 3.11  
**Primary Dependencies**: Standard library only (argparse, json, pathlib, typing, dataclasses); `pytest` for testing  
**Storage**: JSON file `tasks.json` (schema_version included)  
**Testing**: pytest + coverage (≥90% line changed modules, global ≥85%)  
**Target Platform**: Local workstation (single-process, Windows/Linux/macOS)  
**Project Type**: Single project CLI tool  
**Performance Goals**: List/search <300ms median @ ≤5k tasks; create <1s  
**Constraints**: No external DB; atomic file writes; minimal dependencies; no concurrency  
**Scale/Scope**: ≤5,000 tasks in single JSON file  

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Description | Verification Method |
|------|-------------|---------------------|
| Function Size | No function >40 logical lines (unless justified) | Static scan / reviewer checklist |
| Coverage | ≥90% line for changed modules; global ≥85% line; no regression | Pytest coverage report |
| Dependency Justification | All new deps have PR justification section | PR review notes |
| Boundary Separation | CLI layer has no direct file I/O; repository handles persistence | Code review of changed files |
| Error Documentation | Public functions/classes docstring list raised exceptions | Docstring inspection |
| Persistence Versioning | JSON schema has `schema_version` and migration for bumps | Presence of schema_version + migration file |
| JSON Output Stability | `--json` CLI mode returns valid structured output (success + error) | Integration test results |
| TDD Sequence | Tests written first (initial failing commit) precedes implementation | Commit history / PR description |

All gates must be green before implementation tasks proceed.

## Project Structure

### Documentation (this feature)
```text
specs/001-cli-task-manager/
├── spec.md
├── plan.md
├── checklists/
│   └── requirements.md
└── (later) tasks.md
```

### Source Code (repository root)
```text
src/
├── cli/
│   ├── main.py
│   ├── commands/
│   │   ├── create.py
│   │   ├── list.py
│   │   └── search.py
│   ├── formatting.py
│   ├── args_base.py
│   ├── logging_setup.py
│   └── commands/common.py (polish phase)
├── models/
│   ├── status.py
│   ├── task.py
│   └── validation.py
├── repository/
│   ├── json_repository.py
│   ├── schema.py
│   └── errors.py
├── services/
│   ├── id_allocator.py
│   ├── filtering.py
│   ├── search.py
│   └── seeder.py
└── __init__.py

tests/
├── unit/
│   ├── test_task_model.py
│   ├── test_repository_create.py
│   ├── test_list_filter.py
│   ├── test_search.py
├── integration/
│   ├── test_cli_create.py
│   ├── test_cli_list.py
│   ├── test_cli_search.py
│   └── test_error_cases.py (polish)
└── __init__.py

scripts/
└── benchmark_search.py (polish)

tasks.json (runtime data file)
.coveragerc (coverage policy)
README.md
```

**Structure Decision**: Single-project CLI with layered separation. Services layer encapsulates logic beyond persistence & models (filtering, search, id allocation) enabling future DB/graph replacement.

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| Services layer | Encapsulates logic separate from repository/model | Putting logic in CLI would break layer boundaries & hinder future storage switch |

(No other complexity beyond baseline; minimal dependencies.)

## Implementation Phases (High-Level)
1. Setup: Scaffolding, tooling, coverage config, README.
2. Foundational: Core domain & persistence components ready, CLI formatting & arg parsing.
3. User Story 1: Create task (tests first) + seed capability.
4. User Story 2: List tasks with optional status filter.
5. User Story 3: Search tasks by substring (case-insensitive).
6. Polish: Docs, performance benchmarking, error case tests, refactoring.

## Risks & Mitigations
- File corruption: atomic temp file writes + backup strategy.
- Performance scaling: simple list/search O(n) is acceptable @5k; future indexing migration planned.
- Future DB migration: repository abstraction & services logic independent from storage details.

## Test Strategy
- Unit tests: models, repository operations, filtering, search logic.
- Integration tests: CLI commands (create/list/search) human + JSON output.
- Error tests: invalid inputs, corrupted file recovery.
- Coverage enforced with `.coveragerc` thresholds.

## Performance Strategy
Benchmark script `scripts/benchmark_search.py` to load synthetic 5k tasks and measure search/list latency; optimize only if thresholds fail (e.g., precompute lowercase fields).

## Migration Outline (Future)
Introduce new repository implementation (e.g., SQLite) behind same interface; maintain CLI unchanged; add migration command to convert `tasks.json` to new store using schema version mapping.

## Next Step
Proceed to generate `tasks.md` with TDD-first tasks following constitution gates.
