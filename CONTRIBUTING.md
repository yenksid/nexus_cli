# Contributing to Nexus CLI 🌌

Thank you for your interest in improving Nexus CLI! To maintain high standards as an "Automation Intelligent Architect," please follow these guidelines.

## 📝 Conventional Commits
We use **Conventional Commits** to automate our changelog and versioning. Your commit messages must follow this format:

- `feat:` for new features (triggers a Minor version).
- `fix:` for bug fixes (triggers a Patch version).
- `docs:` for documentation changes.
- `refactor:` for code changes that neither fix a bug nor add a feature.

Example: `feat: integrate OpenRAG for codebase indexing`

## 🛠️ Issue-Driven Development
1. Every change must be linked to an **Issue**.
2. Issues must include: Context, Objective, Tasks, and Criteria for Approval.
3. Do not start working on a task until the Issue is approved.

## 🧪 Testing
All contributions must pass the E2E test suite:
```bash
python tests/run_tests.py