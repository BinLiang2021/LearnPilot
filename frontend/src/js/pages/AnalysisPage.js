/**
 * 分析进度页面
 */

export function renderAnalysisPage(context) {
  const app = document.getElementById('app')
  const sessionId = context.params.sessionId
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">分析进度</h1>
        <p class="text-gray-600">分析ID: ${sessionId}</p>
        <p class="text-gray-500 mt-2">分析功能正在开发中...</p>
      </div>
    </div>
  `
}