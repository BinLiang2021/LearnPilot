/**
 * 用户设置页面
 */

export function renderSettingsPage(context) {
  const app = document.getElementById('app')
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">用户设置</h1>
        <p class="text-gray-500">设置功能正在开发中...</p>
      </div>
    </div>
  `
}