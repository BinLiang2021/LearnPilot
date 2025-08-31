/**
 * 论文上传页面
 */

export function renderUploadPage(context) {
  const app = document.getElementById('app')
  
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">论文上传</h1>
        <p class="text-gray-600">上传功能正在开发中...</p>
      </div>
    </div>
  `
}