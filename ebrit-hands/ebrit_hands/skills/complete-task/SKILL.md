---
name: complete-task
triggers:
- complete-task
---

Complete the task described by the provided inputs. The project is located at `/workspace/project`.

## Inputs

- **Title**: short name of the task
- **Description**: full description of what needs to be done

## Edge cases

- If description is empty, evaluate whether the title alone is specific enough to act on (e.g. "Fix null pointer in UserService" is sufficient; "Improve code" is not).
- If the title is not actionable on its own, do not attempt the task — respond explaining that a description is required.
