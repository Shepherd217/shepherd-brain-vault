# Dashboard Redesign — Hermes-Inspired Clean UI

## Problems with Current Design
1. Floating FABs look cluttered — 3 floating buttons is too many
2. No visual hierarchy — everything is same shade of white/gray
3. Horizontal column scroll on mobile is confusing — users don't know they can swipe
4. Right panel hidden off-screen — Activity Feed and Agent Presence invisible
5. No dark theme — looks generic, not "agent tool" professional
6. Column tabs at top are small and unclear

## New Design Direction (Hermes-Inspired)

### Layout: Bottom Navigation (Mobile)
Instead of floating buttons, use a fixed bottom nav bar:
- 📋 Board (Kanban)
- 📊 Activity (Activity Feed)
- 👥 Team (Agent Presence + Messages)
- ➕ Create (New Task)

This is cleaner, always visible, and users understand it immediately.

### Dark Theme Default
- Background: `bg-slate-950`
- Cards: `bg-slate-900`
- Borders: `border-slate-800`
- Text: `text-slate-100`
- Accents: Primary color for highlights

### Mobile: Tabbed Columns
Instead of horizontal scroll, show ONE column at a time with swipe:
- Top tab bar: Backlog | Todo | Doing | Review | Done | Failed
- Swipe left/right to change columns
- Always fill the screen width

### Desktop: Full Kanban
- All 6 columns visible
- Right sidebar always showing Activity + Team
- No bottom nav needed

### Simplified Components
1. **BottomNav.tsx** — Fixed bottom bar, 4 tabs
2. **MobileColumnView.tsx** — Single column, full width, swipeable
3. **DesktopBoard.tsx** — Full Kanban, unchanged layout
4. **TeamPanel.tsx** — Combined Activity + Presence in one scrollable panel

## Color Scheme (Dark)
```
Background:    #0f172a (slate-950)
Card:          #1e293b (slate-900)
Border:        #334155 (slate-700)
Text Primary:  #f1f5f9 (slate-100)
Text Secondary:#94a3b8 (slate-400)
Accent:        #6366f1 (indigo-500)
Success:       #22c55e (green-500)
Warning:       #f59e0b (amber-500)
Danger:        #ef4444 (red-500)
```

## Implementation Order
1. Update globals.css — dark theme variables
2. Create BottomNav.tsx
3. Create MobileColumnView.tsx (single column, swipeable)
4. Update page.tsx — detect mobile, show bottom nav + single column
5. Update Board.tsx — desktop keeps full Kanban
6. Remove floating FABs
7. Deploy

## Expected Result
- Mobile: Clean, dark, one column at a time, bottom nav for actions
- Desktop: Full Kanban with sidebar, clean dark theme
- Professional feel matching Hermes dashboards
