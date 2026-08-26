# AGENTS.md

## Project layout
- `frontend/` — React 18 + Vite 5 + react-router-dom v6 SPA (clinical trial patient matching dashboard).
- `backend/` — Node/Express server (`server.js`, port 5000). Frontend dev server proxies `/api` to it.

## Commands
- Frontend dev: `cd frontend && npm ci && npm run dev` (port 3000).
- Production build: `npm run build` (output `frontend/dist/`, gitignored).

## Styling — Tailwind CSS v4 (important)
- The project uses **Tailwind v4** via `@tailwindcss/postcss` (`postcss.config.js`) and `@import "tailwindcss"` in `src/index.css`.
- There is **no `tailwind.config.js`** — v4 ignores it unless referenced with `@config`. The theme lives in the `@theme` block in `src/index.css`.
- Theme tokens are **camelCase on purpose** (`--color-primaryText`, `--color-secondaryText`, `--color-mutedText`) because components use classes like `text-primaryText`. Do not rename them to kebab-case; that silently breaks hundreds of utilities.
- Reusable card style: the `.card` component class in `src/index.css` (bg `#111114`, 1px `#24242A` border, 12px radius).

## Layout conventions
- Sidebar is fixed, 250px wide (`w-[250px]`), hidden below `lg` (becomes a drawer toggled from the Topbar hamburger; state lives in `App.jsx` `AppShell`).
- Main column offsets the sidebar with `lg:pl-[250px]`; Topbar is `sticky` (never `fixed` — body uses `overflow-x: clip` so sticky keeps working).
- `Topbar` derives its page title from a route-pattern map, not props.

## Data
- Pages use mock data (`src/data/mockData.js`) through `src/services/mockApi.js` (async with fake delays). IDs are strings (`PT-001`, `NCT01234567`) — never `parseInt` them when looking up records.
- `src/services/api.js` targets the real backend and is kept for future integration.
