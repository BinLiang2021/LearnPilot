/**
 * 注册页面组件
 */

import { Button } from '../components/ui/Button.js'
import { Input } from '../components/ui/Input.js'
import { Card } from '../components/ui/Card.js'
import { showError, showSuccess } from '../components/ui/Notification.js'
import { authApi } from '../services/api.js'
import { navigate } from '../utils/router.js'
import { isValidEmail } from '../utils/helpers.js'

/**
 * 渲染注册页面
 */
export function renderRegisterPage(context) {
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
            创建您的账户
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            已有账户？
            <a href="/login" class="font-medium text-primary-600 hover:text-primary-500" id="login-link">
              立即登录
            </a>
          </p>
        </div>

        <!-- 注册表单 -->
        <div id="register-form-container">
          <!-- 表单将在这里渲染 -->
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
  
  // 渲染注册表单
  renderRegisterForm()
  
  // 绑定链接事件
  bindLinkEvents()
}

/**
 * 渲染注册表单
 */
function renderRegisterForm() {
  const container = document.getElementById('register-form-container')
  
  const formCard = Card.create('', {
    padding: 'lg'
  })
  
  const form = document.createElement('form')
  form.className = 'space-y-6'
  form.id = 'register-form'
  
  // 姓名输入框
  const nameInput = Input.create({
    type: 'text',
    label: '姓名',
    placeholder: '请输入您的姓名',
    required: true,
    leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>`
  })
  nameInput.id = 'name-field'
  
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
    placeholder: '请输入密码（至少6位）',
    required: true,
    leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>`
  })
  passwordInput.id = 'password-field'
  
  // 确认密码输入框
  const confirmPasswordInput = Input.create({
    type: 'password',
    label: '确认密码',
    placeholder: '请再次输入密码',
    required: true,
    leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>`
  })
  confirmPasswordInput.id = 'confirm-password-field'
  
  // 学术水平选择
  const levelDiv = document.createElement('div')
  levelDiv.innerHTML = `
    <label class="block text-sm font-medium text-gray-700 mb-2">
      学术水平 <span class="text-error-500">*</span>
    </label>
    <select id="level-select" required 
            class="input block w-full">
      <option value="">请选择您的学术水平</option>
      <option value="beginner">初学者</option>
      <option value="intermediate">中等水平</option>
      <option value="advanced">专业水平</option>
    </select>
  `
  
  // 服务条款同意
  const agreementDiv = document.createElement('div')
  agreementDiv.className = 'flex items-center'
  agreementDiv.innerHTML = `
    <input id="agreement" name="agreement" type="checkbox" required
           class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
    <label for="agreement" class="ml-2 block text-sm text-gray-900">
      我同意 
      <a href="#" class="text-primary-600 hover:text-primary-500">服务条款</a> 
      和 
      <a href="#" class="text-primary-600 hover:text-primary-500">隐私政策</a>
    </label>
  `
  
  // 注册按钮
  const registerButton = Button.create('创建账户', {
    variant: 'primary',
    size: 'md',
    fullWidth: true
  }, {
    onClick: handleRegister,
    ariaLabel: '创建LearnPilot账户'
  })
  registerButton.id = 'register-button'
  
  // 组装表单
  form.appendChild(nameInput)
  form.appendChild(emailInput)
  form.appendChild(passwordInput)
  form.appendChild(confirmPasswordInput)
  form.appendChild(levelDiv)
  form.appendChild(agreementDiv)
  form.appendChild(registerButton)
  
  formCard.appendChild(form)
  container.appendChild(formCard)
  
  // 绑定表单提交事件
  form.addEventListener('submit', handleRegister)
}

/**
 * 处理注册
 */
async function handleRegister(e) {
  e.preventDefault()
  
  const nameField = document.querySelector('#name-field input')
  const emailField = document.querySelector('#email-field input')
  const passwordField = document.querySelector('#password-field input')
  const confirmPasswordField = document.querySelector('#confirm-password-field input')
  const levelSelect = document.querySelector('#level-select')
  const agreementField = document.querySelector('#agreement')
  
  const name = nameField.value.trim()
  const email = emailField.value.trim()
  const password = passwordField.value
  const confirmPassword = confirmPasswordField.value
  const level = levelSelect.value
  const agreement = agreementField.checked
  
  // 前端验证
  if (!name) {
    showError('请输入姓名')
    nameField.focus()
    return
  }
  
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
  
  if (password !== confirmPassword) {
    showError('两次输入的密码不一致')
    confirmPasswordField.focus()
    return
  }
  
  if (!level) {
    showError('请选择学术水平')
    levelSelect.focus()
    return
  }
  
  if (!agreement) {
    showError('请同意服务条款和隐私政策')
    agreementField.focus()
    return
  }
  
  // 设置加载状态
  setFormLoading(true)
  
  try {
    // 调用注册API
    await authApi.register({
      name,
      email,
      password,
      level
    })
    
    showSuccess('注册成功！请等待管理员审核激活')
    
    // 跳转到登录页面
    setTimeout(() => {
      navigate('/login')
    }, 2000)
    
  } catch (error) {
    console.error('注册失败:', error)
    
    if (error.status === 409) {
      showError('该邮箱已被注册，请使用其他邮箱')
      emailField.focus()
    } else {
      showError(error.message || '注册失败，请稍后重试')
    }
    
  } finally {
    setFormLoading(false)
  }
}

/**
 * 设置表单加载状态
 */
function setFormLoading(loading) {
  const form = document.querySelector('#register-form')
  const inputs = form.querySelectorAll('input, select')
  const button = document.querySelector('#register-button')
  
  inputs.forEach(input => {
    input.disabled = loading
  })
  
  if (loading) {
    button.innerHTML = `
      <div class="flex items-center justify-center">
        <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
        创建中...
      </div>
    `
    button.disabled = true
  } else {
    button.innerHTML = '创建账户'
    button.disabled = false
  }
}

/**
 * 绑定链接事件
 */
function bindLinkEvents() {
  const loginLink = document.getElementById('login-link')
  loginLink.addEventListener('click', (e) => {
    e.preventDefault()
    navigate('/login')
  })
  
  const homeLink = document.getElementById('home-link')
  homeLink.addEventListener('click', (e) => {
    e.preventDefault()
    navigate('/')
  })
}