/**
 * LearnPilot 前端应用入口
 */

import './styles/main.css'

// 导入核心模块
import { router, authMiddleware, loadingMiddleware } from './js/utils/router.js'
import { userStorage } from './js/utils/storage.js'
import { authApi } from './js/services/api.js'

// 导入页面组件
import './js/pages/HomePage.js'
import './js/pages/LoginPage.js'
import './js/pages/RegisterPage.js'
import './js/pages/DashboardPage.js'
import './js/pages/UploadPage.js'
import './js/pages/AnalysisPage.js'
import './js/pages/PlanPage.js'
import './js/pages/GraphPage.js'
import './js/pages/AdminPage.js'

/**
 * 应用类
 */
class App {
  constructor() {
    this.isInitialized = false
    this.user = null
  }

  /**
   * 初始化应用
   */
  async init() {
    if (this.isInitialized) return
    
    console.log('LearnPilot 正在启动...')
    
    try {
      // 检查用户认证状态
      await this.checkAuthStatus()
      
      // 设置路由中间件
      this.setupMiddlewares()
      
      // 注册路由
      this.registerRoutes()
      
      // 启动路由
      router.start()
      
      this.isInitialized = true
      console.log('LearnPilot 启动成功')
      
    } catch (error) {
      console.error('应用启动失败:', error)
      this.showErrorPage(error)
    }
  }

  /**
   * 检查认证状态
   */
  async checkAuthStatus() {
    const token = userStorage.getToken()
    if (!token) return
    
    try {
      const user = await authApi.me()
      this.user = user
      userStorage.setUser(user)
    } catch (error) {
      console.warn('用户认证失效:', error)
      userStorage.removeToken()
      userStorage.removeUser()
    }
  }

  /**
   * 设置路由中间件
   */
  setupMiddlewares() {
    router.use(loadingMiddleware)
    router.use(authMiddleware)
  }

  /**
   * 注册路由
   */
  registerRoutes() {
    // 首页
    router.route('/', async (context) => {
      const { renderHomePage } = await import('./js/pages/HomePage.js')
      renderHomePage()
    }, {
      title: 'AI驱动的研究论文学习助手'
    })

    // 登录页
    router.route('/login', async (context) => {
      const { renderLoginPage } = await import('./js/pages/LoginPage.js')
      renderLoginPage(context)
    }, {
      title: '登录'
    })

    // 注册页
    router.route('/register', async (context) => {
      const { renderRegisterPage } = await import('./js/pages/RegisterPage.js')
      renderRegisterPage(context)
    }, {
      title: '注册'
    })

    // 用户仪表板
    router.route('/dashboard', async (context) => {
      const { renderDashboardPage } = await import('./js/pages/DashboardPage.js')
      renderDashboardPage(context)
    }, {
      title: '控制台',
      requireAuth: true
    })

    // 论文上传
    router.route('/upload', async (context) => {
      const { renderUploadPage } = await import('./js/pages/UploadPage.js')
      renderUploadPage(context)
    }, {
      title: '上传论文',
      requireAuth: true
    })

    // 分析进度
    router.route('/analysis/:sessionId', async (context) => {
      const { renderAnalysisPage } = await import('./js/pages/AnalysisPage.js')
      renderAnalysisPage(context)
    }, {
      title: '分析进度',
      requireAuth: true
    })

    // 学习计划
    router.route('/plan/:planId', async (context) => {
      const { renderPlanPage } = await import('./js/pages/PlanPage.js')
      renderPlanPage(context)
    }, {
      title: '学习计划',
      requireAuth: true
    })

    // 知识图谱
    router.route('/graph/:sessionId', async (context) => {
      const { renderGraphPage } = await import('./js/pages/GraphPage.js')
      renderGraphPage(context)
    }, {
      title: '知识图谱',
      requireAuth: true
    })

    // 管理员页面
    router.route('/admin', async (context) => {
      const { renderAdminPage } = await import('./js/pages/AdminPage.js')
      renderAdminPage(context)
    }, {
      title: '管理员',
      requireAuth: true,
      requireAdmin: true
    })

    // 用户设置
    router.route('/settings', async (context) => {
      const { renderSettingsPage } = await import('./js/pages/SettingsPage.js')
      renderSettingsPage(context)
    }, {
      title: '设置',
      requireAuth: true
    })
  }

  /**
   * 显示错误页面
   */
  showErrorPage(error) {
    const app = document.getElementById('app')
    app.innerHTML = `
      <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center max-w-md">
          <div class="mb-4">
            <svg class="w-16 h-16 text-red-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">启动失败</h1>
          <p class="text-gray-600 mb-4">应用启动时遇到错误：${error.message}</p>
          <button 
            onclick="location.reload()" 
            class="btn btn-primary"
          >
            重新加载
          </button>
        </div>
      </div>
    `
  }

  /**
   * 获取当前用户
   */
  getCurrentUser() {
    return this.user
  }

  /**
   * 设置当前用户
   */
  setCurrentUser(user) {
    this.user = user
  }

  /**
   * 登出
   */
  logout() {
    this.user = null
    userStorage.removeToken()
    userStorage.removeUser()
    router.navigate('/login')
  }
}

// 创建全局应用实例
const app = new App()

// 导出到全局
window.app = app
window.router = router

// 等待DOM加载完成后启动应用
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    app.init()
  })
} else {
  app.init()
}

// 导出应用实例
export default app