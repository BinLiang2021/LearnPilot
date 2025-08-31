# LearnPilot Frontend 部署指南

## 🚀 快速启动

### 开发环境

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **使用启动脚本**
   ```bash
   ./start_frontend.sh
   ```

3. **或手动启动**
   ```bash
   npm install
   cp .env.example .env  # 首次运行
   npm run dev
   ```

4. **访问应用**
   
   打开浏览器访问: http://localhost:3000

### 生产环境构建

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 🏗️ 项目架构

### 技术栈
- **构建工具**: Vite 5.x
- **样式框架**: Tailwind CSS 3.x
- **JavaScript**: ES2015+ (Vanilla JS)
- **路由**: 自定义 SPA 路由系统
- **API客户端**: Fetch API + 拦截器

### 核心特性
- ✅ 现代化UI组件库
- ✅ 响应式设计（移动端适配）
- ✅ SPA路由系统
- ✅ 用户认证流程
- ✅ API集成和状态管理
- ✅ 错误处理和加载状态
- ✅ 通知系统
- ✅ 模态框组件

## 📱 页面结构

### 已实现页面

1. **首页 (`/`)**
   - 产品介绍和特性展示
   - 响应式设计
   - CTA按钮和导航

2. **用户认证**
   - 登录页面 (`/login`)
   - 注册页面 (`/register`)
   - 表单验证和错误处理

3. **用户控制台 (`/dashboard`)**
   - 统计卡片展示
   - 快速操作面板
   - 最近论文列表
   - 用户菜单和导航

4. **功能页面占位符**
   - 论文上传 (`/upload`)
   - 分析进度 (`/analysis/:sessionId`)
   - 学习计划 (`/plan/:planId`)
   - 知识图谱 (`/graph/:sessionId`)
   - 用户设置 (`/settings`)
   - 管理员页面 (`/admin`)

## 🎨 设计系统

### 颜色方案
```css
/* 主色系 */
--color-primary-500: #475569;
--color-accent-400: #22c55e;

/* 语义色彩 */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-info: #3b82f6;
```

### 组件库
- `Button` - 多样式按钮组件
- `Input` - 表单输入组件
- `Card` - 卡片容器组件
- `Modal` - 模态框组件
- `Notification` - 通知提示组件
- `StatCard` - 统计卡片组件
- `PaperCard` - 论文卡片组件

## 🔧 开发工具

### 脚本命令
```bash
npm run dev      # 开发服务器
npm run build    # 生产构建
npm run preview  # 预览构建结果
npm run lint     # 代码检查
npm run lint:fix # 修复代码问题
```

### 项目结构
```
frontend/
├── src/
│   ├── js/
│   │   ├── components/ui/     # UI组件
│   │   ├── pages/             # 页面组件
│   │   ├── services/          # API服务
│   │   └── utils/             # 工具函数
│   ├── styles/main.css        # 主样式文件
│   └── main.js               # 应用入口
├── public/                   # 静态资源
├── dist/                     # 构建输出
└── package.json             # 项目配置
```

## 🌐 API集成

### API客户端配置
```javascript
// 环境变量配置
VITE_API_BASE_URL=http://localhost:8000/api

// API服务模块
import { authApi, paperApi, userApi } from './services/api.js'
```

### 认证流程
1. 用户登录/注册
2. Token存储到localStorage
3. API请求自动添加认证头
4. Token过期自动跳转登录

## 📦 构建和部署

### 构建配置
- **目标**: ES2015 (兼容现代浏览器)
- **代码分割**: 路由级别 + 第三方库分包
- **优化**: Tree-shaking + 代码压缩
- **兼容性**: Legacy浏览器支持

### 部署选项

**1. 静态文件服务器**
```bash
npm run build
# 将 dist/ 目录部署到 Nginx/Apache
```

**2. Docker部署**
```dockerfile
FROM nginx:alpine
COPY dist/ /usr/share/nginx/html/
EXPOSE 80
```

**3. CDN部署**
- 支持部署到 Vercel, Netlify, GitHub Pages 等

## 🔒 安全性

- XSS防护（DOM操作转义）
- CSRF保护（API Token验证）
- 安全的Token存储
- 输入验证和过滤

## 📊 性能指标

### 构建结果
- **主包大小**: ~21KB (Gzipped: ~7.6KB)
- **CSS大小**: ~26KB (Gzipped: ~5.1KB)
- **代码分割**: 支持按需加载

### 加载性能
- 首次加载: < 50KB (Gzipped)
- 路由切换: < 1s
- 组件懒加载: 支持

## 🐛 故障排除

### 常见问题

**1. 依赖安装失败**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**2. 构建错误**
- 检查Node.js版本 (推荐 16+)
- 确认环境变量配置
- 清理缓存后重新构建

**3. 开发服务器启动失败**
- 检查端口占用
- 确认项目路径正确
- 查看错误日志

**4. API连接问题**
- 确认后端服务运行
- 检查代理配置
- 验证CORS设置

## 📈 后续开发计划

### 待实现功能
1. 论文上传界面（拖拽上传）
2. 分析进度实时显示
3. 知识图谱可视化
4. 学习计划管理
5. 数据可视化图表

### 优化方向
1. 性能优化（虚拟滚动、懒加载）
2. 用户体验改进（骨架屏、过渡动画）
3. 无障碍性增强
4. 国际化支持
5. PWA功能

## 🆘 技术支持

如遇到问题，请：
1. 查看浏览器控制台错误
2. 检查网络请求状态
3. 确认环境配置正确
4. 提交Issue到项目仓库

---

**版本**: v1.0.0  
**更新时间**: 2024-12-XX  
**维护团队**: LearnPilot Development Team