---
name: service-onboarding
description: Procedures for safely and consistently onboarding new services or microservices into a software stack.
version: 0.1.0
status: draft
---

# Service Onboarding

## Purpose
Safely, consistently, and securely onboard a new service, microservice, or workload into an active development workspace or cluster. This checklist prevents deployment gaps where services are configured but unreachable, undocumented, or unmonitored.

## Use When
- A user requests: "Onboard a new service," "Add a microservice," "Configure a new deployment," or "Set up this workload."
- You need a structured operational path for deploying, exposing, monitoring, and documenting a new codebase component.

## Do Not Use When
- Simply updating an existing service or deploying a hotfix (use regular Git flows).
- The service onboarding is highly platform-specific and has its own custom pipeline outside standard code rules.
- Writing code logic for a single feature without any new container, network, or server placement requirements.

## Inputs To Check
- Existing repository maps (`AGENTS.md`, `README.md`).
- Configurations and secrets directories or templates (`.env.example`, `config/`).
- Documentation directories containing runbooks, deployment guides, or architecture diagrams.
- Active cluster configuration folders or GitOps paths (e.g., Kubernetes manifests, Docker Compose files).

## Procedure
1.  **Define Packaging and Placement**:
    *   Inspect runtime options (e.g. Docker, Kubernetes, host-side systemd, bare-metal).
    *   Draft clean configuration templates (`.env.example` or equivalent configuration templates) ensuring all credentials and secrets are marked for runtime-only injection.
    *   Never commit production credentials, passwords, or keys to Git.
2.  **Define Ingress and Access**:
    *   Determine the ingress endpoint (e.g., path route `host/path` or subdomain `service.domain`).
    *   Establish local DNS, proxy/load-balancer configurations, or ingress manifests.
    *   Provide simple verification instructions (e.g. DNS lookups, curl tests) to test connection bounds.
3.  **Establish Monitoring Baseline**:
    *   Configure basic health-check probes, endpoint availability checks, or blackbox probes.
    *   Draft downtime alert notifications or routing criteria.
    *   Identify log management and observability paths.
4.  **Document and Curate Operations**:
    *   Update codebase service lists, active runtime registers, and host-bound ports.
    *   Add service orientation diagrams, visual topologies, or operations runbooks to documentation.
    *   Add a local changelog or work log entry noting the new service presence.

## Output Format
Render a clean Markdown service onboarding report:
```markdown
# Service Onboarding Report

## ⚙️ Service Orientation
- **Name**: [Service Name]
- **Runtime Placement**: [Kubernetes / Docker Compose / Bare Metal / host systemd]
- **Target Ingress**: [subdomain.domain or domain/path]

## 🛠 Manifests & Configurations
- [ ] Placement definition configured under `[path]`
- [ ] `.env.example` or equivalent templates present
- [ ] Secrets separated from source code repositories

## 🔌 Ingress & Access
- [ ] Local/Global DNS routes defined
- [ ] Ingress/Proxy configuration verified
- [ ] HTTPS certificates active and verified

## 📊 Observability & Probes
- [ ] Health-check endpoint/blackbox probe configured
- [ ] Downtime alerts active
- [ ] Log outputs visible in monitoring dashboard

## 🛑 Operational Hand-off
- [ ] Service inventory updated in `[path]`
- [ ] Runtime-memory log updated
- [ ] Diagnostics runbook created under `[path]`
```

## Rules
- **NEVER** commit production/live credentials, API keys, or raw secrets to any git repository.
- Ensure that every new service has a documented health check or probe endpoint.
- Keep local infrastructure boundaries cleanly mapped out in repository-local config/runbook docs.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
