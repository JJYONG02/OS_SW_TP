# Git Flow Guide

## Branch Structure

This project uses a simple Git Flow style for team collaboration.

```text
main
- Stable branch
- Do not work directly on this branch
- Merge only completed and tested code

develop
- Integration branch for development
- Feature branches are merged here first

feature/db-docker
- DB design and Docker environment
- Owner: 재현

feature/auth-board
- Authentication and board APIs
- Owner: 태규

feature/chat
- Chat rooms and real-time messages
- Owner: 재용

feature/frontend
- Frontend screens and API integration
- Owner: frontend team
```

## Why Develop Exists

`develop` is the integration branch. Backend and frontend developers should not work directly on `develop`, but they should merge completed feature work into it through Pull Requests.

This lets the team test whether separate features work together before merging into `main`.

```text
feature/db-docker -> develop
feature/auth-board -> develop
feature/chat -> develop
feature/frontend -> develop

develop -> main
```

## Working Rules

1. Start work from your assigned feature branch.
2. Commit small changes with clear messages.
3. Push your branch to GitHub.
4. Open a Pull Request into `develop`.
5. Review before merging.
6. Merge `develop` into `main` only when the first milestone is complete.

## Commit Message Examples

```text
feat: add login api
feat: create post entity
feat: add docker compose for database
feat: add frontend board page
fix: resolve database connection error
docs: update api specification
chore: update project settings
```

## First Milestone Scope

The first milestone focuses on the minimum backend required for frontend integration.

```text
- Sign up
- Login
- Board post create/read/update/delete
- Chat room list
- Chat room enter
- Real-time message send/receive
- Message persistence
- Frontend API integration
```

Features such as payment, notification, image upload, and read receipts are planned for later milestones.
