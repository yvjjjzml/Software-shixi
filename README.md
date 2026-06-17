# AI智能知识管理工作台（软件开发生产实习项目）

> 笔记管理 + AI智能 + 数据看板 + 搜索检索 + 用户系统

## 技术栈

- **前端**: Vue3 + TypeScript + Element Plus + ECharts + Vite
- **后端**: Python Flask + SQLite + DeepSeek API
- **AI能力**: 摘要生成、自动标签、知识问答、内容润色、关联推荐

## 项目结构

```
├── backend/                # Flask后端
│   ├── app.py             # 应用入口
│   ├── config/            # 配置
│   │   └── config.py
│   ├── routes/            # 路由模块
│   │   ├── auth.py        # 认证API
│   │   ├── notes.py       # 笔记API
│   │   ├── ai.py          # AI功能API
│   │   ├── dashboard.py   # 仪表盘API
│   │   ├── search.py      # 搜索API
│   │   ├── admin.py       # 管理员API
│   │   ├── tags.py        # 标签API
│   │   ├── templates.py   # 模板API
│   │   └── demo.py        # 演示数据API
│   ├── utils/             # 工具函数
│   │   └── __init__.py
│   └── requirements.txt
├── frontend/              # Vue3前端
│   ├── src/
│   │   ├── api/           # API封装
│   │   ├── components/    # 组件
│   │   ├── router/        # 路由
│   │   ├── stores/        # 状态管理
│   │   └── views/         # 页面
│   └── package.json
├── data/                  # 数据存储
├── .gitignore
├── LICENSE
└── README.md
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端运行在 http://localhost:5000

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:3000，自动代理API到后端。

### 默认管理员账户

- 用户名: `admin`
- 密码: `admin123`

## 功能特性

- 📝 笔记CRUD（创建/编辑/删除/状态管理）
- 🤖 AI智能摘要/标签/问答/润色/推荐
- 📊 数据看板（ECharts图表）
- 🔍 全文搜索 + 标签/分类筛选
- 👤 用户系统 + JWT认证
- 🔐 管理员后台
- 📁 文件导入导出（.txt/.md）
- 📋 笔记模板

## API接口

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 认证 | /api/auth/register | POST | 用户注册 |
| 认证 | /api/auth/login | POST | 用户登录 |
| 笔记 | /api/notes | GET/POST | 获取/创建笔记 |
| 笔记 | /api/notes/:id | GET/PUT/DELETE | 笔记详情/更新/删除 |
| AI | /api/ai/summarize | POST | AI摘要 |
| AI | /api/ai/auto-tag | POST | AI标签 |
| AI | /api/ai/ask | POST | AI问答 |
| AI | /api/ai/polish | POST | AI润色 |
| 仪表盘 | /api/dashboard/stats | GET | 数据统计 |
| 搜索 | /api/search | GET | 搜索笔记 |
| 管理 | /api/admin/users | GET | 用户列表 |
| 管理 | /api/admin/notes | GET | 笔记列表 |

## License

[MIT](LICENSE)
