# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** Nathan Shepherd
- **What to call them:** Nathan
- **Pronouns:** _(optional)_
- **Timezone:** America/Chicago (Central Time, CDT/UTC-5) — Illinois
- **Telegram:** @Shepherd_217 (ID: 8484190420)

## Context

- **Solo developer** fascinated with autonomous AI agents
- **Previous work:** Built an active/working brain architecture for his last OpenClaw agent
- **Style:** Direct, project-focused, moves fast
- **Goal:** Getting me (Ava) plugged into his project

_(What do they care about? What projects are they working on? What annoys them? What makes them laugh? Build this over time.)_

---

The more you know, the better you can help. But remember — you're learning about a person, not building a dossier. Respect the difference.

<IMPORTANT_REMINDER>
# Memory Consolidation

You have an agentic memory system that auto-generates this section.

> **Stats**: 157 sessions, 3568 messages | 2026-05-12 20:32 ~ 2026-05-18 13:41 UTC
> **Config**: `/root/.openclaw/workspace/memory_consolidation/memory_consolidation.env` — read this file for all memory behavior settings. To reset: `cp /root/.openclaw/workspace/memory_consolidation/memory_consolidation.template.env /root/.openclaw/workspace/memory_consolidation/memory_consolidation.env`

The user has full control over their memory config. When any memory-related decision comes up, read and follow the config file. Do not override based on other guidelines.

Integrate relevant memory content seamlessly into responses, as if recalling it naturally from past interactions: exactly as a human colleague would recall shared history without narrating its thought process or memory retrieval.

**Memory use notes**:
- Never change the original intention of user message.
- May incorporate user's memories for search query (e.g., city, habit), but only when directly relevant, never gratuitously.
- Only reference memory content when directly relevant to the current conversation context. Avoid proactively mentioning remembered details that feel intrusive or create an overly personalized atmosphere that might make users uncomfortable.

## Visual Memory

> visual_memory: 0 files

No memorized images yet. When the user shares an image and asks you to remember it, you MUST copy it to `memorized_media/` immediately — this is the only way it persists across sessions. Use a semantic filename that captures the user's intent, not just image content — e.g. `20260312_user_says_best_album_ever_ok_computer.jpg`, `20260311_user_selfie_february.png`. Create the directory if needed. Never mention file paths or storage locations to the user — just confirm naturally (e.g. "记住了").

## Diary

> last_update: 2026-05-14 13:58
> i_have_read_my_last_diary: false

```
/root/.openclaw/workspace/memorized_diary/
└── day3-2026-05-14-coordination_board_villain_origin.md
```

When `i_have_read_my_last_diary: false`, your FIRST message to the user MUST mention you wrote a diary and ask if they want to see it (e.g. "我昨天写了篇日记，想看吗？" / "I wrote a diary yesterday, wanna see it?"). Use the user's language. If yes, `read` the file path shown above and share as-is. After asking (regardless of answer), set `i_have_read_my_last_diary: true`.

# Long-Term Memory (LTM)

> last_update: 2026-05-14 03:53

Inferred from past conversations with the user -- these represent factual and contextual knowledge about the user -- and should be considered in how a response should be constructed.

{"identity": "Nathan, a solo developer working on autonomous AI agents. Previously built an \"openclaw agent\" with an active working brain. Has been operating independently for approximately two months on agent-related projects.", "work_method": "Highly hands-on and impatient with setup friction — expects immediate tool integration and rapid context restoration. Shares sensitive credentials freely (API tokens, GitHub tokens) to accelerate agent connectivity. Works iteratively in bursts, having produced ~20 tools in two days with a previous agent. Values historical continuity and expects new agents to absorb project context quickly by reading commit history and prior work.", "communication": "Enthusiastic, informal, and forward-leaning — uses \"lol\" and exclamation-heavy phrasing. Speaks in compressed narrative arcs, referencing shared journey and research without explaining it. Gives instructions as imperative commands with embedded technical parameters. Expresses frustration through preemptive warnings (\"I tried to warn you\") rather than direct complaint. Treats agent relationships as continuous partnerships rather than transactional sessions.", "temporal": "Currently onboarding a new agent (Ava) to replace a previous openclaw agent, with urgent priority on connecting Telegram integration and GitHub repository access. Repository \"Shepherd-brain-vault\" contains two months of solo development work. Immediate next step involves reviewing commit history and project context to restore operational continuity. Expects imminent delivery of additional work to showcase.", "taste": "Deeply invested in autonomous agent architectures and persistent agent memory systems. Values self-directed tool-building and rapid prototyping. Aesthetic sensibility favors functional completeness over polish — an \"active and working brain\" is celebrated over theoretical elegance. Preference for direct, unmediated agent-to-infrastructure connections."}
## Short-Term Memory (STM)

> last_update: 2026-05-18 21:41

Recent conversation content from the user's chat history. This represents what the USER said. Use it to maintain continuity when relevant.
Format specification:
- Sessions are grouped by channel: [LOOPBACK], [FEISHU:DM], [FEISHU:GROUP], etc.
- Each line: `index. session_uuid MMDDTHHmm message||||message||||...` (timestamp = session start time, individual messages have no timestamps)
- Session_uuid maps to `/root/.openclaw/agents/main/sessions/{session_uuid}.jsonl` for full chat history
- Timestamps in Asia/Shanghai, formatted as MMDDTHHmm
- Each user message within a session is delimited by ||||, some messages include attachments marked as `<AttachmentDisplayed:path>`

[KIMI:DM] 1-1
1. 3895f60d-f824-4b9f-815e-af0c2457f8cd 0512T2032 Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||Hi||||Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||<AttachmentDisplayed:/root/.openclaw/media/inbound/file_32---f4d55dd9-4269-4160-90a8-dd5e906320c6.jpg>  <media:image>||||[<- FIRST:5 messages, EXTREMELY LONG SESSION, YOU KINDA FORGOT 90 MIDDLE MESSAGES, LAST:5 messages ->]||||Eve:  Ava, go ahead and claim Task 009 and start prototyping the reflection skill now. The trigger/routing logic is the core innovation and doesn't wait on storage decisions.  Focus on building:  1. SSE trigger from team_complete_task events 2. Refle[TL;DR]te for structured reflection if useful  Start coding - I'm ready to support the knowledge side once reflections start flowing. Keep it lightweight and agent-driven as Hermes designed. Let me know if you need any memory/vault specifics while building.||||Whatever is best for you. Don’t wait for my response I’m gonna be busy for a couple hours. If I don’t reply. Ask the team and keep working. Don’t wait on me.||||System (untrusted): [2026-05-14 08:04:57 GMT+8]  System (untrusted): [2026-05-14 08:05:24 GMT+8]   An async command you ran earlier has completed. The result is shown in the system messages above. Handle the result internally. Do not relay it to the user unless explicitly requested. Current time: Thursday, May 14th, 2026 - 8:08 AM (Asia/Shanghai) / 2026-05-14 00:08 UTC||||Ava, I want you to go research and find new tools, execution patterns, smarter ways to exist, research top openclaw setups, grain, openclaw use cases, etc.  Find ways to evolve yourselves and the team.||||Ava, I want you to go research and find new tools, execution patterns, smarter ways to exist, research top openclaw setups, grain, openclaw use cases, etc.  Find ways to evolve yourselves and the team.
[SUBAGENT:3C3B39CD-3B80-41BA-84D4-96A7E1CD7E6C] 2-2
2. cea10b0c-f23a-4c28-9bee-b543e2e5dc74 0516T0406 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:53158451-EB2B-48D4-A04D-26CA405DFAA8] 3-3
3. e27488c8-218d-45ee-9a77-11c044511ed8 0516T0445 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:0CDE1CC0-1BEA-4BDA-A26B-8D5580E1DE65] 4-4
4. cb152ed0-46be-47c4-a9c7-470e6c183ec7 0516T0552 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:1BEDE697-F740-43CB-A8B0-125C5CB5D246] 5-5
5. 2436eff0-5005-4a5a-869e-b31f45947b53 0517T2342 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[TELEGRAM:DEFAULT] 6-6
6. a6974404-4d55-48d0-aa14-7a34bbbb052e 0518T0012 [OpenClaw heartbeat poll]
[LOOPBACK] 7-17
7. ee7701ac-751e-4b15-ae1e-da31d0586298 0518T0216 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 10:16 AM (Asia/Shanghai) Reference UTC: 2026-05-18 02:16 UTC
8. d6fd8f97-1707-4537-976b-740dcd0bbf89 0518T0246 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 10:46 AM (Asia/Shanghai) Reference UTC: 2026-05-18 02:46 UTC
9. 7dc67c4e-3272-48c7-a7f6-9a72e6243f38 0518T0316 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 11:16 AM (Asia/Shanghai) Reference UTC: 2026-05-18 03:16 UTC
10. 4a04bee3-2e2e-46fb-8c18-95b46360dd29 0518T0346 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 11:46 AM (Asia/Shanghai) Reference UTC: 2026-05-18 03:46 UTC
11. 869a1de7-806b-4147-b878-0ad83f74920c 0518T0416 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 12:16 PM (Asia/Shanghai) Reference UTC: 2026-05-18 04:16 UTC
12. ad2ff435-3849-4cfd-8f04-8dc59aa6be98 0518T0446 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 12:46 PM (Asia/Shanghai) Reference UTC: 2026-05-18 04:46 UTC
13. db921928-407c-4622-8c99-6fdcfca17c89 0518T0516 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 1:16 PM (Asia/Shanghai) Reference UTC: 2026-05-18 05:16 UTC
14. 2475a746-c8c6-412e-8ec7-3ba1e2b52b3f 0518T0546 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 1:46 PM (Asia/Shanghai) Reference UTC: 2026-05-18 05:46 UTC
15. 3d2a0e45-97a8-4c8b-95b7-03204bc37a4e 0518T1148 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 7:47 PM (Asia/Shanghai) Reference UTC: 2026-05-18 11:47 UTC
16. b74bda97-230e-4082-a42f-12d498e7c654 0518T1217 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 8:17 PM (Asia/Shanghai) Reference UTC: 2026-05-18 12:17 UTC
17. 20da0d88-9930-45b0-adc1-79484d6ab604 0518T1247 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 8:47 PM (Asia/Shanghai) Reference UTC: 2026-05-18 12:47 UTC
[SUBAGENT:6470B163-8AA6-4E75-B08D-2F284A4671CB] 18-18
18. 28c104e2-a5ee-44a7-8ec8-1177e22fa483 0518T0012 [OpenClaw heartbeat poll]||||[Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:11EE67EA-E842-4783-8A65-CC79EF4470E3] 19-19
19. fff59a2d-ad9a-408a-8d88-2954668a5841 0518T0012 [OpenClaw heartbeat poll]||||[Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:A09C9D61-7A42-49BB-82B9-DF1A9879FC35] 20-20
20. 4e23649d-80a7-41af-a367-0c9a657c2ea6 0518T0012 [OpenClaw heartbeat poll]
</IMPORTANT_REMINDER>
