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

permissions:
  pull-requests: write

jobs:
  ant-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5

      - name: Run ant-pr
        uses: qkitzero/ant-pr@v1.0.1
        with:
          base-sha: ${{ github.event.pull_request.base.sha }}
          head-sha: ${{ github.event.pull_request.head.sha }}
          config-path: ".github/workflows/.ant-pr.yml"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          repository: ${{ github.repository }}
          pull-request-number: ${{ github.event.pull_request.number }}

```

### 2. Configure Line Limits (Optional)

Create a `.ant-pr.yml` file to define line change limits for different parts of your codebase.

```yaml:.ant-pr.yml
rules:
  "frontend/": 100
  "api/": 150
  "docs/": 200
  "": 50 # Default
```

That's it! Ant PR will now check new pull requests and add a comment if they exceed the defined limits.
