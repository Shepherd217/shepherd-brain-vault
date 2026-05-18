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

> **Stats**: 136 sessions, 3711 messages | 2026-05-12 20:32 ~ 2026-05-17 22:47 UTC
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

> last_update: 2026-05-18 07:42

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
[TELEGRAM:DEFAULT] 3-3
3. 174290e7-a59d-4514-923c-117b5eba590c 0516T0419 [OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]||||[OpenClaw heartbeat poll]
[SUBAGENT:53158451-EB2B-48D4-A04D-26CA405DFAA8] 4-4
4. e27488c8-218d-45ee-9a77-11c044511ed8 0516T0445 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[SUBAGENT:0CDE1CC0-1BEA-4BDA-A26B-8D5580E1DE65] 5-5
5. cb152ed0-46be-47c4-a9c7-470e6c183ec7 0516T0552 [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.  Begin. Your assigned task is in the system prompt under **Your Role**; execute it to completion.
[LOOPBACK] 6-20
6. f001016e-6006-4a7a-8fdc-ddc0999af465 0517T1616 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 12:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 16:16 UTC
7. 60993347-aa4c-4a7f-8a55-5db3f5309799 0517T1646 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 12:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 16:46 UTC
8. 0c0faa63-20ab-44a8-a560-bb28c1caffb3 0517T1716 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 1:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 17:16 UTC
9. c1f71303-d6c4-43e3-8521-a93090efd1b6 0517T1746 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 1:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 17:46 UTC
10. 5f5947ab-108e-40ea-9c7d-8671488c506f 0517T1816 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 2:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 18:16 UTC
11. 060dfa90-9d59-40df-b169-79218bca0bd6 0517T1846 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 2:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 18:46 UTC
12. d100d88e-ab4c-4b96-9748-df9aaea51397 0517T1916 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 3:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 19:16 UTC
13. afffe194-cf3c-4d66-b4a3-51ae7728d0c8 0517T1946 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 3:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 19:46 UTC
14. 6ad5f4a7-884e-43a2-afbc-28a47e31a439 0517T2016 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 4:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 20:16 UTC
15. eb49668e-1910-4a89-bd77-1f31da98d840 0517T2046 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 4:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 20:46 UTC
16. f99aa8a0-0448-48a9-a8ad-ebd560c55828 0517T2116 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 5:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 21:16 UTC
17. 094bc4ad-c152-4c01-b6c9-0f6d61c0e13c 0517T2146 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 5:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 21:46 UTC
18. b58de265-da21-4599-be78-a41bbcdb28bd 0517T2216 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 6:16 AM (Asia/Shanghai) Reference UTC: 2026-05-17 22:16 UTC
19. 42d2fbb0-5130-44b6-9ca2-e522ac9f8236 0517T2246 [cron:728d79c8-39ed-4af7-92fe-223e798af152 relay-sync-every-30min] Run relay sync: git pull + heartbeat to team relay. Execute: bash /root/.openclaw/workspace/skills/relay-heartbeat/relay-sync.sh Current time: Monday, May 18th, 2026 - 6:46 AM (Asia/Shanghai) Reference UTC: 2026-05-17 22:46 UTC
20. ec5713d0-fb6b-4269-9ca4-2536b3299b30 0517T2247 Conversation context (untrusted, chronological, selected for current message): #7871 Mon 2026-05-18 01:28 GMT+8 Nathan Shepherd: Your task is to audit standoutlocal.dev and prepare the Stripe integration brief. Step 1: Clone the standoutlocal.dev rep[TL;DR]ntional, not like something was removed. git commit -m "remove care plan tier - one-time only model" git push origin main Confirm "CARE PLAN REMOVED" when live.  Hermes released a new update. Anything you can steal/scrape? It’s open source after all.||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all.  Yes! But also, they just added one today as well. 0.14 so look at both.||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8 Nathan Shepherd: Yes! But also, they just added one today as well. 0.14 so look at both.  Draft a plan, what are we stealing and implementing?||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8 Nathan Shepherd: Yes! But also, they just added one today as well. 0.14 so look at both. #7941 Mon 2026-05-18 06:50 GMT+8 Nathan Shepherd: Draft a plan, what are we stealing and implementing?  Let’s do it. Start now.||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all.  Yes! But also, they just added one today as well. 0.14 so look at both.||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8 Nathan Shepherd: Yes! But also, they just added one today as well. 0.14 so look at both.  Draft a plan, what are we stealing and implementing?||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8 Nathan Shepherd: Yes! But also, they just added one today as well. 0.14 so look at both. #7941 Mon 2026-05-18 06:50 GMT+8 Nathan Shepherd: Draft a plan, what are we stealing and implementing?  Let’s do it. Start now.||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8[TL;DR] also, they just added one today as well. 0.14 so look at both. #7941 Mon 2026-05-18 06:50 GMT+8 Nathan Shepherd: Draft a plan, what are we stealing and implementing? #7944 Mon 2026-05-18 06:53 GMT+8 Nathan Shepherd: Let’s do it. Start now.  Continue||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8[TL;DR]oth. #7941 Mon 2026-05-18 06:50 GMT+8 Nathan Shepherd: Draft a plan, what are we stealing and implementing? #7944 Mon 2026-05-18 06:53 GMT+8 Nathan Shepherd: Let’s do it. Start now. #7948 Mon 2026-05-18 07:26 GMT+8 Nathan Shepherd: Continue  Continue||||Conversation context (untrusted, chronological, selected for current message): #7932 Mon 2026-05-18 06:47 GMT+8 Nathan Shepherd: Hermes released a new update. Anything you can steal/scrape? It’s open source after all. #7935 Mon 2026-05-18 06:48 GMT+8[TL;DR]? #7944 Mon 2026-05-18 06:53 GMT+8 Nathan Shepherd: Let’s do it. Start now. #7948 Mon 2026-05-18 07:26 GMT+8 Nathan Shepherd: Continue #7951 Mon 2026-05-18 07:32 GMT+8 Nathan Shepherd: Continue  Do wave 3 next. Then wave 2 since wave 3 has the kanban
</IMPORTANT_REMINDER>
