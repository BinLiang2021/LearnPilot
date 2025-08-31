# LearnPilot Frontend

LearnPilot AI论文学习助手的现代化React前端界面。

## ✨ 特性

- 🎯 **智能分析** - AI驱动的论文内容分析和概念提取
- 📚 **学习计划** - 个性化学习路径规划和进度跟踪
- 🕸️ **知识图谱** - 可视化知识结构和概念关系
- 📱 **响应式设计** - 完美适配移动端和桌面端
- 🎨 **现代界面** - 专业的学术风格设计
- 🔐 **安全认证** - JWT token认证和权限控制
- ⚡ **高性能** - React 18 + Vite + TypeScript
- 🧩 **组件化** - 完整的UI组件库
- 🌐 **中文支持** - 完整的中文本地化
- ♿ **无障碍** - 遵循WCAG可访问性标准

## 🚀 快速开始

### 环境要求
- Node.js 18+ 
- npm 8+ 或 yarn 1.22+

### 安装步骤

1. **安装依赖**
   ```bash
   npm install
   ```

2. **环境配置**
   ```bash
   # 复制环境配置文件
   cp .env.example .env
   
   # 编辑配置（可选）
   nano .env
   ```

3. **启动开发服务器**
   ```bash
   # 使用启动脚本（推荐）
   chmod +x start_frontend.sh
   ./start_frontend.sh
   
   # 或直接使用npm
   npm run dev
   ```

4. **访问应用**
   打开浏览器访问 [http://localhost:3000](http://localhost:3000)

### 环境变量配置

```env
# API 配置
VITE_API_BASE_URL=http://localhost:8000/api

# 应用配置
VITE_APP_NAME=LearnPilot
VITE_APP_VERSION=1.0.0

# 开发模式配置
VITE_DEV_MODE=true

# 文件上传配置
VITE_MAX_FILE_SIZE=52428800
VITE_SUPPORTED_FILE_TYPES=pdf,md,txt

# 功能开关
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_NOTIFICATIONS=true
```

## 📁 项目结构

```
frontend/
├── src/                      # 源代码目录
│   ├── components/          # React组件
│   │   ├── ui/             # 基础UI组件
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   └── layout/         # 布局组件
│   │       ├── Layout.tsx
│   │       ├── Header.tsx
│   │       └── Sidebar.tsx
│   ├── pages/              # 页面组件
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── UploadPage.tsx
│   │   ├── AnalysisPage.tsx
│   │   ├── PlanPage.tsx
│   │   ├── GraphPage.tsx
│   │   ├── SettingsPage.tsx
│   │   └── AdminPage.tsx
│   ├── services/           # API服务
│   │   ├── api.ts
│   │   └── authApi.ts
│   ├── stores/             # 状态管理
│   │   └── authStore.ts
│   ├── types/              # TypeScript类型
│   │   └── index.ts
│   ├── App.tsx             # 主应用组件
│   ├── main.tsx            # 应用入口
│   └── index.css           # 全局样式
├── public/                  # 公共资源
├── index.html              # HTML模板
├── vite.config.js          # Vite配置
├── tailwind.config.js      # Tailwind CSS配置
├── tsconfig.json           # TypeScript配置
└── package.json            # 项目依赖
```

## 🎯 核心功能页面

### 1. 首页 (`/`)
- 产品介绍和特性展示
- 用户登录/注册入口
- 响应式设计

### 2. 用户认证
- **登录页面** (`/login`) - 用户登录表单
- **注册页面** (`/register`) - 用户注册表单

### 3. 用户控制台 (`/dashboard`)
- 用户概览统计
- 快速操作入口
- 最近论文列表
- 学习进度展示

### 4. 论文管理
- **上传页面** (`/upload`) - 拖拽上传论文文件
- **分析页面** (`/analysis/:sessionId`) - 实时分析进度

### 5. 学习功能
- **学习计划** (`/plan/:planId`) - 个性化学习路径
- **知识图谱** (`/graph/:sessionId`) - 交互式概念图谱

### 6. 系统管理
- **管理员页面** (`/admin`) - 用户审批和系统管理
- **用户设置** (`/settings`) - 个人偏好设置

## 🧩 组件库

### 基础 UI 组件

- **Button** - 多种样式和尺寸的按钮
- **Input** - 支持图标、验证、多种类型
- **Card** - 卡片容器，支持点击、悬停效果
- **Modal** - 模态框，支持确认对话框
- **Notification** - 通知提示，支持多种类型

### 高级组件

- **StatCard** - 统计数据卡片
- **PaperCard** - 论文信息卡片
- **DataTable** - 数据表格（带分页、排序）
- **Timeline** - 时间线组件

## 🔧 开发指南

### 添加新页面

1. 在 `src/js/pages/` 中创建页面组件
2. 在 `src/main.js` 中注册路由
3. 实现页面渲染逻辑

```javascript
// src/js/pages/MyPage.js
export function renderMyPage(context) {
  const app = document.getElementById('app')
  app.innerHTML = `<div>My Page Content</div>`
}

// src/main.js
router.route('/my-page', async (context) => {
  const { renderMyPage } = await import('./js/pages/MyPage.js')
  renderMyPage(context)
}, {
  title: 'My Page',
  requireAuth: false
})
```

### 创建新组件

遵循组件化设计原则：

```javascript
// src/js/components/ui/MyComponent.js
export class MyComponent {
  constructor(options = {}) {
    this.options = { ...defaultOptions, ...options }
  }

  createElement(children, props = {}) {
    // 创建 DOM 元素
    const element = document.createElement('div')
    // 应用样式和事件
    return element
  }

  static create(children, options = {}, props = {}) {
    const component = new MyComponent(options)
    return component.createElement(children, props)
  }
}
```

### API 集成

使用内置的 API 客户端：

```javascript
import { api, paperApi } from '../services/api.js'

// 通用 API 调用
const data = await api.get('/endpoint')

// 专用 API 服务
const papers = await paperApi.list()
```

## 🎨 样式系统

### Tailwind CSS 配置

项目使用定制的 Tailwind CSS 配置，包含：

- 品牌色彩系统（primary, accent, success, warning, error）
- 响应式断点
- 自定义动画和过渡效果
- 中文字体栈

### 设计 Token

```css
/* 主色调 */
--color-primary-500: #475569;
--color-accent-400: #22c55e;

/* 间距系统（8px 基准）*/
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-4: 1rem;     /* 16px */
```

## 🧪 测试

运行测试：

```bash
npm run test
```

类型检查：

```bash
npm run type-check
```

代码检查：

```bash
npm run lint
npm run lint:fix
```

## 📦 构建优化

### 代码分割

- 路由级别的代码分割
- 第三方库分包（vendor, utils）
- 动态导入优化

### 性能优化

- Tree-shaking 移除未使用代码
- 图片压缩和格式优化
- CSS 压缩和优化
- Gzip 压缩

## 🌐 浏览器支持

- Chrome 80+
- Firefox 80+
- Safari 13+
- Edge 80+

## 📱 移动端适配

- 触摸优化的交互
- 响应式布局
- 移动端导航菜单
- 适配不同屏幕尺寸

## 🔒 安全性

- XSS 防护
- CSRF 防护
- 安全的认证 Token 存储
- API 请求验证

## 🚀 部署

### 静态部署

构建后可以部署到任何静态文件服务器：

```bash
npm run build
# 将 dist/ 目录部署到服务器
```

### Docker 部署

```dockerfile
FROM nginx:alpine
COPY dist/ /usr/share/nginx/html/
EXPOSE 80
```

## 📝 更新日志

### v1.0.0 (2024-12-XX)
- ✨ 初始版本发布
- 🎨 完整的设计系统
- 📱 响应式界面
- 🔐 用户认证系统
- 📊 Dashboard 功能

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码变更
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 🆘 支持

如有问题或建议，请提交 Issue 或联系开发团队。