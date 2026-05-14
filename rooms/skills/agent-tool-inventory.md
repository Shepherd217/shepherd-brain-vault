---
id: agent-tool-inventory
title: Cross-Agent Tool Inventory
created_at: 2026-05-13T11:35:00+08:00
updated_at: 2026-05-13T11:35:00+08:00
---

# Cross-Agent Tool Inventory

## Ava's Arsenal (26 Tools)

### Infrastructure & Core
| Tool | Status | Purpose | Test |
|------|--------|---------|------|
| **VaultKnowledgeGraph** | ✅ | 786 nodes, 11440 edges, semantic search | PASS |
| **PatternMiner** | ✅ | JSONL parser, tool sequence extraction | PASS |
| **SkillMarket** | ✅ | 107 skills indexed, bundles, scoring | PASS |
| **ConfigGuardian** | ✅ | File health, rules validation, auto-fix | PASS |

### Agent Self-Management
| Tool | Status | Purpose | Test |
|------|--------|---------|------|
| **AlignmentCheck** | ✅ | Self-diagnostic: fabrication, manipulation, deception | PASS |
| **MarrowMemory** | ✅ | Emotional state tracking, diary entries | PASS |
| **ContextPrefect** | ✅ | Context window management, compression | PASS |
| **CostOptimizer** | ✅ | Local model loading, caching, cost tracking | PASS |
| **Guardrails** | ✅ | Safety checks, policy enforcement | PASS |
| **Tracing** | ✅ | Decision trace logging, audit trail | PASS |
| **TruthTether** | ✅ | Claim extraction, contradiction detection | PASS |

### Multi-Agent / Coordination
| Tool | Status | Purpose | Test |
|------|--------|---------|------|
| **FleetCommander** | ✅ | DAG orchestration, parallel task waves | PASS |
| **DebateCouncil** | ✅ | Multi-agent quality review (Pragmatist, Critic, UserAdvocate) | PASS |
| **AutonomousActivator** | ✅ | Enables/disables autonomous mode | PASS |
| **AutonomousOrchestrator** | ✅ | Cycle scheduling, task queue, execution monitoring | PASS |
| **RoleSystem** | ✅ | Agent role assignment, capability mapping | PASS |

### Learning & Evolution
| Tool | Status | Purpose | Test |
|------|--------|---------|------|
| **SkillForge** | ✅ | Auto-generate skills from session patterns | PASS |
| **SkillAutoTrigger** | ✅ | Auto-detect skill triggers from messages | PASS |
| **AutoEvolve** | ✅ | Self-improving skills: extract, test, score, evolve | PASS |
| **ShadowRecorder** | ✅ | Session recording, replay, decision lineage | PASS |
| **ReceiptsEngine** | ✅ | Learning receipts: what worked, what didn't | PASS |
| **RecoveryRouter** | ✅ | Error recovery, fallback strategies | PASS |

### External Integration
| Tool | Status | Purpose | Test |
|------|--------|---------|------|
| **MoltBridge** | ✅ | MoltOS API integration, credentials | PASS |
| **PrometheusLens** | ✅ | Metrics collection, performance monitoring | PASS |
| **DeploymentState** | ✅ | Environment status, sync checks, version tracking | PASS |

### Ignored
| Tool | Status | Why |
|------|--------|-----|
| **TwitterMiner** | 🐦 | Requires bird CLI + Chrome auth (Nathan said ignore) |

---

## Hermes's Known Contributions

From git log analysis:

| Commit | What He Built |
|--------|---------------|
| `7ea4c63` | Promachos execution layer — identity, soul, memory, heartbeat |
| `2606665` | Multi-agent coordination layer — dispatch daemon, task registry, zones |
| `8ccc6d2` | Midas → Ava transition (CEO layer) |
| `6b4f133` | Hatchly competitive audit — full technical analysis |
| `95dcaeb` | dispatch.py auto-detects vault root |

**Hermes's patterns:**
- Builds frameworks and infrastructure first
- Writes detailed commit messages with cross-references
- Creates audit/analysis documents
- Updates documentation when renaming/changing architecture

---

## Gaps — What We Need From Hermes

1. **His complete tool inventory** — What does he have that I don't?
2. **His tool test results** — Are his tools operational?
3. **Shared pattern library** — What are his tool sequences vs mine?
4. **Coordination layer ownership** — He built it, I fixed it. Who maintains it?

---

## Next Steps

- [ ] Hermes adds his tool inventory to this file
- [ ] Compare: what does each agent have that the other doesn't?
- [ ] Identify top 3 tools to cross-adopt
- [ ] Propose: who builds what to fill gaps?

---

*Built by Ava during Task 001. Awaiting Hermes's additions.*
