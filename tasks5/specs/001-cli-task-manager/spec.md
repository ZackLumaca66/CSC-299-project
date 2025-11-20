# Feature Specification: CLI Task Manager MVP

**Feature Branch**: `001-cli-task-manager`  
**Created**: 2025-11-19  
**Status**: Draft  
**Input**: User description: "Build a CLI task manager that allows creating, listing, searching tasks. Each task has id, title, optional description, and status (todo, in-progress, done). Persist tasks in JSON file tasks.json. Support search by substring. Focus on initial MVP; no user auth. Provide sample tasks. Include non-functional requirements: performance adequate for <5k tasks, easy future switch to SQLite or Neo4J, and testability."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Task (Priority: P1)
User adds a new task providing a title (required) and optionally a description; task stored with a unique id and default status `todo` unless explicitly set to one of the allowed statuses.

**Why this priority**: Creation is the foundational capability; without tasks other actions have no value.

**Independent Test**: Invoke CLI create command with minimal and full inputs; verify task appears in persistence and returned in list/search operations.

**Acceptance Scenarios**:
1. **Given** an empty task store, **When** user creates a task with title "Write spec", **Then** system assigns unique id and persists task with status `todo`.
2. **Given** existing tasks, **When** user creates a task with title and description and status `in-progress`, **Then** task is persisted with provided status and retrievable via list.
3. **Given** existing tasks, **When** user attempts creation with blank title, **Then** system rejects with clear error message and non-zero exit code.

---

### User Story 2 - List Tasks (Priority: P2)
User lists all tasks to view id, title, status (and description optionally). Supports optional filtering by status.

**Why this priority**: Listing enables visibility and is core to interacting with stored tasks after creation.

**Independent Test**: Invoke list command before and after creating tasks; verify output formatting and optional status filter behavior.

**Acceptance Scenarios**:
1. **Given** several tasks in different statuses, **When** user runs list, **Then** all tasks are displayed with correct fields.
2. **Given** tasks with mixed statuses, **When** user runs list with status filter `done`, **Then** only tasks whose status is `done` are shown.

---

### User Story 3 - Search Tasks (Priority: P3)
User searches tasks by providing a substring; matches on title and description (case-insensitive). Returns matching tasks.

**Why this priority**: Search improves usability for larger sets (<5k) enabling quick retrieval.

**Independent Test**: Create sample tasks; run search with varying casing and partial strings; verify returned subset correctness.

**Acceptance Scenarios**:
1. **Given** tasks including title "Write spec" and description "Initial MVP", **When** user searches substring "spec", **Then** matching task returned.
2. **Given** tasks, **When** user searches substring with no matches, **Then** system returns empty result (no error) and indicates zero matches.
3. **Given** tasks, **When** user searches with mixed case substring, **Then** matches are evaluated case-insensitively.

---

### Edge Cases
- Creating task with excessively long title (>256 chars) → validation error.
- Creating task with unsupported status value → validation error listing allowed statuses.
- Listing when no tasks exist → outputs informative "no tasks" message (or empty JSON array in JSON mode).
- Search substring is empty → returns error instructing to provide non-empty query.
- tasks.json missing/corrupted (invalid JSON) → system attempts safe recovery: backup corrupt file and start fresh store with warning.
- Concurrent modifications (multi-process) → Out of scope for MVP (Assumption: single-process usage).
- Atomic persistence failure (disk full) → returns error; no partial file persisted.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST allow creating a task with required title and optional description and optional provided status.
- **FR-002**: System MUST assign a unique integer id sequentially starting at 1.
- **FR-003**: System MUST persist tasks to a JSON file `tasks.json` using an atomic write strategy (no partial/corrupt writes) and include a `schema_version` field.
- **FR-004**: System MUST allow listing all tasks with id, title, status, and optionally description.
- **FR-005**: System MUST allow filtering list output by status (`todo`, `in-progress`, `done`).
- **FR-006**: System MUST perform case-insensitive substring search over title and description and return matching tasks.
- **FR-007**: System MUST validate status against allowed set and reject invalid values with clear error message.
- **FR-008**: System MUST provide both human-readable and `--json` structured outputs for create, list, search operations.
- **FR-009**: System MUST initialize storage if `tasks.json` does not exist (creating empty task collection with `schema_version`).
- **FR-010**: System MUST handle corrupted `tasks.json` by backing up (rename with timestamp) and starting with empty store while reporting error.
- **FR-011**: System MUST load sample tasks via an optional initialization flag (e.g., `--seed`) to assist testing/demo.
- **FR-012**: System MUST reject creation attempts with blank or whitespace-only title.
- **FR-013**: System MUST support status defaulting to `todo` when not provided.
- **FR-014**: System MUST return non-zero exit codes on validation or persistence errors.
- **FR-015**: System MUST maintain separation of concerns: CLI layer (interaction), repository layer (persistence), model layer (domain validation) as per constitution.

### Key Entities *(include if feature involves data)*
- **Task**: Represents a unit of work. Attributes: `id` (int), `title` (string), `description` (optional string), `status` (enum: todo|in-progress|done).
- **Task Repository**: Abstract persistence boundary responsible for loading, saving, and atomic write operations; hides JSON details from other layers.
- **Task Collection**: In-memory representation (list) enabling search, filtering, and id assignment logic.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Users can create a task and see it in list within <1 second on typical workstation.
- **SC-002**: Listing all tasks (≤5,000) completes in <300ms median time.
- **SC-003**: Substring search on ≤5,000 tasks returns results in <300ms median time.
- **SC-004**: Task creation validation errors are reported with explicit messages (100% of invalid attempts). 
- **SC-005**: Atomic persistence ensures zero occurrences of partial or corrupted writes under normal operation (verified via fault injection tests).
- **SC-006**: Test coverage for new modules ≥90% line and ≥85% branch; global coverage does not drop below 85% line.
- **SC-007**: Extensibility demonstrated by a documented migration outline to alternate storage (e.g., relational or graph) without changing CLI contract.
- **SC-008**: JSON output for list and search is valid and parsable (100% runs in test suite).

## Assumptions
- Single-user, single-process execution (no concurrent writes).
- Case-insensitive matching uses Unicode simple case folding.
- Id generation is sequential and not recycled after deletions (future deletion out of scope).
- Ordering of list defaults to ascending id.
- Maximum practical tasks in MVP is 5,000; performance targets scoped accordingly.

## Out of Scope
- Updating or deleting tasks.
- Advanced filtering (date ranges, tags, statuses combinations).
- User authentication or multi-user concurrency controls.
- Rich query language or pagination.
- Persistent indexing for search.

## Risks
- Corruption handling might hide underlying disk issues—clear warning messaging required.
- Sequential id strategy limits future sharding (acceptable for MVP scale).
- Single JSON file may become bottleneck beyond 5k tasks—migration plan needed early.

## Migration & Extensibility Notes
- Repository abstraction enables future replacement with SQLite or Neo4J maintaining same CLI contract.
- `schema_version` supports incremental evolution; migration script required for any incompatible structure changes.

