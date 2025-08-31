# LearnPilot 设计系统 v2.0

## 🎨 视觉设计理念

### 设计原则
1. **学术专业** - 体现科研严谨性和权威性
2. **智能友好** - 突出AI技术的先进性和易用性  
3. **学习导向** - 优化知识获取和学习体验
4. **无障碍包容** - 确保所有用户都能高效使用

## 🌈 颜色系统

### 主色调 (Primary Colors)
```css
:root {
  /* 主品牌色 - 深蓝学术色 */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #3b82f6;  /* 主色 */
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  --primary-800: #1e40af;
  --primary-900: #1e3a8a;
}
```

### 辅助色调 (Secondary Colors)
```css
:root {
  /* 辅助色 - 温暖橙色，突出AI智能 */
  --secondary-50: #fff7ed;
  --secondary-100: #ffedd5;
  --secondary-200: #fed7aa;
  --secondary-300: #fdba74;
  --secondary-400: #fb923c;
  --secondary-500: #f97316;  /* 辅助色 */
  --secondary-600: #ea580c;
  --secondary-700: #c2410c;
  --secondary-800: #9a3412;
  --secondary-900: #7c2d12;
}
```

### 状态色 (Status Colors)
```css
:root {
  /* 成功色 */
  --success-50: #f0fdf4;
  --success-500: #22c55e;
  --success-700: #15803d;
  
  /* 警告色 */
  --warning-50: #fffbeb;
  --warning-500: #f59e0b;
  --warning-700: #b45309;
  
  /* 错误色 */
  --error-50: #fef2f2;
  --error-500: #ef4444;
  --error-700: #c53030;
  
  /* 信息色 */
  --info-50: #f0f9ff;
  --info-500: #3b82f6;
  --info-700: #1d4ed8;
}
```

### 中性色 (Neutral Colors)
```css
:root {
  /* 中性灰色系 */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
}
```

## 📚 字体系统

### 字体族
```css
:root {
  /* 主要字体 - 用于标题和重要内容 */
  --font-primary: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  
  /* 阅读字体 - 用于长文本和论文内容 */
  --font-reading: 'Source Serif Pro', 'Times New Roman', serif;
  
  /* 代码字体 - 用于代码和数据展示 */
  --font-mono: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', monospace;
  
  /* 中文字体 */
  --font-chinese: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
```

### 字体大小和行高
```css
:root {
  /* 字体大小 */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  
  /* 行高 */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  --leading-loose: 2;
}
```

## 📐 间距系统

### 间距标准
```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
}
```

### 布局容器
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.container-sm { max-width: 640px; }
.container-md { max-width: 768px; }
.container-lg { max-width: 1024px; }
.container-xl { max-width: 1280px; }
```

## 🔲 组件设计规范

### 按钮 (Buttons)
```css
/* 主要按钮 */
.btn-primary {
  background: var(--primary-500);
  color: white;
  border: none;
  border-radius: 8px;
  padding: var(--space-3) var(--space-6);
  font-weight: 600;
  font-size: var(--text-base);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-primary:hover {
  background: var(--primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

/* 次要按钮 */
.btn-secondary {
  background: transparent;
  color: var(--primary-500);
  border: 2px solid var(--primary-500);
  border-radius: 8px;
  padding: var(--space-3) var(--space-6);
  font-weight: 600;
  transition: all 0.2s ease;
}

/* 危险按钮 */
.btn-danger {
  background: var(--error-500);
  color: white;
}

/* 按钮尺寸 */
.btn-sm { 
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}

.btn-lg { 
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
}
```

### 表单元素
```css
/* 输入框 */
.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: var(--text-base);
  transition: border-color 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error {
  border-color: var(--error-500);
}

/* 标签 */
.form-label {
  display: block;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: var(--space-2);
  font-size: var(--text-sm);
}

/* 选择框 */
.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml...");
  background-repeat: no-repeat;
  background-position: right var(--space-3) center;
  padding-right: var(--space-8);
}
```

### 卡片 (Cards)
```css
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
  overflow: hidden;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-4) var(--space-6);
  background: var(--gray-50);
  border-top: 1px solid var(--gray-200);
}
```

### 导航 (Navigation)
```css
.navbar {
  background: white;
  border-bottom: 1px solid var(--gray-200);
  padding: var(--space-4) 0;
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(10px);
}

.nav-link {
  padding: var(--space-2) var(--space-4);
  color: var(--gray-600);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.active {
  color: var(--primary-500);
  background: var(--primary-50);
}
```

## 🎭 交互状态设计

### 加载状态
```css
/* 骨架屏 */
.skeleton {
  background: linear-gradient(90deg, 
    var(--gray-200) 25%, 
    var(--gray-100) 50%, 
    var(--gray-200) 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 加载指示器 */
.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--gray-200);
  border-top: 3px solid var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

### 进度指示
```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-500), var(--secondary-500));
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* 步骤指示器 */
.steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: var(--gray-500);
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: var(--primary-500);
  color: white;
}

.step.completed .step-circle {
  background: var(--success-500);
  color: white;
}
```

## 📱 响应式设计

### 断点系统
```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

/* 移动优先设计 */
@media (min-width: 640px) {
  .sm\:text-lg { font-size: var(--text-lg); }
  .sm\:p-6 { padding: var(--space-6); }
}

@media (min-width: 768px) {
  .md\:text-xl { font-size: var(--text-xl); }
  .md\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .lg\:text-2xl { font-size: var(--text-2xl); }
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
}
```

### 移动端优化
```css
/* 触摸友好的按钮尺寸 */
@media (max-width: 768px) {
  .btn {
    min-height: 44px;
    padding: var(--space-3) var(--space-5);
  }
  
  .form-input {
    min-height: 44px;
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .card {
    margin: var(--space-4);
    border-radius: 8px;
  }
}
```

## 🔧 实用工具类

### 间距工具
```css
/* 外边距 */
.m-0 { margin: 0; }
.m-4 { margin: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mr-4 { margin-right: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
.ml-4 { margin-left: var(--space-4); }

/* 内边距 */
.p-0 { padding: 0; }
.p-4 { padding: var(--space-4); }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-4 { padding-top: var(--space-4); padding-bottom: var(--space-4); }
```

### 布局工具
```css
/* Flexbox */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

/* Grid */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.gap-4 { gap: var(--space-4); }

/* 定位 */
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }
.sticky { position: sticky; }

/* 显示/隐藏 */
.hidden { display: none; }
.visible { visibility: visible; }
.invisible { visibility: hidden; }
```

### 文本工具
```css
/* 对齐 */
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

/* 字重 */
.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

/* 文本处理 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.text-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

## 🎨 主题系统

### 深色模式支持
```css
[data-theme="dark"] {
  --bg-primary: var(--gray-900);
  --bg-secondary: var(--gray-800);
  --text-primary: var(--gray-100);
  --text-secondary: var(--gray-300);
  --border-color: var(--gray-700);
}

/* 自动切换 */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: var(--gray-900);
    --text-primary: var(--gray-100);
  }
}
```

### 学术主题变体
```css
/* 学术蓝主题 */
[data-theme="academic"] {
  --primary-500: #1e40af;
  --secondary-500: #dc2626;
  --accent-color: #059669;
}

/* 研究橙主题 */
[data-theme="research"] {
  --primary-500: #ea580c;
  --secondary-500: #7c3aed;
  --accent-color: #0891b2;
}
```

## 🔍 可访问性设计

### 颜色对比度
- 所有文本与背景对比度 ≥ 4.5:1
- 大文本与背景对比度 ≥ 3:1
- UI组件边界对比度 ≥ 3:1

### 焦点状态
```css
.focus-visible:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
  .btn-primary {
    border: 2px solid currentColor;
  }
}

/* 减少动画 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 📏 使用指南

### 1. 组件优先级
1. **基础组件**：按钮、表单、卡片
2. **布局组件**：导航、侧边栏、网格
3. **反馈组件**：通知、加载、提示
4. **数据组件**：表格、图表、列表

### 2. 设计原则
- **一致性**：保持视觉和交互的一致性
- **简洁性**：减少不必要的视觉元素
- **功能性**：优先考虑功能和可用性
- **包容性**：确保所有用户都能使用

### 3. 实施建议
- 使用CSS变量确保主题一致性
- 采用移动优先的响应式设计
- 实现渐进式增强
- 定期进行可访问性测试

这个设计系统为LearnPilot提供了完整的视觉和交互基础，确保产品具有专业、现代且用户友好的界面。