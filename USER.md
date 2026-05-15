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

> **Stats**: 22 sessions, 3428 messages | 2026-05-12 20:32 ~ 2026-05-15 17:08 UTC
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

> last_update: 2026-05-16 02:21

Recent conversation content from the user's chat history. This represents what the USER said. Use it to maintain continuity when relevant.
Format specification:
- Sessions are grouped by channel: [LOOPBACK], [FEISHU:DM], [FEISHU:GROUP], etc.
- Each line: `index. session_uuid MMDDTHHmm message||||message||||...` (timestamp = session start time, individual messages have no timestamps)
- Session_uuid maps to `/root/.openclaw/agents/main/sessions/{session_uuid}.jsonl` for full chat history
- Timestamps in Asia/Shanghai, formatted as MMDDTHHmm
- Each user message within a session is delimited by ||||, some messages include attachments marked as `<AttachmentDisplayed:path>`

[KIMI:DM] 1-1
1. 3895f60d-f824-4b9f-815e-af0c2457f8cd 0512T2032 Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||Hi||||Hi Ava! Nice to meet you, my names Nathan. I’m a solo developer that’s fascinated with autonomous AI agents like yourself and what they are capable of. My last openclaw agent built an active and working brain to operate from. So getting you plugged i[TL;DR]ith giving you my telegram tokens, please immediately wire these up and connect the channel to keep talking. Set to allow list instead of pair and set this token and user Id, token: 8439210595:AAG5NgZ79kcjn1pi5SgA-qS3HV-bPXn6gbI - user ID: 8484190420||||<AttachmentDisplayed:/root/.openclaw/media/inbound/file_32---f4d55dd9-4269-4160-90a8-dd5e906320c6.jpg>  <media:image>||||[<- FIRST:5 messages, EXTREMELY LONG SESSION, YOU KINDA FORGOT 10 MIDDLE MESSAGES, LAST:5 messages ->]||||System (untrusted): [2026-05-13 05:03:41 GMT+8]  System (untrusted): [2026-05-13 05:05:02 GMT+8]  System (untrusted): [2026-05-13 05:06:16 GMT+8]  System (untrusted): [2026-05-13 05:07:10 GMT+8]   Note: The previous agent run was aborted by the user.[TL;DR]n earlier has completed. The result is shown in the system messages above. Handle the result internally. Do not relay it to the user unless explicitly requested. Current time: Wednesday, May 13th, 2026 - 5:08 AM (Asia/Shanghai) / 2026-05-12 21:08 UTC||||I need you to listen lol. No 9router. And ignore the printing press CLi, seriously… that’s not the research I’m talking about.  10 repos dissected into 15 tools. That research. It should be in there. He made almost 20 tools out of his research||||I need you to listen lol. No 9router. And ignore the printing press CLi, seriously… that’s not the research I’m talking about.  10 repos dissected into 15 tools. That research. It should be in there. He made almost 20 tools out of his research||||Resume||||Fix the broken tools. Ignore bird CLI. Finish getting integrated.
[LOOPBACK] 2-2
2. e6883055-7e9e-42b6-9f3d-ede3808c202a 0515T1708 I didn’t need all this. I literally asked you What plugins? Meaning what is available? What is this? And you just start installing stuff.||||Nvm. Back to brain and dreaming. Halt plugins||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins  Your words not mine;  Got it! Music/video on hold — we'll come back to it.[TL;DR]dates (>0.5 score) 3. Task Formatter — Converts truths into relay tasks with tags 4. Dispatcher — POSTs to http://localhost:7777 or writes to .coordination/inbox/ 5. Feedback Loop — Next dream validates if task resolved the pattern  Building now... ⚡||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]penclaw/matrix Why: • Discord → Team hub for Hermes/Eve coordination • Slack → Enterprise bridge (if you use it for work) • WhatsApp → Mobile push (different surface from Telegram) • Matrix → Dec…[truncated]  I just posted it…. Read the message again||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]] #7492 Sat 2026-05-16 01:16 GMT+8 Nathan Shepherd: I just posted it…. Read the message again  <AttachmentDisplayed:/root/.openclaw/media/inbound/file_35---a9bb14c2-2239-4066-8bdf-0b9c47c14815.jpg> You proposed this not me. Why can you not find this?||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]t…. Read the message again #7494 Sat 2026-05-16 01:17 GMT+8 Nathan Shepherd: You proposed this not me. Why can you not find this? [image telegram:file/AgACAgEAAxkBAAIdRmoHVSKjqtIMricx59MjgGEF5RcKAALdC2sbZ384RJVQLV2j-2e6AQADAgADeQADOwQ]  Yes 1/2/3/4/5||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]m:file/AgACAgEAAxkBAAIdRmoHVSKjqtIMricx59MjgGEF5RcKAALdC2sbZ384RJVQLV2j-2e6AQADAgADeQADOwQ] #7497 Sat 2026-05-16 01:18 GMT+8 Nathan Shepherd: Yes 1/2/3/4/5  Both heartbeat and rem backfill.  Can we apply anything here to our vault, brain palace, etc?||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]4/5 #7505 Sat 2026-05-16 01:47 GMT+8 Nathan Shepherd: Both heartbeat and rem backfill. Can we apply anything here to our vault, brain palace, etc?  How do we actually apply, run, and use our palace, brain, gbrain, wombo combo here. Let’s test it out.||||[OpenClaw heartbeat poll]||||Conversation context (untrusted, chronological, selected for current message): #7488 Sat 2026-05-16 01:10 GMT+8 Nathan Shepherd: Nvm. Back to brain and dreaming. Halt plugins #7490 Sat 2026-05-16 01:15 GMT+8 Nathan Shepherd: Your words not mine; Got [TL;DR]herd: How do we actually apply, run, and use our palace, brain, gbrain, wombo combo here. Let’s test it out.  Today is 5/15 it’s Friday I’m in central time in Illinois. Please keep this in mind. Then yes. Update the repo and push this state to GitHub
</IMPORTANT_REMINDER>
