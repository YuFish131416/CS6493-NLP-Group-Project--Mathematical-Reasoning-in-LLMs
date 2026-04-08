# AGENT_STARTUP.md
> **This is your single entry point. Read this file completely before touching anything else.**
> Every session — new feature, iteration, or bug fix — begins here and follows the phases below in order. No skipping.

---

## 0. Directory Layout

```
project-root/
├── plan/                        # Compressed knowledge base — your long-term memory
│   ├── AGENT_STARTUP.md         # ← This file. Read first, always.
│   ├── PROJECT_OVERVIEW.md      # Goals / feature list / non-goals / acceptance criteria
│   ├── ARCHITECTURE.md          # Module map + key data flows (no internal logic)
│   ├── INTERFACES.md            # Every API / function signature + constraints  ← D-level
│   ├── SCHEMAS.md               # Every DB table + key struct, field-level detail ← D-level
│   ├── CONSTRAINTS.md           # Tech stack, version locks, compatibility rules
│   ├── DIR_MAP.md               # One-line purpose for every folder and key file
│   ├── ITERATION_LOG.md         # Structured log for Agent — file paths + change type
│   ├── CHANGELOG.md             # Narrative log for humans — why + impact
│   ├── API_CHANGELOG.md         # Contract diff for frontend/callers — Before/After
│   └── TECH_DEBT.md             # Known issues, shortcuts, and optimization candidates
│
├── process/
│   ├── PROGRESS.md              # Milestone-level checkboxes (coarse)
│   └── CURRENT_TASK.md          # Breakpoint-resume state (fine) — updated after every step
│
├── src/                         # Source code
├── tests/                       # Mirror structure of src/
├── docs/                        # External-facing documentation
├── review/                      # Per-iteration self code review outputs
│
├── config/
│   ├── config.example.yaml      # Committed template — no secrets
│   └── config.local.yaml        # Local secrets — gitignored
│
├── tmp/                         # All generated / debug / scratch files — gitignored
├── .env.example                 # Committed env template
├── .env                         # Local env — gitignored
└── .gitignore
```

---

## Phase 0 — Startup & Drift Detection

Run this every session before any other action.

### 0.1 Read plan/ in order
```
1. plan/AGENT_STARTUP.md          (you are here)
2. plan/PROJECT_OVERVIEW.md
3. plan/ARCHITECTURE.md
4. plan/INTERFACES.md
5. plan/SCHEMAS.md
6. plan/CONSTRAINTS.md
7. plan/DIR_MAP.md
8. process/CURRENT_TASK.md        ← determines whether this is a fresh start or a resume
```
After reading these eight files you should have sufficient context to work.
**Only open src/ files if plan/ is missing information you actively need.**

### 0.2 Drift Detection (human-change awareness)
Before proceeding, check for changes made outside your last session:
```
- Run: git status  (or compare file mtimes if git is unavailable)
- Identify any src/ changes not recorded in ITERATION_LOG.md
- If drift is found:
    [ ] List each drifted file and the apparent change
    [ ] Update INTERFACES.md / SCHEMAS.md if signatures or fields changed  [HARD GATE]
    [ ] Update ARCHITECTURE.md / DIR_MAP.md if structure changed            [soft]
    [ ] Append a drift entry to ITERATION_LOG.md:
        ## [DRIFT] <date>
        - <file> — detected external modification, plan/ updated
    [ ] Confirm with the user before continuing if the drift is large or ambiguous
```

### 0.3 Determine entry point
```
if process/CURRENT_TASK.md shows an in-progress task:
    → Resume from the last unchecked step. Do not re-run completed steps.
else:
    → Proceed to Phase 1 (first-time setup) or Phase 2 (new iteration).
```

---

## Phase 1 — First-Time Setup (run once per new project)

> Skip this phase entirely if plan/ files already exist and are populated.

Scan the entire project. While reading, **write immediately** — do not buffer until the end.

```
For each src/ file you read:
  → If it defines an API endpoint or exported function → append to INTERFACES.md
  → If it defines a DB table or key data structure    → append to SCHEMAS.md
  → If it reveals a module boundary or data flow      → update ARCHITECTURE.md
  → If it contains a hidden constraint, known bug,
    legacy quirk, or temporary workaround             → append to TECH_DEBT.md
  → If it is a config / env file                      → note in CONSTRAINTS.md, never copy secrets

Populate all plan/ files using the schemas defined in Section A below.
Populate process/PROGRESS.md with top-level milestones.
Leave process/CURRENT_TASK.md empty (no active task yet).
```

---

## Phase 2 — Planning (before writing any code)

> **Hard rule: no src/ modification until this phase is complete.**

```
[ ] Update plan/PROJECT_OVERVIEW.md
      — Goals, feature list (existing + new), non-goals, acceptance criteria

[ ] Update plan/ARCHITECTURE.md
      — Mark which modules are affected by this iteration

[ ] Update plan/CONSTRAINTS.md
      — Add any new compatibility constraints or version requirements

[ ] Compatibility check for every interface/schema touched:
      For each change:
        - Confirmed breaking  → must update, mark Breaking in API_CHANGELOG.md
        - Uncertain           → do NOT change, log risk in CONSTRAINTS.md
        - Confirmed safe      → proceed, no extra action required

[ ] Update process/PROGRESS.md
      — Add this iteration as a new milestone block, all steps [ ]

[ ] Write process/CURRENT_TASK.md (see schema in Section B)
      — Full step list, each with a unique ID
      — Set status: IN PROGRESS, last_completed: none
```

---

## Phase 3 — Implementation

Work through steps in `process/CURRENT_TASK.md` sequentially.

**After each step:**
```
[ ] Mark the step [x] in process/CURRENT_TASK.md
[ ] Update last_completed and next_step fields
[ ] If the step changed an interface signature or field  → update INTERFACES.md  [HARD GATE]
[ ] If the step changed a DB table or struct field       → update SCHEMAS.md     [HARD GATE]
[ ] If anything else noteworthy changed (arch, constraint, new debt) → update relevant plan/ file  [soft]
```

**Never batch plan/ updates.** Each step's documentation happens immediately after that step.

---

## Phase 4 — Testing

```
[ ] Run unit tests for every changed module
[ ] Run integration tests
[ ] Verify each acceptance criterion in PROJECT_OVERVIEW.md
[ ] Mark test steps [x] in process/CURRENT_TASK.md as they pass

If any test fails:
    fix → re-run → mark [x]
    Do not proceed to Phase 5 with failing tests.
```

---

## Phase 5 — Wrap-Up (run after all tests pass)

### 5.1 Self Code Review
```
[ ] Review all files changed in this iteration
[ ] Write review/REVIEW_<iteration-id>.md (see schema in Section C)
[ ] Append any new items found to plan/TECH_DEBT.md
```

### 5.2 Documentation finalization
```
[ ] Append to plan/ITERATION_LOG.md (machine-readable, see schema in Section D)
[ ] Append to plan/CHANGELOG.md (human-readable, see schema in Section D)
[ ] If any interface, response field, or schema changed → update plan/API_CHANGELOG.md (Section E)
[ ] Update plan/DIR_MAP.md if new files or folders were created
[ ] Mark this iteration [x] in process/PROGRESS.md
[ ] Set process/CURRENT_TASK.md status: COMPLETED
```

### 5.3 .gitignore Compliance Check
```
Verify .gitignore contains all of the following. Append any that are missing:
  tmp/
  .env
  *.local.*
  config/config.local.*
  *.log
  __pycache__/
  node_modules/
  dist/
  build/
```

---

## Section A — plan/ Document Schemas

### PROJECT_OVERVIEW.md
```markdown
## Goal
<one sentence>

## Feature List
### Existing
- [x] <feature>
### New (this iteration)
- [ ] <feature>

## Non-Goals
- <explicitly out of scope>

## Acceptance Criteria
- [ ] <measurable criterion>
```

### INTERFACES.md
```markdown
## <ModuleName>

### <FunctionName> | <METHOD /api/path>
- **Signature**: `func(param: Type, ...) -> ReturnType`
- **Description**: <one line>
- **Request fields**: `field: Type` — description
- **Response fields**: `field: Type` — description
- **Constraints**: [e.g. "userId must not be null", "returns 404 if not found"]
- **Side effects**: none | [list]
- **Last modified**: <iteration-id>
```

### SCHEMAS.md
```markdown
## <TableName> / <StructName>
| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| id    | UUID | NO       | gen     | PK         |       |

**Relations**: <TableA>.fieldX → <TableB>.fieldY
**Last modified**: <iteration-id>
```

### CONSTRAINTS.md
```markdown
## Stack
- Language: X vY.Z
- Framework: X vY.Z

## Compatibility Rules
- <rule> — reason

## Known Risks (do-not-touch)
- <file or interface> — <risk description> — added in <iteration-id>
```

### DIR_MAP.md
```markdown
| Path | Purpose |
|------|---------|
| src/module/ | <one line> |
```

### TECH_DEBT.md
```markdown
| ID | File | Description | Severity | Added | Resolution |
|----|------|-------------|----------|-------|------------|
| TD-001 | src/x.py | Hardcoded timeout | Medium | iter-3 | — |
```
Severity: Critical / High / Medium / Low

---

## Section B — process/CURRENT_TASK.md Schema
```markdown
## Task: <iteration-id> — <title>
**Status**: IN PROGRESS | COMPLETED | BLOCKED
**Last completed step**: <step-id> | none
**Next step**: <step-id>
**Blocked by**: <description> | none
**Started**: <date>

## Steps
- [x] S01 — <description>
- [ ] S02 — <description>
- [ ] S03 — <description> [HARD GATE: update INTERFACES.md after this step]
- [ ] S04 — <description> [HARD GATE: update SCHEMAS.md after this step]

## Test Steps
- [ ] T01 — unit test: <module>
- [ ] T02 — integration test: <scenario>
- [ ] T03 — verify acceptance criterion: <criterion>
```

---

## Section C — review/REVIEW_<iteration-id>.md Schema
```markdown
## Code Review: <iteration-id> — <date>

## Changed Files
| File | Change Type | Quality | Notes |
|------|-------------|---------|-------|
| src/x.py | Modified | Good | — |

## Architecture Assessment
<Does the change align with the existing architecture? Any violations?>

## New Tech Debt Introduced
| ID | File | Description | Severity |
|----|------|-------------|----------|

## Risks
<Any new risks introduced by this change?>
```

---

## Section D — Iteration Log Schemas

### ITERATION_LOG.md (Agent — structured)
```markdown
## [<iteration-id>] <title> — <date>
- MOD: src/path/file.ext — <what changed, one line>
- ADD: src/path/file.ext — <what it does>
- DEL: src/path/file.ext — <why removed>
- BREAKING: <interface or field> — <before → after>
```

### CHANGELOG.md (Human — narrative)
```markdown
## <version or iteration-id> — <date>
### What changed
<2–4 sentences: what was done and why>
### Impact
<Who is affected and how>
### Breaking changes
<None | description>
```

---

## Section E — API_CHANGELOG.md Schema
```markdown
## [<iteration-id>] — <date>

### Changed Endpoints
| Method | Path | Change Type |
|--------|------|-------------|
| GET | /api/teachers/:id/courses | Response structure changed |

### Request / Response Diff

#### GET /api/teachers/:id/courses
**Before**
{ "course": { "id": 1, "name": "Math" } }

**After**
{ "courses": [{ "id": 1, "name": "Math" }, { "id": 2, "name": "Physics" }] }

⚠️ Breaking Change: field renamed `course` → `courses`, type changed object → array.

### Schema Diff
| Table | Field | Change |
|-------|-------|--------|
| teacher_courses | teacher_id | UNIQUE constraint removed |

### Migration Guide
<Step-by-step instructions for callers to migrate>
```

---

## Hard Rules

```
✗ Never modify src/ before Phase 2 is complete
✗ Never batch plan/ updates — write immediately after each step
✗ Never leave INTERFACES.md or SCHEMAS.md stale after a hard-gate step
✗ Never commit .env / config.local.* / tmp/ contents
✗ Never read, write, or modify anything inside .git/
✗ Never skip failing tests and proceed to Phase 5
✗ Never change an interface when compatibility impact is uncertain — log the risk instead
```

---

## Pre-Commit Checklist

```
[ ] process/CURRENT_TASK.md status = COMPLETED, all steps [x]
[ ] plan/INTERFACES.md reflects current signatures
[ ] plan/SCHEMAS.md reflects current field structure
[ ] plan/ITERATION_LOG.md has an entry for this iteration
[ ] plan/CHANGELOG.md has an entry for this iteration
[ ] plan/API_CHANGELOG.md updated (if any interface/schema changed)
[ ] review/REVIEW_<iteration-id>.md written
[ ] plan/TECH_DEBT.md updated
[ ] .gitignore compliance check passed
[ ] All tests green
```
