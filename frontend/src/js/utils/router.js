/**
 * 简单的SPA路由系统
 * 基于History API实现
 */

export class Router {
  constructor() {
    this.routes = new Map()
    this.middlewares = []
    this.currentRoute = null
    this.isNavigating = false
    
    // 绑定浏览器前进后退事件
    window.addEventListener('popstate', (e) => {
      this.handlePopState(e)
    })
  }

  /**
   * 定义路由
   */
  route(path, handler, options = {}) {
    this.routes.set(path, {
      handler,
      options: {
        title: '',
        requireAuth: false,
        layout: 'default',
        ...options
      }
    })
    return this
  }

  /**
   * 添加中间件
   */
  use(middleware) {
    this.middlewares.push(middleware)
    return this
  }

  /**
   * 导航到指定路径
   */
  navigate(path, state = null, replace = false) {
    if (this.isNavigating) return
    this.isNavigating = true
    
    try {
      // 更新浏览器历史
      if (replace) {
        history.replaceState(state, '', path)
      } else {
        history.pushState(state, '', path)
      }
      
      // 处理路由
      this.handleRoute(path, state)
    } finally {
      this.isNavigating = false
    }
  }

  /**
   * 替换当前路由
   */
  replace(path, state = null) {
    this.navigate(path, state, true)
  }

  /**
   * 返回上一页
   */
  back() {
    history.back()
  }

  /**
   * 前进下一页
   */
  forward() {
    history.forward()
  }

  /**
   * 启动路由
   */
  start() {
    const currentPath = window.location.pathname + window.location.search
    this.handleRoute(currentPath, history.state)
  }

  /**
   * 处理浏览器前进后退
   */
  handlePopState(e) {
    const currentPath = window.location.pathname + window.location.search
    this.handleRoute(currentPath, e.state)
  }

  /**
   * 处理路由
   */
  async handleRoute(path, state) {
    const route = this.matchRoute(path)
    
    if (!route) {
      this.handleNotFound(path)
      return
    }

    // 创建路由上下文
    const context = {
      path,
      route: route.route,
      params: route.params,
      query: this.parseQuery(path),
      state,
      router: this
    }

    try {
      // 执行中间件
      for (const middleware of this.middlewares) {
        const result = await middleware(context)
        if (result === false) {
          // 中间件阻止了导航
          return
        }
      }

      // 检查权限
      if (route.route.options.requireAuth && !this.checkAuth(context)) {
        this.handleUnauthorized(context)
        return
      }

      // 设置页面标题
      if (route.route.options.title) {
        document.title = route.route.options.title + ' | LearnPilot'
      }

      // 执行路由处理器
      this.currentRoute = context
      await route.route.handler(context)
      
    } catch (error) {
      console.error('路由处理错误:', error)
      this.handleError(error, context)
    }
  }

  /**
   * 匹配路由
   */
  matchRoute(path) {
    // 移除查询参数
    const pathname = path.split('?')[0]
    
    for (const [pattern, route] of this.routes) {
      const match = this.matchPattern(pattern, pathname)
      if (match) {
        return {
          route,
          params: match.params
        }
      }
    }
    
    return null
  }

  /**
   * 模式匹配
   */
  matchPattern(pattern, path) {
    // 处理动态路由参数
    const patternSegments = pattern.split('/')
    const pathSegments = path.split('/')
    
    if (patternSegments.length !== pathSegments.length) {
      return null
    }
    
    const params = {}
    
    for (let i = 0; i < patternSegments.length; i++) {
      const patternSegment = patternSegments[i]
      const pathSegment = pathSegments[i]
      
      if (patternSegment.startsWith(':')) {
        // 动态参数
        const paramName = patternSegment.slice(1)
        params[paramName] = decodeURIComponent(pathSegment)
      } else if (patternSegment !== pathSegment) {
        // 静态段不匹配
        return null
      }
    }
    
    return { params }
  }

  /**
   * 解析查询参数
   */
  parseQuery(path) {
    const queryString = path.split('?')[1]
    if (!queryString) return {}
    
    const params = new URLSearchParams(queryString)
    const query = {}
    
    for (const [key, value] of params) {
      query[key] = value
    }
    
    return query
  }

  /**
   * 检查认证状态
   */
  checkAuth(context) {
    // 这里可以检查用户是否已登录
    const token = localStorage.getItem('auth_token')
    return !!token
  }

  /**
   * 处理未找到的路由
   */
  handleNotFound(path) {
    console.warn('路由未找到:', path)
    // 可以导航到404页面
    this.showNotFoundPage()
  }

  /**
   * 处理未授权访问
   */
  handleUnauthorized(context) {
    console.warn('未授权访问:', context.path)
    // 保存当前路径，登录后返回
    sessionStorage.setItem('redirect_after_login', context.path)
    this.navigate('/login')
  }

  /**
   * 处理错误
   */
  handleError(error, context) {
    console.error('路由错误:', error)
    this.showErrorPage(error)
  }

  /**
   * 显示404页面
   */
  showNotFoundPage() {
    const app = document.getElementById('app')
    app.innerHTML = `
      <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center">
          <h1 class="text-6xl font-bold text-gray-400 mb-4">404</h1>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">页面未找到</h2>
          <p class="text-gray-600 mb-8">抱歉，您访问的页面不存在。</p>
          <button 
            onclick="router.navigate('/')"
            class="btn btn-primary"
          >
            返回首页
          </button>
        </div>
      </div>
    `
  }

  /**
   * 显示错误页面
   */
  showErrorPage(error) {
    const app = document.getElementById('app')
    app.innerHTML = `
      <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center">
          <h1 class="text-6xl font-bold text-red-400 mb-4">错误</h1>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">系统异常</h2>
          <p class="text-gray-600 mb-8">${error.message || '发生了未知错误'}</p>
          <button 
            onclick="location.reload()"
            class="btn btn-primary"
          >
            刷新页面
          </button>
        </div>
      </div>
    `
  }

  /**
   * 获取当前路由信息
   */
  getCurrentRoute() {
    return this.currentRoute
  }

  /**
   * 构建URL
   */
  buildUrl(path, params = {}, query = {}) {
    let url = path
    
    // 替换路径参数
    Object.entries(params).forEach(([key, value]) => {
      url = url.replace(`:${key}`, encodeURIComponent(value))
    })
    
    // 添加查询参数
    const queryParams = new URLSearchParams(query)
    if (queryParams.toString()) {
      url += '?' + queryParams.toString()
    }
    
    return url
  }
}

/**
 * 路由中间件
 */

// 认证中间件
export function authMiddleware(context) {
  if (context.route.options.requireAuth) {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      sessionStorage.setItem('redirect_after_login', context.path)
      context.router.navigate('/login')
      return false
    }
  }
  return true
}

// 加载中间件
export function loadingMiddleware(context) {
  // 显示加载状态
  const app = document.getElementById('app')
  const loading = document.createElement('div')
  loading.className = 'loading-overlay fixed inset-0 bg-white bg-opacity-75 flex items-center justify-center z-50'
  loading.innerHTML = `
    <div class="text-center">
      <div class="spinner w-8 h-8 mx-auto mb-4"></div>
      <p class="text-gray-600">页面加载中...</p>
    </div>
  `
  
  // 添加到页面
  document.body.appendChild(loading)
  
  // 在路由处理完成后移除
  setTimeout(() => {
    const existingLoading = document.querySelector('.loading-overlay')
    if (existingLoading) {
      existingLoading.remove()
    }
  }, 100)
  
  return true
}

// 创建全局路由实例
export const router = new Router()

// 导出便利函数
export function navigate(path, state = null) {
  return router.navigate(path, state)
}

export function replace(path, state = null) {
  return router.replace(path, state)
}

export function back() {
  return router.back()
}

export function forward() {
  return router.forward()
}