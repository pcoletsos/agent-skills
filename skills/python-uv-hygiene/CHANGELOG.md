# Changelog

## 0.1.0

- **Date**: 2026-05-24
- **Source Repos**: `creator-knowledge-pipeline`, `sbstck-dl`, `storage-strategist`
- **Reason for Change**: Extract standardized Python dependency and environment management procedures using the uv package manager into a reusable global skill.
- **Summary of Change**: Created the initial `0.1.0` draft of `python-uv-hygiene` defining standard sync workflows (`uv sync --frozen`), pyproject.toml conventions, dependency segregation, and local test validations.
- **Expected Behavior Change**: Pairing agents can deterministically setup and validate Python projects using uv.
- **Risk**: None. Starts in draft status.
