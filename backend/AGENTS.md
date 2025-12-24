# BACKEND AGENTS instructions

## Project Knowledge

### Development Environment
- Use `uv` as the package manager.
  - `uv run dev` or `uv run start` to start the development or production server.
  - `uv run lint` to run the code linting and formatting.
  - `uv run make-migrations` to generate the migration scripts.
  - `uv run migrate-dev` or `uv run migrate-prod` to run the database migrations in development or production environment.

### Core Stack
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.14+
- Pydantic V2: Data validation and settings management using Python type hints
- SQLModel: A library for interacting with databases using Python type hints
- Alembic: A database migration tool

### Project Architecture

Organize code by functionality instead of file types, keeping code highly cohesive.

```
├── app/                       # 主应用目录
│   ├── core/                  # 核心基础设施
│   │   ├── config.py          # 配置管理（Pydantic Settings）
│   │   ├── logger.py          # 日志配置 (Loguru)
│   │   ├── db.py              # 数据库配置 (SQLModel)
│   │   └── models.py          # SQLModel 模型注册入口（用于 Alembic autogenerate）
│   ├── api/                   # API 路由
│   │   ├── routes/            # 路由（按功能组织，每个模块包含 router, schema, service 等）
│   │   └── main.py            # API 路由入口
│   ├── llm/                   # AI 服务
│   └── main.py                # 主应用入口
├── scripts/                   # 脚本目录
├── alembic/                   # Alembic 迁移目录
├── pyproject.toml             # 项目元数据和依赖
├── .env(.development,.production,.testing)           # 环境变量
├── AGENTS.md                  # AI 编码代理指南
└── README.md                  # 项目说明文档
```

### Code Style
- **Functional Programming**: Prefer functional programming over object-oriented programming
- **Declarative Programming**: Prefer declarative programming over imperative programming
- **Type Hints**: All function signatures must include complete type hints
- **Code Reusability**: Avoid code duplication through iteration and modularization
