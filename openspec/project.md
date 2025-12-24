# 项目上下文

## 项目目标
全栈 AI 应用模板项目，旨在提供一套现代化的、开箱即用的 AI 应用开发脚手架。项目集成了前后端最佳实践，包括类型安全、代码规范、数据库迁移和测试覆盖。

## 技术栈

### 前端
- **Next.js 16** - 全栈 React 框架（App Router）
- **React 19** - UI 基础框架
- **TypeScript 5** - 类型安全
- **Shadcn UI** - 组件库（基于 Base UI）
- **Tailwind CSS 4** - 原子化 CSS 工具
- **Jotai** - 原子化状态管理
- **TanStack Query** - 数据获取与缓存
- **CopilotKit** - AI 集成
- **Biome** - 代码格式化和检查
- **pnpm** - 包管理器

### 后端
- **FastAPI** - 现代高性能 Web 框架
- **Pydantic V2** - 数据验证和设置管理
- **Microsoft Agent Framework (@ag-ui/client)** - Agent 代理框架
- **SQLModel** - 数据库 ORM（基于 SQLAlchemy）
- **Alembic** - 数据库迁移工具
- **Loguru** - 日志记录
- **Ruff** - Python 代码检查和格式化
- **MyPy** - 静态类型检查
- **Pytest** - 测试框架
- **uv** - Python 包管理器

## 项目约定

### 代码风格

#### 通用原则（前后端）
- **函数式优先** - 优先使用函数式编程而非面向对象
- **声明式优于命令式** - 偏好声明式编程
- **类型提示完整** - 所有函数签名必须包含完整的类型注解
- **避免重复** - 通过迭代和模块化避免代码重复
- **高内聚** - 按功能而非文件类型组织代码
- **关注组合** - 优先使用组合而非继承
- **避免 prop drilling** - 使用适当的状态管理避免属性传递

#### 前端特定
- **组件拆分** - 将大型组件、函数和文件拆分为更小、更聚焦的单元
- **命名约定**
  - 组件：PascalCase（如 `UserProfile.tsx`）
  - 工具函数：camelCase（如 `formatDate.ts`）
  - 常量：UPPER_SNAKE_CASE（如 `API_BASE_URL`）
  - 类型/接口：PascalCase（如 `UserProps`）
- **文件组织** - 遵循 FSD (Feature-Sliced Design) 架构
- **优先组合** - 优先使用组合模式，避免过度抽象

#### 后端特定
- **函数签名** - 必须包含完整的类型提示
- **代码检查** - 使用 Ruff 进行代码检查和格式化
- **类型检查** - 使用 MyPy 进行静态类型检查
- **命名约定**
  - 模块：snake_case（如 `user_service.py`）
  - 类：PascalCase（如 `UserService`）
  - 函数/变量：snake_case（如 `get_user`）
  - 常量：UPPER_SNAKE_CASE（如 `MAX_RETRIES`）

### 架构模式

#### 前端 - FSD (Feature-Sliced Design)
```
分层（从低到高）：
├── shared/      # 共享代码（跨域）
├── entities/    # 业务实体
├── features/    # 业务功能
├── widgets/     # 组合组件
└── app/         # 应用入口（路由和配置）

细分类型：
├── ui/          # UI 组件
├── api/         # API 调用
├── model/       # 数据模型
├── lib/         # 工具函数
└── config/      # 配置
```

#### 后端 - 功能分层架构
```
app/
├── core/        # 核心基础设施（配置、日志、数据库）
├── api/         # API 路由（按功能组织）
│   └── routes/  # 每个模块包含 router, schema, service等
├── llm/         # AI 服务
└── main.py      # 应用入口
```

每个功能模块自包含：
- `router.py` - 路由定义
- `models.py` - 数据库模型
- `schema.py` - 请求/响应模型
- `service.py` - 业务逻辑

### 测试策略

#### 前端
- 无自动测试，开发者手动测试

#### 后端
- **测试框架** - Pytest + pytest-asyncio
- **覆盖率要求** - 使用 pytest-cov 生成覆盖率报告
- **测试组织** - 测试文件位于 `tests/` 目录
- **异步测试** - `asyncio_mode = "auto"`
- **覆盖率配置**
  - 分支覆盖率启用
  - 缺失行显示在终端
  - 生成 HTML 报告

### Git 工作流

#### 分支策略
- `main` - 主分支（生产代码）
- 功能分支从 `main` 创建
- 使用 Pull Request 进行代码审查

## 领域知识

### AI Agent 集成
项目使用 Microsoft Agent Framework (@ag-ui/client) 构建后端 AI 服务，使用 CopilotKit 进行前端 AI 集成。这支持：
- Agent 状态管理
- 工具调用（function calling）
- 流式响应
- 多轮对话上下文

### 数据库管理
- 使用 Alembic 进行数据库迁移
- 迁移脚本自动生成：`uv run make-migrations`
- 开发环境迁移：`uv run migrate-dev`
- 生产环境迁移：`uv run migrate-prod`
- SQLModel 用于类型安全的数据库操作

### 环境配置
- 多环境支持：development, production, testing
- 使用 `.env` 文件管理环境变量，如 `.env.development`, `.env.testing.local`

## 重要约束

### 包管理器
- **后端**：必须使用 `uv`
- **前端**：必须使用 `pnpm`

### 数据库
- 当前使用 MySQL（通过 PyMySQL）
- 使用 Alembic 进行迁移和回滚（以代码优先的方式管理数据库结构）
- 必须先运行迁移再启动服务

## 外部依赖

### AI 服务
- **LLM Provider** - 需要配置 API Key（通过环境变量）
- **Agent Framework** - Microsoft Agent Framework

### 数据库
- **MySQL** - 主数据库
- **Alembic** - 迁移管理
