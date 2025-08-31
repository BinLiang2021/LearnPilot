/**
 * 管理员页面
 */

import { adminApi } from '../services/api.js'
import { showError, showSuccess } from '../components/ui/Notification.js'
import { Button } from '../components/ui/Button.js'
import { Card } from '../components/ui/Card.js'

let currentView = 'dashboard'

export async function renderAdminPage(context) {
  const app = document.getElementById('app')
  
  // 渲染管理员页面框架
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50">
      <!-- 头部导航 -->
      <div class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <h1 class="text-xl font-semibold text-gray-900">🛡️ 管理员控制台</h1>
            </div>
            <div class="flex items-center space-x-4">
              <span class="text-sm text-gray-500">欢迎, 系统管理员</span>
              <button onclick="logout()" class="text-sm text-red-600 hover:text-red-800">退出登录</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 侧边导航和内容区域 -->
      <div class="flex">
        <!-- 侧边栏 -->
        <div class="w-64 bg-white shadow-sm min-h-screen">
          <nav class="mt-5 px-2">
            <div class="space-y-1">
              <button onclick="showDashboard()" id="nav-dashboard" 
                class="nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-900 bg-gray-100">
                📊 仪表板
              </button>
              <button onclick="showPendingUsers()" id="nav-users"
                class="nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                👥 待审批用户
              </button>
              <button onclick="showAllUsers()" id="nav-all-users"
                class="nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                📋 所有用户
              </button>
              <button onclick="showAuditLogs()" id="nav-logs"
                class="nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                📜 审计日志
              </button>
            </div>
          </nav>
        </div>

        <!-- 主内容区域 -->
        <div class="flex-1 p-6">
          <div id="admin-content">
            <!-- 内容将在这里动态加载 -->
          </div>
        </div>
      </div>
    </div>
  `

  // 绑定全局函数
  bindGlobalFunctions()
  
  // 默认加载仪表板
  await showDashboard()
}

// 绑定全局函数
function bindGlobalFunctions() {
  window.showDashboard = showDashboard
  window.showPendingUsers = showPendingUsers  
  window.showAllUsers = showAllUsers
  window.showAuditLogs = showAuditLogs
  window.approveUser = approveUser
  window.rejectUser = rejectUser
  window.logout = logout
}

// 显示仪表板
async function showDashboard() {
  updateActiveNav('nav-dashboard')
  const content = document.getElementById('admin-content')
  
  content.innerHTML = '<div class="text-center py-8">📊 加载仪表板数据...</div>'
  
  try {
    // 这里应该调用仪表板API，先用模拟数据
    const dashboardData = {
      user_stats: {
        total_users: 0,
        pending_approval: 0,
        approved_users: 0,
        rejected_users: 0
      },
      recent_activity: {
        new_registrations: 0,
        recent_approvals: 0
      }
    }

    content.innerHTML = `
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-900">管理员仪表板</h2>
        <p class="text-gray-600">系统概览和统计信息</p>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">👥</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">总用户数</dt>
                  <dd class="text-lg font-medium text-gray-900">${dashboardData.user_stats.total_users}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">⏳</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">待审批</dt>
                  <dd class="text-lg font-medium text-gray-900">${dashboardData.user_stats.pending_approval}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">✅</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">已批准</dt>
                  <dd class="text-lg font-medium text-gray-900">${dashboardData.user_stats.approved_users}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">❌</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">已拒绝</dt>
                  <dd class="text-lg font-medium text-gray-900">${dashboardData.user_stats.rejected_users}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快速操作 -->
      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">快速操作</h3>
        <div class="flex space-x-4">
          <button onclick="showPendingUsers()" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            审批用户
          </button>
          <button onclick="showAllUsers()" class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            查看所有用户
          </button>
          <button onclick="showAuditLogs()" class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            查看日志
          </button>
        </div>
      </div>
    `
  } catch (error) {
    console.error('加载仪表板失败:', error)
    content.innerHTML = '<div class="text-center py-8 text-red-600">❌ 加载仪表板数据失败</div>'
  }
}

// 显示待审批用户
async function showPendingUsers() {
  updateActiveNav('nav-users')
  const content = document.getElementById('admin-content')
  
  content.innerHTML = '<div class="text-center py-8">👥 加载待审批用户...</div>'
  
  try {
    const response = await adminApi.getPendingUsers()
    const users = response.users || []

    content.innerHTML = `
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-900">待审批用户</h2>
        <p class="text-gray-600">共有 ${users.length} 个用户等待审批</p>
      </div>

      ${users.length === 0 ? 
        '<div class="text-center py-12 bg-white rounded-lg shadow"><p class="text-gray-500">🎉 没有待审批的用户</p></div>' :
        `<div class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            ${users.map(user => `
              <li class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                        <span class="text-sm font-medium text-gray-700">${user.name ? user.name.charAt(0).toUpperCase() : 'U'}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">${user.name || '未知'}</div>
                      <div class="text-sm text-gray-500">${user.email || '无邮箱'}</div>
                      <div class="text-xs text-gray-400">注册时间: ${user.created_at ? new Date(user.created_at).toLocaleDateString('zh-CN') : '未知'}</div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button onclick="approveUser(${user.id}, '${user.name}')" 
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                      ✅ 批准
                    </button>
                    <button onclick="rejectUser(${user.id}, '${user.name}')" 
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                      ❌ 拒绝
                    </button>
                  </div>
                </div>
                ${user.registration_notes ? `
                  <div class="mt-2 px-14">
                    <div class="text-sm text-gray-600 bg-gray-50 rounded p-2">
                      <strong>注册备注:</strong> ${user.registration_notes}
                    </div>
                  </div>
                ` : ''}
              </li>
            `).join('')}
          </ul>
        </div>`
      }
    `
  } catch (error) {
    console.error('加载待审批用户失败:', error)
    content.innerHTML = '<div class="text-center py-8 text-red-600">❌ 加载用户列表失败</div>'
  }
}

// 显示所有用户（占位）
async function showAllUsers() {
  updateActiveNav('nav-all-users')
  const content = document.getElementById('admin-content')
  
  content.innerHTML = `
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">所有用户</h2>
      <p class="text-gray-600">用户管理功能</p>
    </div>
    <div class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">🚧 此功能正在开发中...</p>
    </div>
  `
}

// 显示审计日志（占位）
async function showAuditLogs() {
  updateActiveNav('nav-logs')
  const content = document.getElementById('admin-content')
  
  content.innerHTML = `
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">审计日志</h2>
      <p class="text-gray-600">系统操作记录</p>
    </div>
    <div class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">🚧 此功能正在开发中...</p>
    </div>
  `
}

// 批准用户
async function approveUser(userId, userName) {
  if (!confirm(`确定要批准用户 "${userName}" 的注册申请吗？`)) {
    return
  }

  try {
    await adminApi.approveUser(userId)
    showSuccess(`✅ 用户 "${userName}" 已成功批准！`)
    // 刷新待审批用户列表
    await showPendingUsers()
  } catch (error) {
    console.error('批准用户失败:', error)
    showError(`❌ 批准用户失败: ${error.message || '未知错误'}`)
  }
}

// 拒绝用户
async function rejectUser(userId, userName) {
  const reason = prompt(`请输入拒绝用户 "${userName}" 的原因:`)
  if (!reason) {
    return
  }

  try {
    await adminApi.rejectUser(userId, reason)
    showSuccess(`❌ 用户 "${userName}" 已被拒绝`)
    // 刷新待审批用户列表
    await showPendingUsers()
  } catch (error) {
    console.error('拒绝用户失败:', error)
    showError(`❌ 拒绝用户失败: ${error.message || '未知错误'}`)
  }
}

// 更新活跃导航
function updateActiveNav(activeId) {
  // 移除所有活跃状态
  document.querySelectorAll('.nav-item').forEach(item => {
    item.className = 'nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900'
  })
  
  // 设置活跃状态
  const activeItem = document.getElementById(activeId)
  if (activeItem) {
    activeItem.className = 'nav-item w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-900 bg-gray-100'
  }
}

// 退出登录
function logout() {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
}