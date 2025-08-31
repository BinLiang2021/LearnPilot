import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { useAuthStore } from '../stores/authStore'
import toast from 'react-hot-toast'

// 创建 axios 实例
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加认证令牌
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 打印请求日志（开发环境）
    if (import.meta.env.DEV) {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`)
    }
    
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // 打印响应日志（开发环境）
    if (import.meta.env.DEV) {
      console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data)
    }
    
    return response
  },
  (error) => {
    console.error('Response error:', error)
    
    // 处理不同的错误状态码
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除用户状态
          useAuthStore.getState().logout()
          toast.error('登录状态已过期，请重新登录')
          break
          
        case 403:
          toast.error('没有权限执行此操作')
          break
          
        case 404:
          toast.error('请求的资源不存在')
          break
          
        case 422:
          // 验证错误
          const validationError = data.detail || '输入数据验证失败'
          toast.error(typeof validationError === 'string' ? validationError : '输入数据验证失败')
          break
          
        case 429:
          toast.error('请求过于频繁，请稍后再试')
          break
          
        case 500:
          toast.error('服务器内部错误，请稍后再试')
          break
          
        default:
          toast.error(data.message || data.detail || '请求失败')
      }
      
      // 返回错误信息
      return Promise.reject({
        message: data.message || data.detail || `HTTP ${status} Error`,
        status,
        data,
      })
    }
    
    // 网络错误或其他错误
    if (error.request) {
      toast.error('网络错误，请检查您的网络连接')
      return Promise.reject({
        message: '网络错误',
        status: 0,
      })
    }
    
    // 其他错误
    toast.error('未知错误')
    return Promise.reject({
      message: error.message || '未知错误',
      status: 0,
    })
  }
)

// 通用 API 方法
export const apiRequest = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => 
    api.get(url, config).then(response => response.data),
    
  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => 
    api.post(url, data, config).then(response => response.data),
    
  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => 
    api.put(url, data, config).then(response => response.data),
    
  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => 
    api.patch(url, data, config).then(response => response.data),
    
  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => 
    api.delete(url, config).then(response => response.data),
}

// 文件上传专用方法
export const uploadFile = (
  url: string,
  file: File,
  onUploadProgress?: (progressEvent: { loaded: number; total: number }) => void
) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return api.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  }).then(response => response.data)
}

// 批量文件上传
export const uploadMultipleFiles = (
  url: string,
  files: File[],
  onUploadProgress?: (progressEvent: { loaded: number; total: number }) => void
) => {
  const formData = new FormData()
  files.forEach((file, index) => {
    formData.append(`files`, file)
  })
  
  return api.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  }).then(response => response.data)
}

// 下载文件
export const downloadFile = async (url: string, filename?: string): Promise<void> => {
  const response = await api.get(url, {
    responseType: 'blob',
  })
  
  const blob = new Blob([response.data])
  const downloadUrl = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = downloadUrl
  link.download = filename || 'download'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(downloadUrl)
}

// 取消请求的 token
export const createCancelToken = () => axios.CancelToken.source()

export default api