# Stack: Next.js static export + shadcn base-nova (the studio)

Used for the marketing site and the browser-side tools of `piighost-studio`.

## Setup

- `next.config.ts`: `output: "export"`, `trailingSlash`, unoptimised images,
  MDX pages. No server runtime: no API routes, no server actions.
- shadcn with `style: "base-nova"`, `baseColor: "neutral"`, CSS variables
  (`assets/config/components.json`). Generate primitives with the CLI
  (`pnpm dlx shadcn@latest add button badge card tabs`) rather than copying;
  `assets/react/ui/` shows the expected output.
- `lucide-react`, `next-themes` (`attribute="class" defaultTheme="light"
  enableSystem={false}`), `Geist`/`Geist_Mono` from `next/font/google` exposing
  `--font-geist-sans` / `--font-geist-mono`.
- `assets/tokens/globals.css` is the stylesheet: `@import "shadcn/tailwind.css"`,
  `@custom-variant dark`, the tokens, the responsive root font size.

## Conventions

- **base-ui composes with `render`, never `asChild`.**
  `<Button render={<Link href="…" />}>`. The checker flags `asChild`.
- **Copy through `useT()`**; add keys to `types.ts` and both dictionaries.
- **Pages that render copy are client components** because the locale lives
  in client state.
- **Marketing sections** use `Section` with `snap-start` and
  `min-h-[calc(100dvh-4rem)]`; reduced-motion disables the snap.
- **Browser ML gotchas** (transformers.js, gliner, onnxruntime) are worked
  around in `next.config.ts`; read that file before touching inference code.
- **No `text-[13px]`**: the root font size bumps at 1920 and 2560 px.

## Verify before you finish

`pnpm lint`, `pnpm test`, `pnpm build` (must succeed as a static export), then a
look at light and dark, `/en` and `/fr`.
