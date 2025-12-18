# AGENTS instructions

The project is a full-stack application built with TypeScript (React/Next.js) and Python (FastAPI/Microsoft Agent Framework).

## Development Environment

### Backend
- Use `uv` as the package manager.
  - dev server: `uv run fastapi dev`
  - prod server: `uv run fastapi start`
- Use `ruff` as the linter and formatter.
  - lint: `uv run ruff check --fix`
  - format: `uv run ruff format`

### Frontend
- Use `pnpm` as the package manager.
  - dev server: `pnpm dev`
- Use `biome` as the linter and formatter.
  - Use check command to lint and format code: `pnpm check` or `biome check --write`

## Core Stack

### Backend
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.14+
- Pydantic V2: Data validation and settings management using Python type hints

### Frontend
- Nextjs: Full-stack framework for React
- Shadcn UI: A set of beautifully designed components. In this project, it is built on top of **Base UI**.
  - Use shadcn mcp to find and integrate useful components into the project.

## Project Architecture

Organize code around features, domains, and layered boundaries, rather than file type.

**Frontend Architecture Core Concepts**
Refer to the FSD(Feature-Sliced Design) architecture
- Layers: The Backbone of Dependency Direction, from lowest to highest: 
  - shared, entities, features, widgets, app(Routes and Application in Next.js App Router).
- Slices: Grouping by Business Meaning, e.g. user, product, order, etc.
- Segments: Grouping by Technical Purpose, e.g. ui, api, model, lib, config, etc.

```
├── backend/                   # 后端目录
│   ├── app/                   
│   │   ├── core/              # 核心基础设施
│   │   ├── routes/            # 路由模块（每个模块根据需要内含 router,schema,service等）
│   │   ├── llm/               # AI服务
│   │   └── main.py            # 应用入口
│   ├── logs/                  # 日志
│   └── pyproject.toml         # 项目元数据和依赖
├── frontend/                  # 前端目录
│   ├── src/                   # 源代码目录（参考FSD）
│   │   ├── app/               # 应用层和路由层（Nextjs App Router）
│   │   ├── widgets/           # 部件层
│   │   ├── features/          # 功能层
│   │   ├── entities/          # 实体层
│   │   ├── shared/            # 共享层
│   └── package.json           # 项目元数据和依赖
├── AGENTS.md                  # AI 编码代理指南
```

## Code Style
- **Functional Programming**: Prefer functional programming over object-oriented programming
- **Declarative Programming**: Prefer declarative programming over imperative programming
- **Type Hints**: All function signatures must include complete type hints
- **Code Reusability**: Avoid code duplication through iteration and modularization
- **Single Responsibility**: Split large component, function, and file into smaller, focused ones