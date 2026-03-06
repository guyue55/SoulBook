# Soulbook 项目重构计划

## 项目概述
soulbook 是一个基于网络爬虫的小说搜索引擎，提供小说搜索、阅读、书架等功能。

## 重构目标
1. 使用现代化技术栈 (FastAPI, Pydantic, SQLAlchemy)
2. 改进代码结构，提高可维护性
3. 添加类型提示
4. 改进错误处理
5. 使用现代依赖管理 (Poetry)
6. 改进测试覆盖

## 技术栈升级
- Web框架: FastAPI -> 替代 Sanic
- 数据库ORM: SQLAlchemy 2.0 + Async -> 替代 Motor
- 缓存: Redis-py -> 替代 asyncio_redis
- HTTP客户端: httpx -> 替代 aiohttp
- 爬虫: ruia (保留) 或考虑scrapy
- 依赖管理: Poetry -> 替代 Pipenv
- 测试: pytest + pytest-asyncio

## 新项目结构
```
soulbook/
├── alembic/
│   ├── versions/
│   └── env.py
├── src/
│   └── soulbook/
│       ├── __init__.py
│       ├── main.py                 # 应用入口
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py         # 配置管理
│       │   └── database.py         # 数据库配置
│       ├── models/                 # 数据模型
│       │   ├── __init__.py
│       │   ├── base.py             # 基础模型
│       │   ├── user.py             # 用户模型
│       │   ├── novel.py            # 小说模型
│       │   └── bookmark.py         # 书签模型
│       ├── schemas/                # API模式定义
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── novel.py
│       │   └── common.py
│       ├── database/               # 数据库操作
│       │   ├── __init__.py
│       │   ├── session.py          # 会话管理
│       │   └── crud/               # CRUD操作
│       │       ├── __init__.py
│       │       ├── user.py
│       │       └── novel.py
│       ├── api/                    # API路由
│       │   ├── __init__.py
│       │   ├── deps.py             # 依赖注入
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── auth.py         # 认证API
│       │   │   ├── novels.py       # 小说API
│       │   │   └── users.py        # 用户API
│       ├── services/               # 业务逻辑
│       │   ├── __init__.py
│       │   ├── novel_service.py    # 小说服务
│       │   ├── user_service.py     # 用户服务
│       │   └── search_service.py   # 搜索服务
│       ├── utils/                  # 工具函数
│       │   ├── __init__.py
│       │   ├── cache.py            # 缓存工具
│       │   ├── security.py         # 安全工具
│       │   └── validators.py       # 验证器
│       ├── crawlers/               # 爬虫模块
│       │   ├── __init__.py
│       │   ├── base.py             # 基础爬虫类
│       │   ├── qidian.py           # 起点爬虫
│       │   ├── zongheng.py         # 纵横爬虫
│       │   └── middleware.py       # 中间件
│       └── exceptions.py           # 自定义异常
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_auth.py
│   ├── test_novels.py
│   └── integration/
│       └── test_api.py
├── scripts/
│   ├── init_db.py                 # 初始化数据库
│   └── migrate.py                 # 数据迁移脚本
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── pyproject.toml                 # 项目配置
├── poetry.lock
└── README.md
```

## 重构步骤

### 第一步: 创建新项目结构
- 创建新的目录结构
- 配置Poetry依赖管理
- 设置基本的FastAPI应用

### 第二步: 数据模型重构
- 使用SQLAlchemy 2.0定义数据模型
- 添加Pydantic模式验证
- 实现数据关系

### 第三步: API层重构
- 使用FastAPI路由
- 添加类型提示
- 实现依赖注入

### 第四步: 服务层重构
- 分离业务逻辑
- 实现服务类
- 添加单元测试

### 第五步: 爬虫模块重构
- 保留ruia爬虫框架
- 改进错误处理
- 添加重试机制

### 第六步: 数据库操作重构
- 使用SQLAlchemy异步功能
- 实现CRUD操作
- 添加连接池管理

### 第七步: 配置和部署
- 添加环境变量管理
- 配置Docker部署
- 添加CI/CD配置

## 迁移策略

### 数据迁移
1. 从MongoDB导出当前数据
2. 转换为SQL格式
3. 导入到新的PostgreSQL/MySQL数据库

### 功能迁移优先级
1. 核心搜索功能
2. 用户认证系统
3. 书架和书签功能
4. 爬虫功能
5. 推荐系统
6. 管理后台

## 预期收益
- 更好的性能 (FastAPI + 异步数据库)
- 更强的类型安全 (完整类型提示)
- 更好的可维护性 (清晰的分层架构)
- 更高的开发效率 (现代化工具链)
- 更好的扩展性 (模块化设计)
- 更好的测试覆盖率

## 时间估算
- 第一阶段 (基础架构): 2-3天
- 第二阶段 (核心功能): 4-5天
- 第三阶段 (高级功能): 3-4天
- 总计: 9-12天