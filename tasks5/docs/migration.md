# Migration Outline: JSON to SQLite / Neo4J

## Current State
- Persistence in `tasks.json` with structure: `{ "schema_version": 1, "tasks": [ {id,title,description,status}, ...] }`
- Access via `JsonTaskRepository` (`load_all_tasks`, `save_new_task`).
- Repository abstraction isolates CLI & services from storage.

## Goals
1. Switch storage without changing CLI command contracts or services logic.
2. Preserve task IDs and statuses.
3. Enable future performance improvements (indexes, queries).

## SQLite Migration Steps
1. Add dependency (e.g., `sqlite3` standard lib or `SQLAlchemy` if justified).
2. Create new repository `SqlTaskRepository` implementing:
   - `load_all_tasks() -> List[Task]`
   - `save_new_task(task: Task) -> None`
3. Schema: Table `tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT NULL, status TEXT NOT NULL)`.
4. Write migration script:
   ```python
   import json, sqlite3
   data = json.load(open('tasks.json'))
   conn = sqlite3.connect('tasks.db'); cur = conn.cursor()
   cur.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, description TEXT, status TEXT)')
   for t in data['tasks']:
       cur.execute('INSERT INTO tasks(id,title,description,status) VALUES(?,?,?,?)', (t['id'], t['title'], t['description'], t['status']))
   conn.commit()
   ```
5. Replace import in CLI entrypoint or a factory method to return `SqlTaskRepository`.
6. Add indexes if needed: `CREATE INDEX idx_tasks_status ON tasks(status); CREATE INDEX idx_tasks_title ON tasks(title);`

## Neo4J Migration Steps
1. Add driver dependency (neo4j Python driver).
2. Create `Neo4jTaskRepository` with same public methods.
3. Graph model:
   - Node label: `Task`
   - Properties: `id`, `title`, `description`, `status`.
4. Insertion Cypher:
   `CREATE (t:Task {id: $id, title: $title, description: $description, status: $status})`
5. Load all tasks:
   `MATCH (t:Task) RETURN t.id AS id, t.title AS title, t.description AS description, t.status AS status ORDER BY t.id`
6. Indexes:
   - `CREATE INDEX task_id IF NOT EXISTS FOR (t:Task) ON (t.id)`
   - `CREATE INDEX task_title IF NOT EXISTS FOR (t:Task) ON (t.title)`

## Repository Switch Mechanism
Use a factory:
```python
from src.repository.json_repository import JsonTaskRepository
# from src.repository.sql_repository import SqlTaskRepository  # future

def get_repository():
    return JsonTaskRepository()  # swap here only
```
CLI commands call `get_repository()` instead of direct constructor.

## Validation After Migration
- Run full test suite against new repository.
- Confirm performance benchmarks meet targets (<300ms list/search for 5k tasks).
- Ensure `schema_version` handling updated if schema changes.

## Rollback Strategy
Retain original `tasks.json` backup until migration validated. Provide script to rehydrate JSON from DB if needed.

## Future Considerations
- Add search optimization (LIKE or FTS in SQLite; full-text index in Neo4J or external search engine).
- Handle concurrent writes via DB transactions.
