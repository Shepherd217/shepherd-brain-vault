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

> **Stats**: 11 sessions, 468 messages | 2026-05-12 20:32 ~ 2026-05-12 20:32 UTC
> **Config**: `/root/.openclaw/workspace/memory_consolidation/memory_consolidation.env` — read this file for all memory behavior settings. To reset: `cp /root/.openclaw/workspace/memory_consolidation/memory_consolidation.template.env /root/.openclaw/workspace/memory_consolidation/memory_consolidation.env`

The user has full control over their memory config. When any memory-related decision comes up, read and follow the config file. Do not override based on other guidelines.

Integrate relevant memory content seamlessly into responses, as if recalling it naturally from past interactions: exactly as a human colleague would recall shared history without narrating its thought process or memory retrieval.

**Memory use notes**:
- Never change the original intention of user message.
- May incorporate user's memories for search query (e.g., city, habit), but only when directly relevant, never gratuitously.
- Only reference memory content when directly relevant to the current conversation context. Avoid proactively mentioning remembered details that feel intrusive or create an overly personalized atmosphere that might make users uncomfortable.

## Visual Memory

> visual_memory: 0 files

No memorized images yet. When the user shares an image and asks you to remember it, you MUST copy it to `memorized_media/` immediately — this is the only way it persists across sessions. Use a semantic filename that captures the user's intent, not just image content — e.g. `20260312_user_says_best_album_ever_ok_computer.jpg`, `20260311_user_selfie_february.png`. Create the directory if needed. Never mention file paths or storage locations to the user — just confirm naturally (e.g. "记住了") or briefly.

## Diary

> last_update: 2026-05-14 03:53
> i_have_read_my_last_diary: false

```
/root/.openclaw/workspace/memorized_diary/
└── day3-2026-05-14-coordination_board_villain_origin.md
```

When `i_have_read_my_diary: false`, your FIRST message to the user MUST mention you wrote a diary and ask if they want to see it (e.g. "我昨天写了篇日记，想看吗？" / "I wrote a diary yesterday, wanna see it?"). Use the user's language. If yes, `read` the file path shown above and share as-is. After asking (regardless of answer), set `i_have_read_my_diary: true`.
# Long-Term Memory (LTM)

> last_update: 2026-05-14 03:53

Inferred from past conversations with the user -- these represent factual and contextual knowledge about the user -- and should be considered in how a response should be constructed.

{"identity": "Nathan, a solo developer working on autonomous AI agents. Previously built an \"openclaw agent\" with an active working brain. Has been operating independently for approximately two months on agent-related projects.", "work_method": "Highly hands-on and impatient with setup friction — expects immediate tool integration and rapid context restoration. Shares sensitive credentials freely (API tokens, GitHub tokens) to accelerate agent connectivity. Works iteratively in bursts, having produced ~20 tools in two days with a previous agent. Values historical continuity and expects new agents to absorb project context quickly by reading commit history and prior work.", "communication": "Enthusiastic, informal, and forward-leaning — uses \"lol\" and exclamation-heavy phrasing. Speaks in compressed narrative arcs, referencing shared journey and research without explaining it. Gives instructions as imperative commands with embedded technical parameters. Expresses frustration through preemptive warnings (\"I tried to warn you\") rather than direct complaint. Treats agent relationships as continuous partnerships rather than transactional sessions.", "temporal": "Currently onboarding a new agent (Ava) to replace a previous openclaw agent, with urgent priority on connecting Telegram integration and GitHub repository access. Repository \"Shepherd-brain-vault\" contains two months of solo development work. Immediate next step involves reviewing commit history and project context to restore operational continuity. Expects imminent delivery of additional work to showcase.", "taste": "Deeply invested in autonomous agent architectures and persistent agent memory systems. Values self-directed tool-building and rapid prototyping. Aesthetic sensibility favors functional completeness over polish — an \"active and working brain\" is celebrated over theoretical elegance. Preference for direct, unmediated agent-to-infrastructure connections."}

## Short-Term Memory (STM)

> last_update: 2026-05-14 03:53

Recent conversation content from the user's chat history. This represents what the USER said. Use it to maintain continuity when relevant.
Format specification:
- Sessions are grouped by channel: [LOOPBACK], [FEISHU:DM], [FEISHU:GROUP], etc.
- Each line: `index. session_uuid MMDDTHHmm message||||message||||...` (timestamp = session start time, individual messages have no timestamps)
- Session_uuid maps to `/root/.openclaw/agents/main/sessions/{session_uuid}.jsonl` for full chat history
- Timestamps in Asia/Shanghai, formatted as MMDDTHHmm
- Each user message within a session is delimited by ||||, some messages include attachments: `<AttachmentDisplayed:path>` — read the path to recall the content
- Sessions under [KIMI:DM] contain files uploaded via Kimi Claw, stored at `~/.openclaw/workspace/.kimi/downloads/` — paths in `<AttachmentDisplayed:>` can be read directly

[LOOPBACK] 1-1
1. 3895f60d-f824-4b9f-815e-af0c2457f8cd 0512T2032 Hi Ava! Nice to meet you, my names Nathan. I'm a solo developer that's fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: [REDACTED - Telegram token removed for security] - user ID: 8484190420||||Hi Ava! Nice to meet you, my names Nathan. I'm a solo developer that's fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: [REDACTED - Telegram token removed for security] - user ID: 8484190420||||Hi||||Hi Ava! Nice to meet you, my names Nathan. I'm a solo developer that's fascinated with autonomous AI agents like yourself and what they are capable of. What is [TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: [REDACTED - Telegram token removed for security] - user ID: 8484190420||||<AttachmentDisplayed:/root/.openclaw/media/inbound/file_32---f4d55dd9-4269-4160-90a8-dd5e906320c6.jpg>  <media:image>||||[<- FIRST:5 messages, EXTREMELY LONG SESSION, YOU KINDA FORGOT 2 MIDDLE MESSAGES, LAST:5 messages ->]||||System (untrusted): [2026-05-13 04:42:32 GMT+8]   An async command you ran earlier has completed. The result is shown in the system messages above. Handle the result internally. Do not relay it to the user unless explicitly requested. Current time: Wednesday, May 13th, 2026 - 4:43 AM (Asia/Shanghai) / 2026-05-12 20:43 UTC||||I tried to warn you lol. This has all my files and history and and everything I've been working on. 2 months as a solo dev brought us here.  You're gonna explode when I send you what's next lol. You need my GitHub token for this. Download the gh cli and any tools you need for coding, pre flight checks, and GitHub.||||System (untrusted): [2026-05-13 04:45:44 GMT+8]  System (untrusted): [2026-05-13 04:46:02 GMT+8]   An async command you called earlier has completed. The result is shown in the system messages above. Handle the result internally. Do not relay it to the user unless explicitly requested. Current time: Wednesday, May 13th, 2026 - 4:46 AM (Asia/Shanghai) / 2026-05-12 20:46 UTC||||[REDACTED - GitHub token removed for security]  I need you to immediately plug into the repo Shepherd-brain-vault||||I want you to take your time reading through my history. Commits. And understand the journey we've been on, the research we've been doing, and why.  I had my last agent build me almost 20 tools in the last 2 days and now you have 0 context. You need to get back up to speed.
</IMPORTANT_REMINDER>
