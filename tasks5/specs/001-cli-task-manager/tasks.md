# Tasks: CLI Task Manager MVP

**Input**: Design documents from `/specs/001-cli-task-manager/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are MANDATORY (TDD). All implementation tasks MUST have preceding failing tests (unit + integration/contract as appropriate). No production code without coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---
## Phase 1: Setup (Shared Infrastructure)
**Purpose**: Project initialization and baseline tooling

- [X] T001 Create base source directories: `src/cli`, `src/models`, `src/repository`, `src/services`, `tests/unit`, `tests/integration`
- [X] T002 Initialize Python project with `pyproject.toml` including `pytest` dev dependency
- [X] T003 [P] Create initial empty `tasks.json` with schema_version=1 and `{ "tasks": [] }`
- [X] T004 [P] Add `.coveragerc` enforcing 90% line, 85% branch thresholds
- [X] T005 [P] Draft `README.md` with overview and planned commands
- [X] T006 Add `scripts/benchmark_search.py` placeholder (performance harness skeleton)

---
## Phase 2: Foundational (Blocking Prerequisites)
**Purpose**: Core domain & persistence ready; MUST complete before user stories

- [X] T007 Implement status enum in `src/models/status.py`
- [X] T008 [P] Implement Task model with validation in `src/models/task.py`
- [X] T009 Define schema constants (`schema_version`) in `src/repository/schema.py`
- [X] T010 Implement repository error types in `src/repository/errors.py`
- [X] T011 Implement JSON repository with atomic write & backup in `src/repository/json_repository.py`
- [X] T012 [P] Implement id allocator service in `src/services/id_allocator.py`
- [X] T013 Implement CLI formatting helpers (human + JSON) in `src/cli/formatting.py`
- [X] T014 [P] Implement base argument parsing module in `src/cli/args_base.py`
- [X] T015 Implement logging setup in `src/cli/logging_setup.py`
- [X] T016 [P] Create validation utilities centralizing error messages in `src/models/validation.py`

**Checkpoint**: Foundation ready; proceed to user stories.

---
## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP
**Goal**: User can create tasks with required title, optional description/status; persisted and retrievable.
**Independent Test**: Running only create + list subset (list minimal stub) verifies persistence & JSON output.

### Tests for User Story 1 (MANDATORY - write first) ⚠️
- [X] T017 [P] [US1] Unit test task model creation & invalid title in `tests/unit/test_task_model.py`
- [X] T018 [P] [US1] Unit test repository create path + atomic write in `tests/unit/test_repository_create.py`
- [X] T019 [P] [US1] Integration test CLI create (human output) in `tests/integration/test_cli_create.py`
- [X] T020 [P] [US1] Integration test CLI create JSON output in `tests/integration/test_cli_create_json.py`

### Implementation for User Story 1
- [X] T021 [P] [US1] Implement create command logic in `src/cli/commands/create.py`
- [X] T022 [US1] Wire create command into entrypoint in `src/cli/main.py`
- [X] T023 [US1] Implement seeding utility for sample tasks in `src/services/seeder.py`
- [X] T024 [US1] Add centralized error handling for create in `src/cli/commands/create.py`
- [X] T025 [US1] Add logging for create operations in `src/cli/logging_setup.py`

**Checkpoint**: User Story 1 fully functional; tasks can be created & inspected via temporary list.

---
## Phase 4: User Story 2 - List Tasks (Priority: P2)
**Goal**: User can view all tasks and filter by status.
**Independent Test**: List command alone operates over existing tasks (created via seed or manual). Works without search functionality.

### Tests for User Story 2 (MANDATORY - write first) ⚠️
- [X] T026 [P] [US2] Unit test status filtering logic in `tests/unit/test_list_filter.py`
- [X] T027 [P] [US2] Integration test CLI list human output in `tests/integration/test_cli_list.py`
- [X] T028 [P] [US2] Integration test CLI list JSON output + status filter in `tests/integration/test_cli_list_json.py`

### Implementation for User Story 2
- [X] T029 [P] [US2] Implement list command in `src/cli/commands/list.py`
- [X] T030 [US2] Implement status filtering service in `src/services/filtering.py`
- [X] T031 [US2] Wire list command into entrypoint in `src/cli/main.py`
- [X] T032 [US2] Add empty-store messaging + JSON empty array handling in `src/cli/commands/list.py`

**Checkpoint**: User Story 2 independently testable (create assumed available but not required for base listing if seed used).

---
## Phase 5: User Story 3 - Search Tasks (Priority: P3)
**Goal**: User can search tasks by substring (case-insensitive) across title & description.
**Independent Test**: Search command works with seeded or previously created tasks; no dependency on list internals beyond repository access.

### Tests for User Story 3 (MANDATORY - write first) ⚠️
- [X] T033 [P] [US3] Unit test search logic (case-insensitive) in `tests/unit/test_search.py`
- [X] T034 [P] [US3] Integration test CLI search human output in `tests/integration/test_cli_search.py`
- [X] T035 [P] [US3] Integration test CLI search JSON output no matches & matches in `tests/integration/test_cli_search_json.py`

### Implementation for User Story 3
- [X] T036 [P] [US3] Implement search service in `src/services/search.py`
- [X] T037 [US3] Implement search command in `src/cli/commands/search.py`
- [X] T038 [US3] Wire search command into entrypoint in `src/cli/main.py`
- [X] T039 [US3] Add empty-result messaging & JSON format in `src/cli/commands/search.py`

**Checkpoint**: All three user stories independently functional & testable.

---
## Phase 6: Polish & Cross-Cutting Concerns
**Purpose**: Hardening, documentation, performance, refactoring.

- [X] T040 [P] Update `README.md` with full usage examples (create/list/search + JSON flag)
- [X] T041 Add migration outline to `docs/migration.md`
- [X] T042 [P] Add error cases integration tests in `tests/integration/test_error_cases.py`
- [X] T043 Refactor shared CLI command utilities into `src/cli/commands/common.py`
- [X] T044 [P] Add performance benchmark script implementation in `scripts/benchmark_search.py`
- [X] T045 Add coverage badge generation step doc `README.md`
- [X] T046 [P] Add seed sample tasks file `docs/sample_tasks.json` for demos

---
## Dependencies & Execution Order
### Phase Dependencies
- Setup → Foundational → User Stories (3–5 can proceed only after Foundational complete)
- User stories can be developed sequentially (P1→P2→P3) or in parallel after Foundational
- Polish after desired stories complete

### User Story Independence
- US1 requires foundational only.
- US2 requires foundational; optionally uses US1 to create real tasks but can rely on seed.
- US3 requires foundational; independent of US2 (search logic direct over repository results).

### Within Each User Story
- Tests (unit + integration) MUST precede implementation tasks.
- Parallelizable tasks marked [P] may run concurrently once tests exist in failing state.
- Command wiring into `main.py` done after command module & service exist.

### Parallel Opportunities
- Setup: T003, T004, T005 can parallel after T001 & T002.
- Foundational: T008, T012, T014, T016 can run in parallel; others sequential for dependency formation.
- User Story 1 tests: T017–T020 parallel; then implementations T021 & T023 parallel; wiring after (T022).
- User Story 2 tests: T026–T028 parallel; implementations T029 & T030 parallel; wiring T031 next.
- User Story 3 tests: T033–T035 parallel; implementations T036 & T037 parallel; wiring T038.
- Polish: Multiple [P] tasks can run simultaneously.

---
## Parallel Example: User Story 1
```
# In parallel (after foundational):
T017 tests/unit/test_task_model.py (failing first)
T018 tests/unit/test_repository_create.py (failing first)
T019 tests/integration/test_cli_create.py (failing first)
T020 tests/integration/test_cli_create_json.py (failing first)

# After tests red:
T021 src/cli/commands/create.py
T023 src/services/seeder.py

# Then:
T022 src/cli/main.py (wire command)
```

---
## Implementation Strategy
### MVP First (User Story 1 Only)
1. Complete Setup + Foundational (T001–T016)
2. Execute US1 tests (T017–T020) then create implementation (T021–T025)
3. Validate coverage & performance basic create latency
4. Deliver initial CLI (create + temporary list) as MVP

### Incremental Delivery
- Add listing (US2) enabling full visibility
- Add search (US3) for usability scaling
- Polish phase for hardening & performance

### Team Parallelization
- Developer A: Foundational repository + models (T007–T011)
- Developer B: CLI helpers & validation (T013–T016)
- Developer C: Services (T012 + later filtering/search) & tests
- After foundation: split user stories across developers using parallel test-first tasks.

---
## Notes
- [P] tasks = different files with no sequence dependency.
- All user story tasks labeled [US1]/[US2]/[US3].
- Atomic file writes implemented once in repository (avoid duplication).
- Coverage gates enforced before merging story phases.

