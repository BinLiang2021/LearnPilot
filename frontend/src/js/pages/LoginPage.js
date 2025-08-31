/**
 * 登录页面组件
 */

import { Button } from '../components/ui/Button.js'
import { Input } from '../components/ui/Input.js'
import { Card } from '../components/ui/Card.js'
import { showError, showSuccess } from '../components/ui/Notification.js'
import { authApi } from '../services/api.js'
import { userStorage } from '../utils/storage.js'
import { navigate } from '../utils/router.js'
import { isValidEmail } from '../utils/helpers.js'

/**
 * 渲染登录页面
 */
export function renderLoginPage(context) {
  const app = document.getElementById('app')
  
  app.innerHTML = `
    <div class="min-h-screen bg-gradient-to-br from-primary-50 to-accent-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <!-- Logo 和标题 -->
        <div class="text-center">
          <div class="flex justify-center">
            <div class="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
          </div>
          <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
            登录您的账户
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            还没有账户？
            <a href="/register" class="font-medium text-primary-600 hover:text-primary-500" id="register-link">
              立即注册
            </a>
          </p>
        </div>

        <!-- 登录表单 -->
        <div id="login-form-container">
          <!-- 表单将在这里渲染 -->
        </div>

        <!-- 其他登录方式 -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">其他方式</span>
            </div>
          </div>

          <div class="mt-6 space-y-3">
            <button type="button" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors">
              <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span class="ml-2">使用 Google 账户登录</span>
            </button>
          </div>
        </div>

        <!-- 返回首页链接 -->
        <div class="text-center">
          <a href="/" class="text-sm text-gray-500 hover:text-gray-700" id="home-link">
            ← 返回首页
          </a>
        </div>
      </div>
    </div>
  `
  
  // 渲染登录表单
  renderLoginForm()
  
  // 绑定链接事件
  bindLinkEvents()
}

/**
 * 渲染登录表单
 */
function renderLoginForm() {
  const container = document.getElementById('login-form-container')
  
  // 创建表单卡片
  const formCard = Card.create('', {
    padding: 'lg'
  })
  
  // 创建表单元素
  const form = document.createElement('form')
  form.className = 'space-y-6'
  form.id = 'login-form'
  
  // 邮箱输入框
  const emailInput = Input.create({
    type: 'email',
    label: '邮箱地址',
    placeholder: '请输入您的邮箱',
    required: true,
    leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
              </svg>`
  })
  emailInput.id = 'email-field'
  
  // 密码输入框
  const passwordInput = Input.create({
    type: 'password',
    label: '密码',
    placeholder: '请输入您的密码',
    required: true,
    leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>`
  })
  passwordInput.id = 'password-field'
  
  // 记住我和忘记密码
  const optionsDiv = document.createElement('div')
  optionsDiv.className = 'flex items-center justify-between'
  optionsDiv.innerHTML = `
    <div class="flex items-center">
      <input id="remember-me" name="remember-me" type="checkbox" 
             class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
      <label for="remember-me" class="ml-2 block text-sm text-gray-900">
        记住我
      </label>
    </div>
    <div class="text-sm">
      <a href="#" class="font-medium text-primary-600 hover:text-primary-500" id="forgot-password">
        忘记密码？
      </a>
    </div>
  `
  
  // 登录按钮
  const loginButton = Button.create('登录', {
    variant: 'primary',
    size: 'md',
    fullWidth: true
  }, {
    onClick: handleLogin,
    ariaLabel: '登录到LearnPilot'
  })
  loginButton.id = 'login-button'
  
  // 组装表单
  form.appendChild(emailInput)
  form.appendChild(passwordInput)
  form.appendChild(optionsDiv)
  form.appendChild(loginButton)
  
  formCard.appendChild(form)
  container.appendChild(formCard)
  
  // 绑定表单提交事件
  form.addEventListener('submit', handleLogin)
}

/**
 * 处理登录
 */
async function handleLogin(e) {
  e.preventDefault()
  
  const emailField = document.querySelector('#email-field input')
  const passwordField = document.querySelector('#password-field input')
  const rememberField = document.querySelector('#remember-me')
  const loginButton = document.querySelector('#login-button')
  
  const email = emailField.value.trim()
  const password = passwordField.value
  const remember = rememberField.checked
  
  // 前端验证
  if (!email) {
    showError('请输入邮箱地址')
    emailField.focus()
    return
  }
  
  if (!isValidEmail(email)) {
    showError('请输入有效的邮箱地址')
    emailField.focus()
    return
  }
  
  if (!password) {
    showError('请输入密码')
    passwordField.focus()
    return
  }
  
  if (password.length < 6) {
    showError('密码长度至少6位')
    passwordField.focus()
    return
  }
  
  // 设置加载状态
  setFormLoading(true)
  
  try {
    // 调用登录API
    const response = await authApi.login({
      email,
      password,
      remember
    })
    
    // 保存用户信息和token
    userStorage.setToken(response.token)
    userStorage.setUser(response.user)
    
    // 设置全局用户状态
    if (window.app) {
      window.app.setCurrentUser(response.user)
    }
    
    showSuccess('登录成功！')
    
    // 跳转到目标页面
    const redirectUrl = sessionStorage.getItem('redirect_after_login') || '/dashboard'
    sessionStorage.removeItem('redirect_after_login')
    
    setTimeout(() => {
      navigate(redirectUrl)
    }, 1000)
    
  } catch (error) {
    console.error('登录失败:', error)
    
    // 显示错误信息
    if (error.status === 401) {
      showError('邮箱或密码错误，请重试')
    } else if (error.status === 403) {
      showError('账户尚未激活或已被禁用')
    } else if (error.status === 429) {
      showError('登录尝试过于频繁，请稍后再试')
    } else {
      showError(error.message || '登录失败，请稍后重试')
    }
    
    // 清空密码
    passwordField.value = ''
    passwordField.focus()
    
  } finally {
    setFormLoading(false)
  }
}

/**
 * 设置表单加载状态
 */
function setFormLoading(loading) {
  const emailField = document.querySelector('#email-field input')
  const passwordField = document.querySelector('#password-field input')
  const rememberField = document.querySelector('#remember-me')
  const loginButton = document.querySelector('#login-button')
  
  emailField.disabled = loading
  passwordField.disabled = loading
  rememberField.disabled = loading
  
  if (loading) {
    loginButton.innerHTML = `
      <div class="flex items-center justify-center">
        <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
        登录中...
      </div>
    `
    loginButton.disabled = true
  } else {
    loginButton.innerHTML = '登录'
    loginButton.disabled = false
  }
}

/**
 * 绑定链接事件
 */
function bindLinkEvents() {
  // 注册链接
  const registerLink = document.getElementById('register-link')
  registerLink.addEventListener('click', (e) => {
    e.preventDefault()
    navigate('/register')
  })
  
  // 首页链接
  const homeLink = document.getElementById('home-link')
  homeLink.addEventListener('click', (e) => {
    e.preventDefault()
    navigate('/')
  })
  
  // 忘记密码链接
  const forgotPasswordLink = document.getElementById('forgot-password')
  forgotPasswordLink.addEventListener('click', (e) => {
    e.preventDefault()
    handleForgotPassword()
  })
}

/**
 * 处理忘记密码
 */
function handleForgotPassword() {
  // TODO: 实现忘记密码功能
  showError('忘记密码功能暂未开放，请联系管理员')
}