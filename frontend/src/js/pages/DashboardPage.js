/**
 * 用户控制台页面
 */

import { Button } from '../components/ui/Button.js'
import { Card, StatCard, PaperCard } from '../components/ui/Card.js'
import { showError } from '../components/ui/Notification.js'
import { paperApi, userApi } from '../services/api.js'
import { userStorage } from '../utils/storage.js'
import { navigate } from '../utils/router.js'
import { formatTime } from '../utils/helpers.js'

/**
 * 渲染Dashboard页面
 */
export function renderDashboardPage(context) {
  const app = document.getElementById('app')
  const user = userStorage.getUser()
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50">
      <!-- 顶部导航栏 -->
      <nav class="bg-white shadow-sm border-b border-gray-200">
        <div class="container-responsive py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
              <h1 class="text-xl font-bold text-gray-900">LearnPilot</h1>
            </div>
            
            <div class="flex items-center space-x-4">
              <div class="hidden md:block text-sm text-gray-600">
                欢迎回来，${user?.name || '用户'}！
              </div>
              
              <!-- 用户菜单 -->
              <div class="relative" id="user-menu">
                <button 
                  class="flex items-center space-x-2 text-gray-700 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100"
                  id="user-menu-button"
                >
                  <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-sm font-medium text-primary-600">
                      ${user?.name?.charAt(0)?.toUpperCase() || 'U'}
                    </span>
                  </div>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>
                
                <!-- 下拉菜单 -->
                <div 
                  class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 hidden"
                  id="user-menu-dropdown"
                >
                  <a href="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">设置</a>
                  <div class="border-t border-gray-100"></div>
                  <button 
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    id="logout-button"
                  >
                    退出登录
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main class="container-responsive py-8">
        <!-- 页面标题 -->
        <div class="mb-8">
          <h1 class="heading-2 mb-2">控制台</h1>
          <p class="text-gray-600">管理您的论文和学习计划</p>
        </div>

        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8" id="stats-cards">
          <!-- 统计卡片将在这里渲染 -->
        </div>

        <!-- 快速操作 -->
        <div class="mb-8">
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">快速操作</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="quick-actions">
              <!-- 快速操作按钮将在这里渲染 -->
            </div>
          </div>
        </div>

        <!-- 最近论文 -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold text-gray-900">最近论文</h2>
            <a href="/papers" class="text-primary-600 hover:text-primary-500 text-sm font-medium">
              查看全部 →
            </a>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="recent-papers">
            <!-- 最近论文卡片将在这里渲染 -->
          </div>
        </div>

        <!-- 学习进度 -->
        <div>
          <h2 class="text-lg font-semibold text-gray-900 mb-6">学习进度</h2>
          <div id="learning-progress">
            <!-- 学习进度内容将在这里渲染 -->
          </div>
        </div>
      </main>
    </div>
  `
  
  // 初始化页面组件
  initUserMenu()
  renderStatsCards()
  renderQuickActions()
  loadRecentPapers()
  renderLearningProgress()
}

/**
 * 初始化用户菜单
 */
function initUserMenu() {
  const menuButton = document.getElementById('user-menu-button')
  const menuDropdown = document.getElementById('user-menu-dropdown')
  const logoutButton = document.getElementById('logout-button')
  
  // 切换菜单显示
  menuButton.addEventListener('click', (e) => {
    e.stopPropagation()
    menuDropdown.classList.toggle('hidden')
  })
  
  // 点击外部关闭菜单
  document.addEventListener('click', () => {
    menuDropdown.classList.add('hidden')
  })
  
  // 退出登录
  logoutButton.addEventListener('click', () => {
    if (window.app) {
      window.app.logout()
    } else {
      userStorage.removeToken()
      userStorage.removeUser()
      navigate('/login')
    }
  })
}

/**
 * 渲染统计卡片
 */
function renderStatsCards() {
  const container = document.getElementById('stats-cards')
  
  // 示例数据，实际应该从API获取
  const stats = [
    {
      title: '总论文数',
      value: '12',
      change: 20,
      trend: 'up',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
             </svg>`
    },
    {
      title: '已完成分析',
      value: '8',
      change: 14,
      trend: 'up',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
             </svg>`
    },
    {
      title: '学习计划',
      value: '3',
      change: 0,
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
             </svg>`
    },
    {
      title: '本周学习时长',
      value: '8.5h',
      change: 25,
      trend: 'up',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
             </svg>`
    }
  ]
  
  stats.forEach(stat => {
    const statCard = StatCard.create(stat)
    container.appendChild(statCard)
  })
}

/**
 * 渲染快速操作
 */
function renderQuickActions() {
  const container = document.getElementById('quick-actions')
  
  const actions = [
    {
      title: '上传论文',
      description: '添加新的研究论文',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
             </svg>`,
      action: () => navigate('/upload')
    },
    {
      title: '查看知识图谱',
      description: '浏览概念关系图',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M13 10V3L4 14h7v7l9-11h-7z"></path>
             </svg>`,
      action: () => showError('请先完成论文分析')
    },
    {
      title: '学习计划',
      description: '制定学习安排',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 4h.01M9 12h.01M9 16h.01M13 8h3m-3 4h3m-3 4h3"></path>
             </svg>`,
      action: () => showError('请先完成论文分析')
    },
    {
      title: '数据分析',
      description: '查看学习统计',
      icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                     d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
             </svg>`,
      action: () => showError('功能开发中')
    }
  ]
  
  actions.forEach(action => {
    const actionCard = Card.create(`
      <div class="text-center">
        <div class="w-12 h-12 mx-auto mb-3 bg-primary-100 text-primary-600 rounded-lg flex items-center justify-center">
          ${action.icon}
        </div>
        <h3 class="font-medium text-gray-900 mb-1">${action.title}</h3>
        <p class="text-sm text-gray-500">${action.description}</p>
      </div>
    `, {
      clickable: true,
      padding: 'md'
    }, {
      onClick: action.action
    })
    
    container.appendChild(actionCard)
  })
}

/**
 * 加载最近论文
 */
async function loadRecentPapers() {
  const container = document.getElementById('recent-papers')
  
  // 显示加载状态
  container.innerHTML = `
    <div class="col-span-full text-center py-8">
      <div class="spinner w-8 h-8 mx-auto mb-4"></div>
      <p class="text-gray-500">加载中...</p>
    </div>
  `
  
  try {
    // 这里应该调用实际的API
    // const papers = await paperApi.list({ limit: 6 })
    
    // 使用示例数据
    setTimeout(() => {
      const papers = [
        {
          id: '1',
          title: 'Attention Is All You Need',
          authors: ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar'],
          abstract: 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...',
          status: 'completed',
          uploadedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          title: 'BERT: Pre-training of Deep Bidirectional Transformers',
          authors: ['Jacob Devlin', 'Ming-Wei Chang', 'Kenton Lee'],
          abstract: 'We introduce a new language representation model called BERT...',
          status: 'analyzing',
          uploadedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          title: 'GPT-3: Language Models are Few-Shot Learners',
          authors: ['Tom B. Brown', 'Benjamin Mann', 'Nick Ryder'],
          abstract: 'Recent work has demonstrated substantial gains on many NLP tasks and benchmarks...',
          status: 'uploading',
          uploadedAt: new Date().toISOString()
        }
      ]
      
      renderRecentPapers(papers)
    }, 1000)
    
  } catch (error) {
    console.error('加载论文失败:', error)
    container.innerHTML = `
      <div class="col-span-full text-center py-8">
        <p class="text-gray-500">加载失败，请刷新重试</p>
      </div>
    `
  }
}

/**
 * 渲染最近论文
 */
function renderRecentPapers(papers) {
  const container = document.getElementById('recent-papers')
  
  if (papers.length === 0) {
    container.innerHTML = `
      <div class="col-span-full text-center py-12">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">还没有论文</h3>
        <p class="text-gray-500 mb-4">上传您的第一篇研究论文开始学习之旅</p>
        <button class="btn btn-primary" onclick="router.navigate('/upload')">
          上传论文
        </button>
      </div>
    `
    return
  }
  
  container.innerHTML = ''
  
  papers.forEach(paper => {
    const paperCard = PaperCard.create(paper, {}, {
      onClick: () => {
        // 根据状态导航到不同页面
        if (paper.status === 'completed') {
          navigate(`/analysis/${paper.id}`)
        } else if (paper.status === 'analyzing') {
          navigate(`/analysis/${paper.id}`)
        } else {
          showError('论文还在处理中，请稍后查看')
        }
      }
    })
    
    container.appendChild(paperCard)
  })
}

/**
 * 渲染学习进度
 */
function renderLearningProgress() {
  const container = document.getElementById('learning-progress')
  
  container.innerHTML = `
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="text-center py-12">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">暂无学习进度</h3>
        <p class="text-gray-500">完成论文分析后，系统将为您生成学习进度报告</p>
      </div>
    </div>
  `
}