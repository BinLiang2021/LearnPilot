/**
 * API客户端服务
 * 处理与后端API的通信
 */

import { userStorage, cacheStorage } from '../utils/storage.js'
import { showError } from '../components/ui/Notification.js'

class ApiClient {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL
    this.defaultHeaders = {
      'Content-Type': 'application/json'
    }
    this.interceptors = {
      request: [],
      response: []
    }
  }

  /**
   * 添加请求拦截器
   */
  addRequestInterceptor(interceptor) {
    this.interceptors.request.push(interceptor)
  }

  /**
   * 添加响应拦截器
   */
  addResponseInterceptor(interceptor) {
    this.interceptors.response.push(interceptor)
  }

  /**
   * 获取完整URL
   */
  getFullUrl(url) {
    if (url.startsWith('http')) return url
    return this.baseURL + (url.startsWith('/') ? url : `/${url}`)
  }

  /**
   * 获取请求头
   */
  getHeaders(customHeaders = {}) {
    const headers = { ...this.defaultHeaders, ...customHeaders }
    
    // 添加认证头
    const token = userStorage.getToken()
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
    
    return headers
  }

  /**
   * 处理请求拦截器
   */
  async processRequestInterceptors(config) {
    let processedConfig = config
    
    for (const interceptor of this.interceptors.request) {
      processedConfig = await interceptor(processedConfig)
    }
    
    return processedConfig
  }

  /**
   * 处理响应拦截器
   */
  async processResponseInterceptors(response) {
    let processedResponse = response
    
    for (const interceptor of this.interceptors.response) {
      processedResponse = await interceptor(processedResponse)
    }
    
    return processedResponse
  }

  /**
   * 发送HTTP请求
   */
  async request(config) {
    try {
      // 处理请求拦截器
      const processedConfig = await this.processRequestInterceptors(config)
      
      const {
        method = 'GET',
        url,
        data,
        headers = {},
        timeout = 30000,
        cache = false,
        cacheTime = 5 * 60 * 1000 // 5分钟
      } = processedConfig
      
      const fullUrl = this.getFullUrl(url)
      const finalHeaders = this.getHeaders(headers)
      
      // 检查缓存
      if (cache && method === 'GET') {
        const cacheKey = `${method}:${fullUrl}`
        const cachedData = cacheStorage.get(cacheKey)
        if (cachedData) {
          return cachedData
        }
      }
      
      // 构建请求选项
      const fetchOptions = {
        method,
        headers: finalHeaders
      }
      
      // 添加请求体
      if (data && method !== 'GET') {
        if (data instanceof FormData) {
          // FormData情况下移除Content-Type，让浏览器自动设置
          delete fetchOptions.headers['Content-Type']
          fetchOptions.body = data
        } else {
          fetchOptions.body = JSON.stringify(data)
        }
      }
      
      // 设置超时
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), timeout)
      fetchOptions.signal = controller.signal
      
      try {
        // 发送请求
        const response = await fetch(fullUrl, fetchOptions)
        clearTimeout(timeoutId)
        
        // 处理响应
        let responseData
        const contentType = response.headers.get('content-type')
        
        if (contentType && contentType.includes('application/json')) {
          responseData = await response.json()
        } else {
          responseData = await response.text()
        }
        
        if (!response.ok) {
          throw new ApiError(response.status, responseData.message || response.statusText, responseData)
        }
        
        // 处理响应拦截器
        const processedResponse = await this.processResponseInterceptors({
          data: responseData,
          status: response.status,
          headers: response.headers,
          config: processedConfig
        })
        
        // 缓存响应
        if (cache && method === 'GET') {
          const cacheKey = `${method}:${fullUrl}`
          cacheStorage.set(cacheKey, processedResponse.data, cacheTime)
        }
        
        return processedResponse.data
        
      } catch (error) {
        clearTimeout(timeoutId)
        
        if (error.name === 'AbortError') {
          throw new ApiError(408, '请求超时')
        }
        
        throw error
      }
      
    } catch (error) {
      console.error('API请求错误:', error)
      
      // 处理特定错误
      if (error instanceof ApiError) {
        this.handleApiError(error)
        throw error
      }
      
      // 网络错误
      const networkError = new ApiError(0, '网络连接失败，请检查网络设置')
      this.handleApiError(networkError)
      throw networkError
    }
  }

  /**
   * 处理API错误
   */
  handleApiError(error) {
    // 401 未授权 - 清除登录状态
    if (error.status === 401) {
      userStorage.removeToken()
      userStorage.removeUser()
      
      // 如果不是登录页面，跳转到登录页面
      if (!window.location.pathname.includes('/login')) {
        sessionStorage.setItem('redirect_after_login', window.location.pathname)
        window.location.href = '/login'
      }
      return
    }
    
    // 403 禁止访问
    if (error.status === 403) {
      showError('权限不足，无法访问该资源')
      return
    }
    
    // 404 未找到
    if (error.status === 404) {
      showError('请求的资源不存在')
      return
    }
    
    // 500 服务器错误
    if (error.status >= 500) {
      showError('服务器异常，请稍后重试')
      return
    }
    
    // 其他错误
    if (error.message && error.status !== 0) {
      showError(error.message)
    }
  }

  /**
   * GET请求
   */
  get(url, config = {}) {
    return this.request({ method: 'GET', url, ...config })
  }

  /**
   * POST请求
   */
  post(url, data = null, config = {}) {
    return this.request({ method: 'POST', url, data, ...config })
  }

  /**
   * PUT请求
   */
  put(url, data = null, config = {}) {
    return this.request({ method: 'PUT', url, data, ...config })
  }

  /**
   * PATCH请求
   */
  patch(url, data = null, config = {}) {
    return this.request({ method: 'PATCH', url, data, ...config })
  }

  /**
   * DELETE请求
   */
  delete(url, config = {}) {
    return this.request({ method: 'DELETE', url, ...config })
  }

  /**
   * 上传文件
   */
  upload(url, formData, onProgress = null, config = {}) {
    return this.request({
      method: 'POST',
      url,
      data: formData,
      headers: {}, // 让浏览器自动设置Content-Type
      onProgress,
      ...config
    })
  }

  /**
   * 下载文件
   */
  async download(url, filename = null) {
    try {
      const response = await fetch(this.getFullUrl(url), {
        headers: this.getHeaders()
      })
      
      if (!response.ok) {
        throw new ApiError(response.status, '下载失败')
      }
      
      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      
    } catch (error) {
      console.error('下载错误:', error)
      showError('文件下载失败')
      throw error
    }
  }
}

/**
 * API错误类
 */
class ApiError extends Error {
  constructor(status, message, data = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

// 创建API客户端实例
export const api = new ApiClient()

// 添加默认拦截器
api.addRequestInterceptor(async (config) => {
  console.log('API请求:', config.method, config.url)
  return config
})

api.addResponseInterceptor(async (response) => {
  console.log('API响应:', response.status, response.config.url)
  return response
})

/**
 * 具体的API服务
 */

// 认证相关API
export const authApi = {
  // 登录
  login(credentials) {
    return api.post('/auth/login', credentials)
  },
  
  // 注册
  register(userData) {
    return api.post('/auth/register', userData)
  },
  
  // 获取当前用户信息
  me() {
    return api.get('/auth/me', { cache: true })
  },
  
  // 刷新token
  refreshToken(refreshToken) {
    return api.post('/auth/refresh', { refreshToken })
  },
  
  // 登出
  logout() {
    return api.post('/auth/logout')
  },
  
  // 修改密码
  changePassword(data) {
    return api.post('/auth/change-password', data)
  },
  
  // 忘记密码
  forgotPassword(email) {
    return api.post('/auth/forgot-password', { email })
  },
  
  // 重置密码
  resetPassword(token, newPassword) {
    return api.post('/auth/reset-password', { token, newPassword })
  }
}

// 论文相关API
export const paperApi = {
  // 获取论文列表
  list(params = {}) {
    return api.get('/papers', { cache: true, cacheTime: 2 * 60 * 1000, params })
  },
  
  // 获取论文详情
  get(id) {
    return api.get(`/papers/${id}`, { cache: true })
  },
  
  // 上传论文
  upload(files, onProgress) {
    const formData = new FormData()
    if (Array.isArray(files)) {
      files.forEach(file => formData.append('files', file))
    } else {
      formData.append('files', files)
    }
    return api.upload('/papers/upload', formData, onProgress)
  },
  
  // 删除论文
  delete(id) {
    return api.delete(`/papers/${id}`)
  },
  
  // 批量删除论文
  bulkDelete(ids) {
    return api.post('/papers/bulk-delete', { ids })
  }
}

// 分析相关API
export const analysisApi = {
  // 开始分析
  start(paperIds, config = {}) {
    return api.post('/analysis/start', { paperIds, config })
  },
  
  // 获取分析状态
  getStatus(sessionId) {
    return api.get(`/analysis/sessions/${sessionId}`)
  },
  
  // 获取分析结果
  getResults(sessionId) {
    return api.get(`/analysis/sessions/${sessionId}/results`, { cache: true })
  },
  
  // 取消分析
  cancel(sessionId) {
    return api.post(`/analysis/sessions/${sessionId}/cancel`)
  }
}

// 学习计划相关API
export const planApi = {
  // 生成学习计划
  generate(analysisResults, preferences = {}) {
    return api.post('/plans/generate', { analysisResults, preferences })
  },
  
  // 获取学习计划
  get(planId) {
    return api.get(`/plans/${planId}`, { cache: true })
  },
  
  // 更新学习计划
  update(planId, updates) {
    return api.put(`/plans/${planId}`, updates)
  },
  
  // 获取用户的学习计划列表
  list() {
    return api.get('/plans', { cache: true, cacheTime: 60 * 1000 })
  }
}

// 知识图谱相关API
export const graphApi = {
  // 获取知识图谱数据
  get(sessionId) {
    return api.get(`/graphs/${sessionId}`, { cache: true })
  },
  
  // 获取节点详情
  getNode(nodeId) {
    return api.get(`/graphs/nodes/${nodeId}`)
  }
}

// 用户设置相关API
export const userApi = {
  // 获取用户设置
  getSettings() {
    return api.get('/user/settings', { cache: true })
  },
  
  // 更新用户设置
  updateSettings(settings) {
    return api.put('/user/settings', settings)
  },
  
  // 更新个人资料
  updateProfile(profile) {
    return api.put('/user/profile', profile)
  }
}

// 管理员相关API
export const adminApi = {
  // 获取待审批用户
  getPendingUsers(params = {}) {
    return api.get('/admin/users/pending', { params })
  },
  
  // 审批用户
  approveUser(userId, action = 'approve', reason = null, notes = null) {
    return api.post('/admin/users/approve', {
      user_id: userId,
      action: action,
      reason: reason,
      notes: notes
    })
  },
  
  // 拒绝用户
  rejectUser(userId, reason) {
    return api.post('/admin/users/approve', {
      user_id: userId,
      action: 'reject',
      reason: reason
    })
  },
  
  // 获取管理员仪表板
  getDashboard() {
    return api.get('/admin/dashboard', { cache: true, cacheTime: 60 * 1000 })
  },
  
  // 获取用户统计
  getUserStats() {
    return api.get('/admin/users/stats', { cache: true, cacheTime: 60 * 1000 })
  },
  
  // 搜索用户
  searchUsers(query, status = null, skip = 0, limit = 20) {
    const params = { query, skip, limit }
    if (status) params.status = status
    return api.get('/admin/users/search', { params })
  },
  
  // 获取所有用户
  getAllUsers(skip = 0, limit = 50) {
    return api.get('/admin/users/all', { params: { skip, limit } })
  },
  
  // 获取审计日志
  getAuditLogs(params = {}) {
    return api.get('/admin/logs/audit', { params })
  }
}

export { ApiError }