/**
 * 知识图谱页面
 */

export function renderGraphPage(context) {
  const app = document.getElementById('app')
  const sessionId = context.params.sessionId
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">知识图谱</h1>
        <p class="text-gray-600">会话ID: ${sessionId}</p>
        <p class="text-gray-500 mt-2">知识图谱功能正在开发中...</p>
      </div>
    </div>
  `
}