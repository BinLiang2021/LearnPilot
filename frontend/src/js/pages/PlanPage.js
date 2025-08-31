/**
 * 学习计划页面
 */

export function renderPlanPage(context) {
  const app = document.getElementById('app')
  const planId = context.params.planId
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">学习计划</h1>
        <p class="text-gray-600">计划ID: ${planId}</p>
        <p class="text-gray-500 mt-2">学习计划功能正在开发中...</p>
      </div>
    </div>
  `
}