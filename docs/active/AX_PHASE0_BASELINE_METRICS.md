# AX_PHASE0_BASELINE_METRICS

Version: 2026-04-20 v1
Status: baseline file created; most live values still require runtime export

## 1. Purpose

This file satisfies `AX_MIGRATION_EXECUTION` §5 and `AX_OPERATIONS_POLICY` §10.1-§10.2 by providing a baseline-metrics file for Phase 0.
It does not invent production numbers that were not captured from runtime evidence.

## 2. Metrics table

| Metric | Baseline value as of 2026-04-20 | Target value | Measurement method | Review interval | Current blocker |
|---|---|---|---|---|---|
| average input tokens per request | unknown | pending Owner/Approver decision | export from live ingress/control-plane logs | monthly | runtime log export missing |
| p50 latency | unknown | pending Owner/Approver decision | live request timing from ingress and worker logs | monthly | runtime log export missing |
| p95 latency | unknown | pending Owner/Approver decision | live request timing from ingress and worker logs | monthly | runtime log export missing |
| average handoff count | unknown | pending Owner/Approver decision | route-log analysis across `main`, `jarvis`, team-lead wrappers | monthly | route-log export missing |
| percentage of repeated work still handled by AI | unknown | pending Owner/Approver decision | classify recurring tasks across n8n/cron/manual AI work | quarterly | deterministic-runtime inventory incomplete |
| rule violation detection count | unknown | pending Owner/Approver decision | aggregate OpenClaw rules + Claude hook block/warn events | monthly | guard event export missing |
| false positive block count | unknown | pending Owner/Approver decision | manual review of blocked runs vs approved reruns | monthly | incident review dataset missing |
| MTTR | unknown | pending Owner/Approver decision | incident log timestamps from detection to containment | quarterly | structured incident log not yet exported |
| monthly manual rework time | unknown | pending Owner/Approver decision | sampled operator rework tracking | quarterly | no current measurement artifact |
| Owner-absence declaration count and duration | 1 declaration id (`OA-20260419-000`), 2 append lines; not yet a meaningful operational baseline | pending Owner/Approver decision | dual-canonical record count and duration rollup | monthly | only smoke-test data exists |
| post-hoc Owner review backlog count | unknown | pending Owner/Approver decision | governance review queue count | monthly | backlog queue not yet instrumented |

## 3. Phase 0 interpretation

- This file now exists, which closes the "missing baseline metrics file" artifact gap.
- Phase 0 baseline capture is still incomplete because most live metrics have not been exported from runtime evidence.
- No migration success claim may cite these metrics until baseline values and target values are populated from live data.
