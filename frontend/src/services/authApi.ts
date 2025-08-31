import { apiRequest } from './api'
import { User, LoginRequest, LoginResponse, RegisterRequest } from '../types'

// 登录
export const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
  // 使用 FormData 格式发送登录请求（OAuth2 规范）
  const formData = new FormData()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)
  
  return apiRequest.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}

// 注册
export const register = async (userData: RegisterRequest): Promise<LoginResponse> => {
  return apiRequest.post('/auth/register', userData)
}

// 获取当前用户信息
export const getCurrentUser = async (): Promise<User> => {
  return apiRequest.get('/auth/me')
}

// 更新用户资料
export const updateProfile = async (userData: Partial<User>): Promise<User> => {
  return apiRequest.patch('/auth/me', userData)
}

// 修改密码
export const changePassword = async (data: {
  current_password: string
  new_password: string
}): Promise<{ message: string }> => {
  return apiRequest.post('/auth/change-password', data)
}

// 重置密码请求
export const requestPasswordReset = async (email: string): Promise<{ message: string }> => {
  return apiRequest.post('/auth/password-reset/request', { email })
}

// 重置密码确认
export const resetPassword = async (data: {
  token: string
  new_password: string
}): Promise<{ message: string }> => {
  return apiRequest.post('/auth/password-reset/confirm', data)
}

// 验证邮箱
export const verifyEmail = async (token: string): Promise<{ message: string }> => {
  return apiRequest.post('/auth/verify-email', { token })
}

// 重发验证邮件
export const resendVerificationEmail = async (): Promise<{ message: string }> => {
  return apiRequest.post('/auth/resend-verification')
}

// 刷新 token
export const refreshToken = async (): Promise<{ access_token: string }> => {
  return apiRequest.post('/auth/refresh')
}

// 注销（服务器端）
export const logout = async (): Promise<{ message: string }> => {
  return apiRequest.post('/auth/logout')
}