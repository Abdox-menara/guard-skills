# Agent Memory - Persistent Project Knowledge

> **Last Updated**: 2026-08-22 | **Session**: memory-improvement
> **Project**: Guard Skills | **Location**: C:\opencodes\guard skills
> **Auto-Sync**: Verified 2026-08-23 against filesystem (226 skills)

---

## 1. Project Overview

| Field | Value |
|-------|-------|
| Name | Guard Skills |
| Type | Skills repository for coding agents |
| Total Skills | 226 (72 guards, 86 tools, 68 workflow) |
| Root | `C:\opencodes\guard skills` |
| Skills Dir | `C:\opencodes\guard skills\skills\` |
| Last Verified | 2026-08-22 18:02 UTC+1 — filesystem counts match header |

## 2. User Profile

| Preference | Value |
|------------|-------|
| Language | English |
| Communication | Direct, concise |
| Style | Action over explanation |
| Browser | Brave (not Chrome) |
| Desktop MCP | Ghost (`ghost do "..."`) |
| Model (daily) | `opencode/deepseek-v4-flash-free` |
| Model (cheap) | `opencode/nemotron-3-ultra-free` |
| Model (vision) | `openrouter/nvidia/nemotron-nano-12b-v2-vl:free` |

## 3. All Projects (C:\opencodes) — Verified 2026-08-22

### Main Projects
| Project | Files | Description |
|---------|-------|-------------|
| guard skills | 52053* | Guard skills for coding agents (*incl. node_modules/cache) |
| automation | 7525 | OpenCode Automation Suite - OCR, PDF, folder watching, screenshots |
| instrumentation-list | 13910 | Analysis tooling for 19094-02 Instrumentation List |
| office expert | 3534 | Office expert tools |
| agents | 102 | 100 agents auto-mode orchestrators |
| OPENCODE IMPROVEMENT | 415 | Self-learning stack that persists state |
| tools | 294 | Skeleton Tool Generator - 80 skeleton tools (PS1) + BAT wrappers |
| tests | 156 | Test files |
| reports | 137 | Report files |
| scripts | 108 | Script files |

### PC/Diagnostic
| Project | Files | Description |
|---------|-------|-------------|
| PC DIAGNOSTIQUE | 3735* | 100-Point Windows Optimization Suite for Windows 11 (*was 65, growth 2026-07-28) |
| plc | 15429* | PLC tools (ABB conductivity flowcell simulator) (*incl. deps) |

### EPLAN/Engineering
| Project | Files | Description |
|---------|-------|-------------|
| Eplan | 9 | VEGAMET 141 EPLAN Symbol Package |
| Eplan_Symbol | 11 | EPLAN symbols |
| disgnodtique-autocad | 20 | Automotive Electrical Diagnostic System |

### Knowledge/Base
| Project | Files | Description |
|---------|-------|-------------|
| knowledge-base | 15 | Read-only documentation snapshots |
| problems | 22 | Problem-Solution Knowledge Base |
| improvement_report | 16 | Improvement reports |

### Life/Planning
| Project | Files | Description |
|---------|-------|-------------|
| LIFE-OS | 41 | Complete life planning system - 100% local, Markdown + PowerShell |

### OCR/Processing
| Project | Files | Description |
|---------|-------|-------------|
| OCR | 13 | OCR tools |
| opencode-custom | - | Custom opencode configuration |

### Other
| Project | Files | Description |
|---------|-------|-------------|
| opencodes | 47 | Main opencodes repository |
| opencodes-assistant-0.2.0 | 589 | OpenCode assistant package |
| ErrorReports | 3 | Error report files |
| office | 22 | Office files |
| plugins | 3 | Plugin files |
| shared-skills | 17 | Shared skill definitions |
| skills | 15 | Additional skills |

### Empty/Inactive
- KB-Invoice-Generator, KB-Invoice-Generator-New, openmythos, aguseron, aigent

> **Note**: File counts with * include dependencies (node_modules, __pycache__, .git). Clean counts available via `Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch "node_modules|__pycache__|\.git" }`

---

## 4. Skill Index (223 Skills — Verified 2026-08-22)

> Auto-generated from filesystem. Run `Get-ChildItem skills/*/ -Directory | Measure-Object` to re-verify. Do not hand-edit; regenerate.

### Guards (72) — Quality Gates & Validation
| Skill | Purpose |
|-------|---------|
| analytics-guard | ULTRA-ADVANCED analytics guard - Analytics implementation v... |
| api-contract-guard | ULTRA-ADVANCED Api Contract Guard - API contract compliance... |
| api-security-guard | ULTRA-ADVANCED Api Security Guard - API security validation... |
| async-guard | ULTRA-ADVANCED Async Guard - Async/await pattern validation... |
| build-guard | ULTRA-ADVANCED build guard - Build process validation and c... |
| changelog-guard | ULTRA-ADVANCED changelog guard - Changelog format validatio... |
| ci-guard | ULTRA-ADVANCED ci guard - CI/CD pipeline configuration vali... |
| circuit-breaker-guard | ULTRA-ADVANCED Circuit Breaker Guard - Circuit breaker patt... |
| clean-arch-guard | ULTRA-ADVANCED Clean Arch Guard - Clean architecture layer ... |
| clean-code-guard | ULTRA-ADVANCED Clean Code Guard with automated code analysi... |
| comment-guard | ULTRA-ADVANCED Comment Guard - Comment quality validation -... |
| commit-guard | ULTRA-ADVANCED commit guard - Commit message convention val... |
| concurrency-guard | ULTRA-ADVANCED concurrency guard - Concurrency/threading sa... |
| config-guard | ULTRA-ADVANCED config guard - Configuration file validation... |
| cors-guard | ULTRA-ADVANCED Cors Guard - CORS configuration validation a... |
| cqrs-guard | ULTRA-ADVANCED Cqrs Guard - CQRS pattern validation - comma... |
| csrf-guard | ULTRA-ADVANCED Csrf Guard - CSRF protection validation - an... |
| css-guard | ULTRA-ADVANCED css guard - CSS/Sass best practices, specifi... |
| cyclomatic-guard | ULTRA-ADVANCED Cyclomatic Guard - Cyclomatic complexity val... |
| ddd-guard | ULTRA-ADVANCED Ddd Guard - Domain-driven design validation ... |
| dead-code-guard | ULTRA-ADVANCED Dead Code Guard - Dead code detection - unus... |
| dependency-injection-guard | ULTRA-ADVANCED Dependency Injection Guard - DI/IoC validati... |
| deploy-guard | ULTRA-ADVANCED deploy guard - Deployment safety validation ... |
| desktop-control-mcp | ULTRA-ADVANCED Desktop Control MCP — Windows automation server |
| docker-compose-guard | ULTRA-ADVANCED docker compose guard - Docker Compose valida... |
| docker-guard | ULTRA-ADVANCED docker guard - Dockerfile optimization, secu... |
| docs-guard | ULTRA-ADVANCED Docs Guard with automated documentation anal... |
| duplicate-code-guard | ULTRA-ADVANCED Duplicate Code Guard - Code duplication dete... |
| encryption-guard | ULTRA-ADVANCED Encryption Guard - Encryption best practices... |
| env-check-guard | ULTRA-ADVANCED env check guard - Environment variable valid... |
| error-handling-guard | ULTRA-ADVANCED error handling guard - Error handling patter... |
| event-driven-guard | ULTRA-ADVANCED Event Driven Guard - Event-driven architectu... |
| event-sourcing-guard | ULTRA-ADVANCED Event Sourcing Guard - Event sourcing patter... |
| file-guard | ULTRA-ADVANCED file guard - File system security, path trav... |
| graceful-shutdown-guard | ULTRA-ADVANCED Graceful Shutdown Guard - Graceful shutdown ... |
| health-check-guard | ULTRA-ADVANCED Health Check Guard - Health check endpoint v... |
| helm-guard | ULTRA-ADVANCED helm guard - Helm chart validation, template... |
| hexagonal-guard | ULTRA-ADVANCED Hexagonal Guard - Hexagonal/ports-and-adapte... |
| html-guard | ULTRA-ADVANCED html guard - HTML semantics, accessibility c... |
| iam-guard | ULTRA-ADVANCED Iam Guard - IAM policy validation - least pr... |
| idor-guard | ULTRA-ADVANCED Idor Guard - Insecure Direct Object Referenc... |
| injection-guard | ULTRA-ADVANCED Injection Guard - Injection prevention valid... |
| json-guard | ULTRA-ADVANCED json guard - JSON schema validation, structu... |
| jwt-guard | ULTRA-ADVANCED Jwt Guard - JWT implementation validation - ... |
| kubernetes-guard | ULTRA-ADVANCED kubernetes guard - Kubernetes manifest valid... |
| large-class-guard | ULTRA-ADVANCED Large Class Guard - Large class detection - ... |
| logging-pattern-guard | ULTRA-ADVANCED Logging Pattern Guard - Logging patterns - s... |
| long-method-guard | ULTRA-ADVANCED Long Method Guard - Long method detection - ... |
| lsp-guard | ULTRA-ADVANCED LSP Guard - Language Server Protocol auto-de... |
| markdown-guard | ULTRA-ADVANCED markdown guard - Markdown quality, consisten... |
| message-queue-guard | ULTRA-ADVANCED Message Queue Guard - Message queue validati... |
| migration-pattern-guard | ULTRA-ADVANCED Migration Pattern Guard - Database migration... |
| naming-guard | ULTRA-ADVANCED Naming Guard - Naming convention validation ... |
| nested-depth-guard | ULTRA-ADVANCED Nested Depth Guard - Nesting depth validatio... |
| observer-pattern-guard | ULTRA-ADVANCED Observer Pattern Guard - Observer/event patt... |
| pr-guard | ULTRA-ADVANCED pr guard - Pull request template validation,... |
| python-guard | ULTRA-ADVANCED python guard - Python best practices, PEP 8 ... |
| react-guard | ULTRA-ADVANCED react guard - React best practices, hooks ru... |
| readme-guard | ULTRA-ADVANCED readme guard - README completeness, installa... |
| repository-pattern-guard | ULTRA-ADVANCED Repository Pattern Guard - Repository patter... |
| responsive-guard | ULTRA-ADVANCED responsive guard - Responsive design validat... |
| retry-guard | ULTRA-ADVANCED Retry Guard - Retry pattern validation - exp... |
| saga-guard | ULTRA-ADVANCED Saga Guard - Saga/choreography pattern valid... |
| seo-guard | ULTRA-ADVANCED seo guard - SEO validation, meta tags, struc... |
| serialization-guard | ULTRA-ADVANCED serialization guard - Serialization/deserial... |
| ssrf-guard | ULTRA-ADVANCED Ssrf Guard - Server-side request forgery pre... |
| state-guard | ULTRA-ADVANCED state guard - State management validation an... |
| strategy-pattern-guard | ULTRA-ADVANCED Strategy Pattern Guard - Strategy pattern va... |
| terraform-guard | ULTRA-ADVANCED terraform guard - Terraform configuration va... |
| test-guard | ULTRA-ADVANCED Test Guard with automated test analysis, cov... |
| typescript-guard | ULTRA-ADVANCED typescript guard - TypeScript best practices... |
| xss-guard | ULTRA-ADVANCED Xss Guard - XSS prevention validation - outp... |
| yaml-guard | ULTRA-ADVANCED yaml guard - YAML validation, formatting con... |


### Tools (83) — Infrastructure & Utilities
| Skill | Purpose |
|-------|---------|
| accessibility-patterns | ULTRA-ADVANCED Accessibility Patterns - Accessibility patte... |
| alerting-stack | ULTRA-ADVANCED Alerting Stack - Alerting stack - rules, rou... |
| analytics | ULTRA-ADVANCED analytics - Analytics implementation, event ... |
| analytics-setup | ULTRA-ADVANCED Analytics Setup - Analytics implementation -... |
| api-documentation | ULTRA-ADVANCED Api Documentation - API documentation - Open... |
| api-rate-limiting | ULTRA-ADVANCED Api Rate Limiting - API rate limiting - algo... |
| api-versioning | ULTRA-ADVANCED Api Versioning - API versioning strategy - U... |
| audio-processing | ULTRA-ADVANCED audio processing - Audio processing, speech ... |
| backup-strategy | ULTRA-ADVANCED Backup Strategy - Backup strategy - frequenc... |
| batch-processing | ULTRA-ADVANCED batch processing - Batch processing workflow... |
| cache-strategy | ULTRA-ADVANCED Cache Strategy - Cache strategy - TTL, inval... |
| capacity-management | ULTRA-ADVANCED Capacity Management - Capacity management - ... |
| cdn | ULTRA-ADVANCED cdn - CDN configuration, edge caching, and c... |
| cdn-strategy | ULTRA-ADVANCED Cdn Strategy - CDN strategy - edge caching, ... |
| cicd-pipeline | ULTRA-ADVANCED Cicd Pipeline - CI/CD pipeline design - stag... |
| component-library | ULTRA-ADVANCED component library - Component library manage... |
| computer-vision | ULTRA-ADVANCED computer vision - Computer vision, object de... |
| container-patterns | ULTRA-ADVANCED Container Patterns - Container/Docker patter... |
| content-strategy | ULTRA-ADVANCED content strategy - Content strategy, editori... |
| contract-testing | ULTRA-ADVANCED Contract Testing - Contract testing - consum... |
| data-management | ULTRA-ADVANCED Data Management - Data management - lifecycl... |
| data-quality | ULTRA-ADVANCED Data Quality - Data quality framework - vali... |
| data-warehouse | ULTRA-ADVANCED data warehouse - Data warehouse design, star... |
| database-optimization | ULTRA-ADVANCED Database Optimization - Database optimizatio... |
| database-scaling | ULTRA-ADVANCED Database Scaling - Database scaling strategy... |
| design-system | ULTRA-ADVANCED Design System - Design system creation - com... |
| force-delete | ULTRA-ADVANCED Force Delete & Disk Cleanup — protected folder removal, takeown+icacls, drive analysis |
| ecommerce | ULTRA-ADVANCED ecommerce - E-commerce platform design, prod... |
| email-systems | ULTRA-ADVANCED email systems - Email service design, transa... |
| error-boundary-patterns | ULTRA-ADVANCED Error Boundary Patterns - Error boundary pat... |
| etl | ULTRA-ADVANCED etl - ETL pipeline design, data transformati... |
| feature-flag-strategy | ULTRA-ADVANCED Feature Flag Strategy - Feature flag strateg... |
| freebuff-bridge | ULTRA-ADVANCED Freebuff Bridge — Communicate with Freebuff ... |
| full-text-search | ULTRA-ADVANCED full text search - Full-text search implemen... |
| graph-database | ULTRA-ADVANCED graph database - Graph database design, quer... |
| grpc | ULTRA-ADVANCED grpc - gRPC API design, protobuf definition,... |
| image-optimization | ULTRA-ADVANCED Image Optimization - Image optimization - fo... |
| image-processing | ULTRA-ADVANCED image processing - Image processing pipeline... |
| incident-management | ULTRA-ADVANCED Incident Management - Incident management - ... |
| index-design | ULTRA-ADVANCED Index Design - Index strategy - B-tree, hash... |
| information-architecture | ULTRA-ADVANCED information architecture - Information archi... |
| input-blocker | — |
| logging-patterns | ULTRA-ADVANCED Logging Patterns - Logging patterns - struct... |
| logging-stack | ULTRA-ADVANCED Logging Stack - Logging stack design - colle... |
| makefile | ULTRA-ADVANCED Makefile - Makefile best practices - phony t... |
| mfa | ULTRA-ADVANCED mfa - Multi-factor authentication design, TO... |
| microservice-patterns | ULTRA-ADVANCED Microservice Patterns - Microservice pattern... |
| monitoring-stack | ULTRA-ADVANCED Monitoring Stack - Monitoring stack design -... |
| nlp | ULTRA-ADVANCED nlp - Natural language processing, text anal... |
| nosql | ULTRA-ADVANCED nosql - NoSQL database design, document stor... |
| notification | ULTRA-ADVANCED notification - Notification system design, p... |
| oauth | ULTRA-ADVANCED oauth - OAuth 2.0 implementation, authorizat... |
| payment | ULTRA-ADVANCED payment - Payment integration, gateway selec... |
| performance-monitoring | ULTRA-ADVANCED performance monitoring - Performance monitor... |
| performance-optimization | ULTRA-ADVANCED Performance Optimization - Performance optim... |
| protocol-buffers | ULTRA-ADVANCED Protocol Buffers - Protocol Buffers design -... |
| pwa | ULTRA-ADVANCED pwa - Progressive web app development, servi... |
| query-optimization | ULTRA-ADVANCED Query Optimization - Query optimization - ex... |
| rbac | ULTRA-ADVANCED rbac - RBAC/ABAC design, permission modeling... |
| real-time | ULTRA-ADVANCED real time - Real-time system design with Web... |
| responsive-design | ULTRA-ADVANCED Responsive Design - Responsive design patter... |
| rest-api | ULTRA-ADVANCED rest api - REST API design, resource modelin... |
| scrcpy-install | ULTRA-ADVANCED Scrcpy Install & Usage — Android screen mirr... |
| search-engine | ULTRA-ADVANCED search engine - Search engine integration, i... |
| seo | ULTRA-ADVANCED seo - SEO strategy, technical SEO, content o... |
| self-learning | ULTRA-ADVANCED Self-Learning Engine v5 — deep learning, reinforcement, autonomous improvement |
| seo-optimization | ULTRA-ADVANCED Seo Optimization - SEO optimization - techni... |
| serverless-patterns | ULTRA-ADVANCED Serverless Patterns - Serverless patterns - ... |
| service-mesh | ULTRA-ADVANCED Service Mesh - Service mesh - sidecar, mTLS,... |
| shell-scripting | ULTRA-ADVANCED Shell Scripting - Shell scripting best pract... |
| skill-generator-tool | — |
| sso | ULTRA-ADVANCED sso - Single sign-on implementation, SAML/OI... |
| state-management | ULTRA-ADVANCED State Management - State management patterns... |
| static-sites | ULTRA-ADVANCED static sites - Static site generation, SSG f... |
| streaming | ULTRA-ADVANCED streaming - Streaming data processing with K... |
| terabox-integration | ULTRA-ADVANCED TeraBox Integration - Cloud storage operatio... |
| testing-pyramid | ULTRA-ADVANCED Testing Pyramid - Testing pyramid strategy -... |
| time-series | ULTRA-ADVANCED time series - Time series data management, f... |
| tracing-stack | ULTRA-ADVANCED Tracing Stack - Distributed tracing - OpenTe... |
| vector-database | ULTRA-ADVANCED vector database - Vector database integratio... |
| video-processing | ULTRA-ADVANCED video processing - Video processing, transco... |
| webhooks | ULTRA-ADVANCED webhooks - Webhook management, delivery guar... |
| websockets | ULTRA-ADVANCED websockets - WebSocket management, real-time... |
| windows-shortcut-repair | description: ULTRA-ADVANCED Windows Shortcut Repair — GUI +... |
| zero-downtime-deployment | ULTRA-ADVANCED Zero Downtime Deployment - Zero-downtime dep... |


### Workflow (68) — Process & Methodology
| Skill | Purpose |
|-------|---------|
| a-b-testing | ULTRA-ADVANCED a b testing - A/B testing design, statistica... |
| acceptance-testing | ULTRA-ADVANCED Acceptance Testing - Acceptance testing work... |
| api-design | ULTRA-ADVANCED api design - API design workflow, contract-f... |
| api-design-workflow | ULTRA-ADVANCED Api Design Workflow - API design workflow - ... |
| architecture-decision-record | ULTRA-ADVANCED architecture decision record - ADR creation,... |
| atdd | ULTRA-ADVANCED Atdd - Acceptance Test Driven Development - ... |
| backlog-grooming | ULTRA-ADVANCED backlog grooming - Backlog refinement, prior... |
| bdd-workflow | ULTRA-ADVANCED Bdd Workflow - BDD workflow - Gherkin featur... |
| changelog | ULTRA-ADVANCED changelog - Changelog management workflow wi... |
| chaos-engineering | ULTRA-ADVANCED chaos engineering - Chaos engineering experi... |
| chaos-engineering-workflow | ULTRA-ADVANCED Chaos Engineering Workflow - Chaos engineeri... |
| code-migration | ULTRA-ADVANCED code migration - Code migration workflow wit... |
| code-review-workflow | ULTRA-ADVANCED Code Review Workflow - Code review process -... |
| compliance | ULTRA-ADVANCED compliance - Compliance validation workflow,... |
| continuous-improvement | ULTRA-ADVANCED Continuous Improvement - Continuous improvem... |
| cost-optimization | ULTRA-ADVANCED cost optimization - Cost optimization analys... |
| data-migration | ULTRA-ADVANCED data migration - Data migration workflow wit... |
| data-pipeline-workflow | ULTRA-ADVANCED Data Pipeline Workflow - Data pipeline workf... |
| database-design | ULTRA-ADVANCED database design - Database schema design, no... |
| database-design-workflow | ULTRA-ADVANCED Database Design Workflow - Database design w... |
| database-migration-workflow | ULTRA-ADVANCED Database Migration Workflow - Database migra... |
| decision-log | ULTRA-ADVANCED Decision Log - Decision log - ADR format, ra... |
| definition-of-done | ULTRA-ADVANCED Definition Of Done - Definition of Done - qu... |
| dependency-update | ULTRA-ADVANCED dependency update - Dependency update workfl... |
| diagnose | ULTRA-ADVANCED Diagnose skill with systematic debugging, ro... |
| disaster-recovery | ULTRA-ADVANCED disaster recovery - Disaster recovery planni... |
| documentation-as-code | ULTRA-ADVANCED documentation as code - Documentation as cod... |
| estimation | ULTRA-ADVANCED estimation - Story/task estimation technique... |
| event-storming | ULTRA-ADVANCED Event Storming - Event storming workshop - d... |
| example-mapping | ULTRA-ADVANCED Example Mapping - Example mapping workshop -... |
| exploratory-testing | ULTRA-ADVANCED Exploratory Testing - Exploratory testing - ... |
| feature-flags | ULTRA-ADVANCED feature flags - Feature flag strategy, rollo... |
| grill-me | ULTRA-ADVANCED Grill Me skill with systematic questioning, ... |
| handoff | ULTRA-ADVANCED Handoff skill with comprehensive context pre... |
| impact-mapping | ULTRA-ADVANCED Impact Mapping - Impact mapping - strategic ... |
| incident-postmortem | ULTRA-ADVANCED incident postmortem - Blameless post-mortem ... |
| incident-response-workflow | ULTRA-ADVANCED Incident Response Workflow - Incident respon... |
| load-testing | ULTRA-ADVANCED load testing - Load testing strategy, tool s... |
| localization | ULTRA-ADVANCED localization - Localization workflow, transl... |
| meta-skill-generator | — |
| ml-pipeline-workflow | ULTRA-ADVANCED Ml Pipeline Workflow - ML pipeline workflow ... |
| pair-programming | ULTRA-ADVANCED Pair Programming - Pair programming workflow... |
| pdf-ocr | ULTRA-ADVANCED PDF OCR Skill — Content stream scaling appro... |
| performance-audit | ULTRA-ADVANCED Performance Audit - Performance audit - prof... |
| performance-budget | ULTRA-ADVANCED performance budget - Performance budget crea... |
| performance-testing-workflow | ULTRA-ADVANCED Performance Testing Workflow - Performance t... |
| refactoring-workflow | ULTRA-ADVANCED Refactoring Workflow - Refactoring workflow ... |
| release-notes | ULTRA-ADVANCED release notes - Release notes creation with ... |
| requirements-gathering | ULTRA-ADVANCED Requirements Gathering - Requirements gather... |
| retrospective | ULTRA-ADVANCED retrospective - Sprint retrospective facilit... |
| runbook | ULTRA-ADVANCED runbook - Runbook creation, incident respons... |
| secrets-management | ULTRA-ADVANCED secrets management - Secrets management work... |
| secrets-rotation-workflow | ULTRA-ADVANCED Secrets Rotation Workflow - Secrets rotation... |
| security-review | ULTRA-ADVANCED security review - Security review workflow, ... |
| security-testing-workflow | ULTRA-ADVANCED Security Testing Workflow - Security testing... |
| semantic-versioning | ULTRA-ADVANCED semantic versioning - Semantic versioning wo... |
| specification-by-example | ULTRA-ADVANCED Specification By Example - Specification by ... |
| sprint-planning | ULTRA-ADVANCED sprint planning - Sprint planning workflow w... |
| story-splitting | ULTRA-ADVANCED Story Splitting - User story splitting - ver... |
| tdd | ULTRA-ADVANCED Test-Driven Development with systematic red-... |
| technical-debt | ULTRA-ADVANCED technical debt - Technical debt identificati... |
| technical-specification | ULTRA-ADVANCED Technical Specification - Technical specific... |
| terabox-improvement | ULTRA-ADVANCED TeraBox Improvement - Analyze and optimize T... |
| usability-testing | ULTRA-ADVANCED usability testing - Usability testing workfl... |
| user-research | ULTRA-ADVANCED user research - User research planning, inte... |
| user-story-mapping | ULTRA-ADVANCED User Story Mapping - User story mapping - ba... |
| value-stream-mapping | ULTRA-ADVANCED Value Stream Mapping - Value stream mapping ... |
| zoom-out | ULTRA-ADVANCED Zoom Out skill with comprehensive architectu... |


---

## 5. Session History

### Session 2026-06-30 (Memory Setup)
- Set up 3-layer memory system: AGENTS.md, HANDOFF.md, knowledge_base_v2.json
- Ran 13 improvement cycles on memory system
- **Outcome**: Memory system operational

### Session 2026-06-30 (OneDrive Download)
- Downloaded 8 folders from API-SOF-PRO SharePoint
- Downloaded bulk zip (~20GB) — corrupt, needs re-download
- Partial valid zips: FACTORY IO, SMICROSOFT, SOMOVE VFF SOFT
- Missing: ECOSTRUCTURE, SIMATIC STEP 7, STUDIO 5000 V33, TIA PORTAL V13, UNITY PRO V13
- GLM 5.2: PC cannot run (needs 241GB+ RAM, PC has 32GB)
- .NET Framework 2.0: Already installed
- **Bug**: write/edit tools had $ bug — workaround: bash commands (resolved later)

### Session 2026-07-01 (PLC Program Fix)
- Fixed Schneider SoMachine PLC program (`sdi program.smbp`)
- 2 manual fixes applied + 10 already correct in original
- **Fix 1**: SetCoil → Coil for %M1 (RINSE), %M2 (FILL), %M3 (BYPASS)
- **Fix 10**: SetCoil → Coil + S → ST for valves %M300-%M303, %M351
- Full PLC memory map documented (see Section 9)

### Session 2026-07-04 (PDF Report)
- Created PDF system report using fpdf2
- Pushed to GitHub: `Abdox-menara/opencode-reports`
- PowerShell commands for system data gathering documented

### Session 2026-07-05 (Memory Improvement)
- Rewrote AGENTS.md, HANDOFF.md, knowledge_base_v2.json
- Expanded skill index from 20 to 215+ skills
- Added structured session history
- **Outcome**: Memory system significantly improved

### Session 2026-07-07 (Autodesk Complete Removal)
- Removed all Autodesk products: AutoCAD 2024/2025/2026, Inventor 2027, DWG TrueView 2027, Autodesk Access, CER, AdODIS, AdskIdentityManager, Genuine Service, Material Library, App Manager, Featured Apps, REX Inventor, OpenStudio CLI, AutoCAD Open in Desktop, Save to Web and Mobile, Single Sign On Component
- Method: MsiExec /x (orphaned entries), manual registry cleanup, service removal, file deletion
- Services deleted: AdskLicensingService, Autodesk Access Service Host, Autodesk CER Service
- Registry cleaned: Uninstall keys (64/32-bit), Installer Products, HKLM\SOFTWARE\Autodesk, HKCU\Software\Autodesk
- Folders deleted: C:\Program Files\Autodesk, C:\Program Files (x86)\Autodesk, C:\ProgramData\Autodesk, AppData\Local\Autodesk, AppData\Roaming\Autodesk
- Fixed Windows Installer Error for AcademContentLP-CA (HKLM\SOFTWARE\Classes\Installer\Products\FEE98B82701900001620FCF3A3907BD7)
- **Outcome**: COMPLETED - No reboot required, all clean

### Session 2026-07-11 (Vercel Labs Research)
- Analyzed 318 Vercel Labs public repos
- Identified key architectural patterns: agent-first, skills as first-class, security-first
- Integrated findings into AGENTS.md and knowledge_base_v2.json
- Added 6 new patterns (p016-p020), 5 new learnings (l011-l015)
- **Outcome**: Knowledge base enhanced with external research

### Session 2026-07-13 (Ghost Snapshot Toolkit)
- Built `ghost_snapshot.py` v2.0 with 17 commands for desktop screenshot intelligence
- Fixed 1.333x DPI scale drift in both ghost_control.py and ghost_snapshot.py
- v1.0 (8 features): annotation, diff, OCR, multi-monitor, caching, element discovery, history
- v2.0 (9 new): UIA tree/find/click, EasyOCR/RapidOCR, template match, smart click, regions, watch, export
- Fixed: ctypes.wintypes import, pyautogui win32 GDI fallback, uia-find recursive search, smart-click UIA-first
- Created `ghost-snapshot` skill (SKILL.md) + PowerShell wrapper
- Updated Ghost memory.json to v6.0
- **Outcome**: All 17 commands tested and working

### Session 2026-07-15 (TeraBox Integration)
- Uploaded guard-skills.zip (171MB) to TeraBox cloud storage
- Created terabox-integration tool skill with browser automation
- Created terabox-improvement workflow skill for optimization
- Implemented Python scripts for API integration and analysis
- Updated AGENTS.md with new skills (217+ total)
- **Outcome**: TeraBox integration operational with improvement workflow

### Session 2026-07-28 (Ecosystem Cleanup — Major)
- **Scope**: C:\opencodes\, C:\opencodes\plc\, C:\cursor\, C:\Users\Abdox\.config\opencode\
- **Config fixes (5 files)**: Root `opencode.jsonc` (removed dead `INSTRUCTIONS.md` ref); `plc/opencode.json` (2 trailing commas → valid JSON); `Eplan/opencode.json` (added missing vision model); `C:\Users\Abdox\.config\opencode\opencode.jsonc` (2 trailing commas + broken script paths); `C:\cursor\opencode.jsonc` (3 trailing commas)
- **TS tool fixes (3 files)**: `test-runner.ts` (missing closing brace TS1005; removed dead `promisify(spawn)`); `secret-scanner.ts` (severity cascade TS7053 implicit any); `dependency-auditor.ts` (separated stdout/stderr, added descriptive error codes)
- **Python syntax fixes (3 files)**: `export_all_reports.py` (mismatched f-string parens); `plugin_hooks.py` (6 structural issues); `FastDownloader/_build_v5.py` (unescaped `'` breaking brackets)
- **NPM fix**: `brace-expansion` 5.0.6→5.0.8 — 0 vulnerabilities remaining
- **Windows compat**: replaced `rm -rf` with `if exist ... rd /s /q`; created `_audit.cjs` (ESM/CJS fix)
- **Filesystem cleanup (~400 items, ~75 MB)**: 287 Playwright dumps, 105 test_perms files, 7 stale HTML reports/scripts, 2 empty git repos, 2 dist/ dirs, 2 screenshots, 2 empty config subdirs, InputBlocker-v5.exe, 4 stale `.pyc`, 5 `index.lock` files
- **Git hygiene**: stale `index.lock` cleaned (LIFE-OS, OCR, office expert, opencodes, PC DIAGNOSTIQUE); nested `.git` inside `guard skills\.git\` identified (NTFS-locked, harmless ~1 MB)
- **.gitignore upgrades**: 20 sub-projects + `guard skills` updated (node_modules/, __pycache__/, dist/, *.pyc, *.log, .env, .pytest_cache/)
- **Validation**: all 10 `.json` configs parse strictly; both plc TS projects (`opencode-testing`, `opencode-security`) compile without errors; Ghost memory.json valid JSON
- **Git repair at C:\opencodes**: Corrupted `.git` (nested `.git\.git` + missing objects + stale config.lock) — NTFS-locked, needed `icacls /reset` + `git init --separate-git-dir` pointing to `C:\Users\Abdox\.opencode_git_storage`. Initial commit: 1704 files tracked.
- **Root `.gitignore`**: Updated from 73 → ~110 patterns. Excludes 16 nested repos, AI state files, config backups, Office lock files, logs, generated charts/HTML
- **Line endings normalized**: `.gitignore` (CRLF 51→73, LF 22→0) and `shared-abdox.md` (CRLF 112→131, LF 19→0)
- **17 nested repos identified**: Each has its own `.git` — excluded from parent git tracking
- **npm major updates**: `typescript` 5.7→7.0.2, `@types/node` 20→26.1.1, `@opencode-ai/plugin` 1.0→1.17.13 in both TS projects. Fixed TS 7 breaking changes: added `node:` prefix, replaced `Buffer` with `Uint8Array`, added `"types": ["node"]`
- **Status**: COMPLETED (guard skills node_modules 260 MB prune pending — needs admin)

### Session 2026-08-22 (Memory Improvement)
- Audited 3-layer memory drift: skill counts off by +6 (AGENTS) / +8 (knowledge_base), PC specs stale (C: 147GB→88.4GB, H: 0GB→117.4GB), missing sessions 2026-07-07 and 2026-07-28
- Re-verified filesystem: 223 skills (72 guards, 83 tools, 68 workflow) — updated AGENTS.md header and tables from actual SKILL.md frontmatter
- Updated knowledge_base_v2.json: total_skills 215→223, session_history 6→9, added patterns p021-p024, learnings l016-l019
- Fixed shared-abdox.md encoding (Ã¢â‚¬â€ → —) and updated active issues / models date
- Updated HANDOFF.md and PC Specs (OS 10.0.29648, disk free)
- **Outcome**: Memory fully synced and verified

### Session 2026-08-23 (Improvement Cycle)
- Verified 226 skills (72 guards + 86 tools + 68 workflow); added force-delete, self-learning, desktop-control-mcp to index
- Deleted 180 stale .pyc files (27MB) in skills/self-learning/__pycache__ + 3 junk root test scripts
- Fixed NTFS-locked files via force-delete method (icacls /grant:r user:F /T + .NET File.Delete) - learning l020
- knowledge_base_v2.json: skills_index 223->226, session_history 11->12
- **Finding**: git tracks only 13 of ~500 skill files (.gitignore blocks *.ps1/*.bat globally) - full commit recommended
- **Outcome**: Memory synced to 226 skills, junk purged
---

## 5b. External Research — Vercel Labs (2026-07-11)

318 public repos analyzed. Key patterns applied:

### Top Repos by Stars
| Stars | Repo | Lesson |
|-------|------|--------|
| 38.3k | `agent-browser` | Browser automation CLI for AI agents — validates our Ghost MCP direction |
| 28.9k | `agent-skills` | Agent skill collections are high-demand — validates Guard Skills approach |
| 25.8k | `skills` | Open agent skills tool (`npx skills`) — standardize skill interfaces |
| 15.7k | `json-render` | Generative UI framework — dynamic interfaces from structured data |
| 10.1k | `portless` | Named local URLs replacing ports — simplify local dev |
| 5.7k | `native` | Zig-based native desktop toolkit — performance optimization path |
| 5.2k | `deepsec` | Security harness for coding agents — security-first agent development |

### Architectural Patterns Adopted
| Pattern | Source | Applied To |
|---------|--------|------------|
| Skills as first-class citizens | `skills`, `agent-skills` | Guard Skills 223 skill index |
| Agent-browser automation | `agent-browser` | Ghost MCP tool design |
| Generative UI | `json-render` | Ghost MCP JSON output formatting |
| Edge-first computing | `portless`, `vercel-openclaw` | Cloudflare Workers integration |
| Security-first agents | `deepsec` | Guard validation approach |
| Workflow DevKit patterns | ~60 `workflow-*` repos | Integration pattern library |

### Workflow DevKit Patterns (Applicable)
- Approval chains, gates, and async request-reply for task orchestration
- Circuit breaker, bulkhead, and retry with backoff for resilience
- Event sourcing, message filtering, and content-based routing for event-driven
- Pipeline, map-reduce, and batch processing for data workflows
- Dead letter queue and guaranteed delivery for reliability

### Technology Stack Insights
| Tech | Vercel Labs Usage | Our Adoption |
|------|-------------------|--------------|
| TypeScript | Primary language (80%+) | Ghost MCP uses Python — consider TS port |
| Zig | Native desktop toolkit | Future optimization for Windows API calls |
| Rust | Browser automation (38.3k stars) | High-performance agent tool |
| Python | AI/ML pipelines, agent SDKs | Our primary language — validates choice |

---

## 6. Learned Patterns

| # | Pattern | Confidence | Source |
|---|---------|------------|--------|
| 1 | User asks direct questions, expects concise answers | 95% | Multiple sessions |
| 2 | Prefers action over explanation | 90% | Multiple sessions |
| 3 | Wants iterative improvement cycles | 85% | 13 improvement cycles |
| 4 | Uses Brave browser (not Chrome) | 95% | Ghost quirks |
| 5 | Uses desktop-control MCP for browser automation | 90% | Session history |
| 6 | write/edit tools have $ bug — use bash workaround | 95% | Session 2026-06-30 (resolved, keep as fallback) |
| 7 | Always finish current task before answering new questions | 90% | Session 2026-07-01 |
| 8 | Verify everything thoroughly before completing | 85% | Session 2026-07-01 |
| 9 | Recheck with deep analysis | 80% | Session 2026-07-01 |
| 10 | Ghost Snapshot requires DPI-aware coords (1.333x) + UIA-first click | 92% | Session 2026-07-13 |
| 11 | TeraBox integration via browser hidden input + API quota checks | 88% | Session 2026-07-15 |
| 12 | NTFS-locked dirs need icacls /reset + --separate-git-dir workaround | 90% | Session 2026-07-28 |
| 13 | Autodesk removal requires MsiExec /x + registry + service + folder purge | 95% | Session 2026-07-07 |
| 14 | PLC .smbp dual-representation — never text-edit ladder, edit XML tags only | 90% | Session 2026-07-01 |

## 7. Important Decisions

| Decision | Rationale | Alternatives |
|----------|-----------|--------------|
| Use AGENTS.md for persistent memory | Human-readable, version-controlled | Database, JSON only |
| Use HANDOFF.md for session transfers | Structured handoff format | Plain notes |
| Use knowledge_base_v2.json for learning | Machine-readable, queryable | Binary formats |
| OneDrive files save to Desktop/API SFO | Easy access | Downloads folder |
| Use bash for file operations | write/edit tools had $ bug (now fallback) | Wait for fix |
| Auto-verify skill counts from filesystem | Prevents drift (found 223 vs 217) | Manual counting |
| Store node_modules-excluded counts optionally | 52053 incl. deps vs ~4000 clean | Always full scan |

## 8. Quick Reference

### Paths
| Resource | Path |
|----------|------|
| Skills root | `C:\opencodes\guard skills\skills\` |
| Guards | `skills\guards\` |
| Tools | `skills\tools\` |
| Workflow | `skills\workflow\` |
| OneDrive URL | `https://ofpptcasa-my.sharepoint.com/personal/said_fallah_ofppt-edu_ma/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fsaid%5Ffallah%5Fofppt%2Dedu%5Fma%2FDocuments%2FAPI%2DSOF%2DPRO` |
| Local download | `C:\Users\Abdox\Desktop\API SFO\` |
| GitHub reports | `Abdox-menara/opencode-reports` |
| Ghost memory | `C:\Users\Abdox\.ghost\memory.json` |
| Verify skills | `Get-ChildItem C:\opencodes\guard\ skills\skills\*\ -Directory | Measure-Object` |

### Key Commands
```powershell
# Verify skill counts (run 2026-08-23: 72+86+68=226)
Get-ChildItem "C:\opencodes\guard skills\skills\guards" -Directory | Measure-Object
Get-ChildItem "C:\opencodes\guard skills\skills\tools" -Directory | Measure-Object
Get-ChildItem "C:\opencodes\guard skills\skills\workflow" -Directory | Measure-Object

# System report
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 20 Name, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}}
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, @{N='Free(GB)';E={[math]::Round($_.FreeSpace/1GB,1)}}

# Push to GitHub
gh release create "tag-name" "path/to/file.pdf" --repo Abdox-menara/opencode-reports --title "Title" --notes "Description"

# PDF generation
python -c "from fpdf import FPDF; pdf=FPDF(); pdf.add_page(); pdf.set_font('Arial','B',16); pdf.cell(0,10,'Title',0,1,'C'); pdf.output('out.pdf')"
```

---

## 9. PLC Memory Map (SDI Program)

| Address | Function | Type |
|---------|----------|------|
| %M0-%M3 | Manual mode bits (DRAIN, RINSE, FILL, BYPASS) | Memory |
| %M5 | AUTO mode bit | Memory |
| %M230 | Modbus OK status | Memory |
| %M231 | Alarm reset bit | Memory |
| %M300-%M304 | Valve bits (AV1-AV3) | Memory |
| %M320-%M322 | Physical valve status | Memory |
| %M323 | Pump command | Memory |
| %M330 | Tank low sensor | Memory |
| %M350-%M353 | Pump command bits | Memory |
| %M999 | Emergency stop active | Memory |
| %I0.3 | Emergency stop button (NC) | Input |
| %S13 | First scan bit | System |
| %Q0.0-%Q0.3 | Physical outputs (Pump, AV1, AV2, AV3) | Output |

---

## 10. PC Specs — Verified 2026-08-22 18:02 UTC+1

| Component | Spec |
|-----------|------|
| CPU | Intel Core i7-6920HQ @ 2.90GHz (4C/8T) |
| GPU | NVIDIA Quadro M1200 (4GB) + Intel HD 530 |
| RAM | 32 GB (33396208 KB total, 14877700 KB free) |
| C: | 599.9 GB (88.4 GB free) |
| D: | 474.2 GB (16.2 GB free) |
| H: | 328.5 GB (117.4 GB free — was 0 GB FULL on 2026-07-15) |
| OS | Windows 11 Pro Insider Preview (10.0.29648) |

---

## 11. Current State — Verified 2026-08-22

| Item | Status |
|------|--------|
| OneDrive download | Incomplete (20GB zip corrupt) — not retried since 2026-06-30 |
| Desktop MCP (Ghost) | Operational — 17 commands verified 2026-07-13, memory.json v6.0 exists |
| Memory system | Operational — synced 2026-08-22 (AGENTS.md, shared-abdox.md, knowledge_base_v2.json, HANDOFF.md) |
| write/edit bug | Resolved / fallback — bash workaround kept as fallback |
| Autodesk suite | Fully removed 2026-07-07 — no orphaned Installer products |
| Ecosystem | Cleaned 2026-07-28 — 400 items / 75 MB removed, TS 7 migrated, 0 vulnerabilities |
| Skills drift | Fixed 2026-08-22 — 223 verified (was 217) |

---

*This file is the single source of truth for cross-session memory. Auto-verified 2026-08-22. Update at end of every session and re-run filesystem verification.*
