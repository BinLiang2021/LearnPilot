/**
 * 首页组件
 * 展示产品介绍、特性和登录入口
 */

import { Button } from '../components/ui/Button.js'
import { Card } from '../components/ui/Card.js'
import { userStorage } from '../utils/storage.js'
import { navigate } from '../utils/router.js'

/**
 * 渲染首页
 */
export function renderHomePage() {
  const app = document.getElementById('app')
  
  app.innerHTML = `
    <div class="min-h-screen bg-gradient-to-br from-primary-50 to-accent-50">
      <!-- 导航栏 -->
      <header class="bg-white shadow-sm">
        <nav class="container-responsive py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
              <h1 class="text-xl font-bold text-gray-900">LearnPilot</h1>
            </div>
            <div class="flex items-center space-x-4" id="nav-actions">
              <!-- 导航按钮将在这里插入 -->
            </div>
          </div>
        </nav>
      </header>

      <main>
        <!-- Hero 区域 -->
        <section class="py-20">
          <div class="container-responsive text-center">
            <h1 class="heading-1 mb-6 gradient-text">
              AI 驱动的研究论文学习助手
            </h1>
            <p class="body-large mb-8 max-w-2xl mx-auto">
              使用人工智能技术智能分析研究论文，自动提取核心概念，构建知识图谱，
              为您生成个性化的学习计划，让学术研究更高效、更深入。
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center" id="hero-actions">
              <!-- 英雄区按钮将在这里插入 -->
            </div>
          </div>
        </section>

        <!-- 特性介绍 -->
        <section class="py-16 bg-white">
          <div class="container-responsive">
            <div class="text-center mb-16">
              <h2 class="heading-2 mb-4">核心特性</h2>
              <p class="body-large text-gray-600">
                为研究人员和学者量身定制的智能学习工具
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="features">
              <!-- 特性卡片将在这里插入 -->
            </div>
          </div>
        </section>

        <!-- 工作流程 -->
        <section class="py-16 bg-gray-50">
          <div class="container-responsive">
            <div class="text-center mb-16">
              <h2 class="heading-2 mb-4">简单三步，开启智能学习</h2>
              <p class="body-large text-gray-600">
                从上传论文到获得个性化学习计划
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8" id="workflow">
              <!-- 工作流程步骤将在这里插入 -->
            </div>
          </div>
        </section>

        <!-- CTA 区域 -->
        <section class="py-20 bg-gradient-primary text-white">
          <div class="container-responsive text-center">
            <h2 class="heading-2 mb-4">准备开始您的智能学习之旅？</h2>
            <p class="body-large mb-8 opacity-90">
              加入 LearnPilot，让AI助力您的学术研究
            </p>
            <div id="cta-actions">
              <!-- CTA 按钮将在这里插入 -->
            </div>
          </div>
        </section>
      </main>

      <!-- 页脚 -->
      <footer class="bg-gray-900 text-gray-300 py-12">
        <div class="container-responsive">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-4">
              <div class="flex items-center space-x-2">
                <div class="w-6 h-6 bg-gradient-primary rounded flex items-center justify-center">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <span class="font-semibold text-white">LearnPilot</span>
              </div>
              <p class="text-sm">
                AI驱动的研究论文学习助手，让学术研究更高效。
              </p>
            </div>
            
            <div>
              <h3 class="font-semibold text-white mb-4">产品</h3>
              <ul class="space-y-2 text-sm">
                <li><a href="#" class="hover:text-white">特性介绍</a></li>
                <li><a href="#" class="hover:text-white">定价方案</a></li>
                <li><a href="#" class="hover:text-white">API文档</a></li>
              </ul>
            </div>
            
            <div>
              <h3 class="font-semibold text-white mb-4">支持</h3>
              <ul class="space-y-2 text-sm">
                <li><a href="#" class="hover:text-white">帮助中心</a></li>
                <li><a href="#" class="hover:text-white">联系我们</a></li>
                <li><a href="#" class="hover:text-white">意见反馈</a></li>
              </ul>
            </div>
            
            <div>
              <h3 class="font-semibold text-white mb-4">公司</h3>
              <ul class="space-y-2 text-sm">
                <li><a href="#" class="hover:text-white">关于我们</a></li>
                <li><a href="#" class="hover:text-white">隐私政策</a></li>
                <li><a href="#" class="hover:text-white">服务条款</a></li>
              </ul>
            </div>
          </div>
          
          <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2024 LearnPilot. 保留所有权利。</p>
          </div>
        </div>
      </footer>
    </div>
  `
  
  // 渲染动态内容
  renderNavActions()
  renderHeroActions()
  renderFeatures()
  renderWorkflow()
  renderCTAActions()
}

/**
 * 渲染导航栏操作按钮
 */
function renderNavActions() {
  const container = document.getElementById('nav-actions')
  const isLoggedIn = !!userStorage.getToken()
  
  if (isLoggedIn) {
    // 已登录状态
    const dashboardBtn = Button.create('进入控制台', {
      variant: 'primary',
      size: 'sm'
    }, {
      onClick: () => navigate('/dashboard')
    })
    
    container.appendChild(dashboardBtn)
  } else {
    // 未登录状态
    const loginBtn = Button.create('登录', {
      variant: 'ghost',
      size: 'sm'
    }, {
      onClick: () => navigate('/login')
    })
    
    const registerBtn = Button.create('注册', {
      variant: 'primary',
      size: 'sm'
    }, {
      onClick: () => navigate('/register')
    })
    
    container.appendChild(loginBtn)
    container.appendChild(registerBtn)
  }
}

/**
 * 渲染Hero区域操作按钮
 */
function renderHeroActions() {
  const container = document.getElementById('hero-actions')
  const isLoggedIn = !!userStorage.getToken()
  
  if (isLoggedIn) {
    const dashboardBtn = Button.create('进入控制台', {
      variant: 'primary',
      size: 'lg'
    }, {
      onClick: () => navigate('/dashboard')
    })
    
    const uploadBtn = Button.create('上传论文', {
      variant: 'secondary',
      size: 'lg'
    }, {
      onClick: () => navigate('/upload')
    })
    
    container.appendChild(dashboardBtn)
    container.appendChild(uploadBtn)
  } else {
    const registerBtn = Button.create('免费开始', {
      variant: 'primary',
      size: 'lg'
    }, {
      onClick: () => navigate('/register')
    })
    
    const demoBtn = Button.create('查看演示', {
      variant: 'secondary',
      size: 'lg'
    }, {
      onClick: () => {
        // TODO: 添加演示视频或交互演示
        console.log('显示演示')
      }
    })
    
    container.appendChild(registerBtn)
    container.appendChild(demoBtn)
  }
}

/**
 * 渲染特性卡片
 */
function renderFeatures() {
  const container = document.getElementById('features')
  
  const features = [
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
             </svg>`,
      title: 'AI智能分析',
      description: '利用先进的自然语言处理技术，自动分析论文内容，提取关键信息和核心概念。'
    },
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M13 10V3L4 14h7v7l9-11h-7z"></path>
             </svg>`,
      title: '知识图谱',
      description: '构建概念间的关联关系，以可视化图谱的形式呈现知识结构，帮助理解复杂概念。'
    },
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
             </svg>`,
      title: '个性化学习计划',
      description: '根据您的学习目标和时间安排，生成定制化的学习路径和进度计划。'
    },
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
             </svg>`,
      title: '多格式支持',
      description: '支持PDF、Markdown等多种文档格式，轻松导入各类学术论文和研究资料。'
    },
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
             </svg>`,
      title: '协作学习',
      description: '支持团队协作，分享学习计划和研究成果，促进学术交流与合作。'
    },
    {
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
             </svg>`,
      title: '数据安全',
      description: '采用企业级安全措施，确保您的研究数据和隐私信息得到最佳保护。'
    }
  ]
  
  features.forEach(feature => {
    const featureCard = Card.create(`
      <div class="text-center">
        <div class="w-16 h-16 mx-auto mb-6 bg-primary-100 text-primary-600 rounded-xl flex items-center justify-center">
          ${feature.icon}
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-3">${feature.title}</h3>
        <p class="text-gray-600">${feature.description}</p>
      </div>
    `, {
      padding: 'lg',
      hoverable: true
    })
    
    container.appendChild(featureCard)
  })
}

/**
 * 渲染工作流程
 */
function renderWorkflow() {
  const container = document.getElementById('workflow')
  
  const steps = [
    {
      step: '01',
      title: '上传论文',
      description: '支持拖拽上传PDF或Markdown格式的研究论文',
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
             </svg>`
    },
    {
      step: '02',
      title: 'AI分析',
      description: '智能提取核心概念，构建知识关系图谱',
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M13 10V3L4 14h7v7l9-11h-7z"></path>
             </svg>`
    },
    {
      step: '03',
      title: '学习计划',
      description: '生成个性化学习路径和进度安排',
      icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
             </svg>`
    }
  ]
  
  steps.forEach((step, index) => {
    const stepCard = Card.create(`
      <div class="text-center">
        <div class="relative mb-6">
          <div class="w-16 h-16 mx-auto bg-accent-100 text-accent-600 rounded-xl flex items-center justify-center">
            ${step.icon}
          </div>
          <div class="absolute -top-2 -right-2 w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
            ${step.step}
          </div>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-3">${step.title}</h3>
        <p class="text-gray-600">${step.description}</p>
      </div>
    `, {
      padding: 'lg'
    })
    
    container.appendChild(stepCard)
  })
}

/**
 * 渲染CTA按钮
 */
function renderCTAActions() {
  const container = document.getElementById('cta-actions')
  const isLoggedIn = !!userStorage.getToken()
  
  if (isLoggedIn) {
    const dashboardBtn = Button.create('进入控制台', {
      variant: 'secondary',
      size: 'lg'
    }, {
      onClick: () => navigate('/dashboard'),
      className: 'bg-white text-primary-600 hover:bg-gray-100'
    })
    
    container.appendChild(dashboardBtn)
  } else {
    const registerBtn = Button.create('立即开始', {
      variant: 'secondary',
      size: 'lg'
    }, {
      onClick: () => navigate('/register'),
      className: 'bg-white text-primary-600 hover:bg-gray-100'
    })
    
    container.appendChild(registerBtn)
  }
}