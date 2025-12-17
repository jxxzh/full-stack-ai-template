# AGENTS instructions

## Frontend Project Knowledge

### Development Environment
- Use `pnpm` as the package manager.
  - dev server: `pnpm dev`
- Use `biome` as the linter and formatter.
  - Use check command to lint and format code: `pnpm check` or `biome check --write`

### Core Stack
- Nextjs: Full-stack framework for React
- Shadcn UI: A set of beautifully designed components. In this project, it is built on top of **Base UI**.
  - Use shadcn mcp to find and integrate useful components into the project.

### Project Architecture
Refer to the FSD(Feature-Sliced Design) architecture, organize code around features, domains, and layered boundaries, rather than file type.

**Core Concepts**
- Layers: The Backbone of Dependency Direction, from lowest to highest: shared, entities, features, widgets, app(Routes and Application in Next.js App Router).
- Slices: Grouping by Business Meaning, e.g. user, product, order, etc.
- Segments: Grouping by Technical Purpose, e.g. ui, api, model, lib, config, etc.
