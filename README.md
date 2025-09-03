# 🐜 Ant PR: "Small Pull Requests are Beautiful"

**A GitHub Action that champions the philosophy of small, incremental changes by keeping your pull requests tiny and manageable.**

Just like a colony of ants working together with small, consistent efforts to build something great, this action helps your team maintain a healthy and efficient development workflow.

---

## ✨ Why Small Pull Requests?

Smaller pull requests are:

- **✅ Easier & Faster to Review:** Less code means quicker, more thorough reviews.
- **🐛 Easier to Debug:** Pinpoint issues with surgical precision.
- **🚀 Deployed Faster:** Small changes merge smoothly into the main branch.
- **🧘 Less Stressful:** Reduce the mental load for both authors and reviewers.

Ant PR helps you enforce this best practice automatically.

## 🚀 Getting Started

Integrate Ant PR into your workflow in seconds.

### 1. Create the Workflow

Create a workflow file (e.g., `.github/workflows/ant-pr.yml`) with the following content. This workflow ensures that the action has the necessary information to compare file changes.

```yaml:ant-pr.yml
name: Ant PR

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches-ignore:
      - "main"

permissions:
  pull-requests: write

jobs:
  ant-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run ant-pr
        uses: qkitzero/ant-pr@v1.3.0
        with:
          config-path: ".ant-pr.yml"
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Configure Limits

Create a `.ant-pr.yml` file in your repository to define limits for line changes and the total number of changed files.

If this file is not present, the action will still run, but no limits will be enforced.

```yaml:.ant-pr.yml
limits:
  files: 15 # Limit the total number of changed files in a PR.
  lines: # Define line change limits for different parts of your codebase.
    "frontend/": 200
    "backend/": 200
    "docs/": 300
```

That's it! Ant PR will now check new pull requests and add a comment if they exceed the defined limits.
