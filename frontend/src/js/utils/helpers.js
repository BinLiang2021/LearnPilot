/**
 * 工具函数集合
 */

/**
 * 类名合并工具 (类似clsx)
 */
export function cn(...classes) {
  return classes
    .flat()
    .filter(Boolean)
    .filter(x => typeof x === 'string' || typeof x === 'number')
    .join(' ')
}

/**
 * 防抖函数
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func.apply(this, args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 */
export function throttle(func, limit) {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * 格式化文件大小
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 格式化时间
 */
export function formatTime(date) {
  if (!date) return ''
  
  const now = new Date()
  const diff = now - new Date(date)
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

/**
 * 生成唯一ID
 */
export function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 深拷贝
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (typeof obj === 'object') {
    const cloned = {}
    Object.keys(obj).forEach(key => {
      cloned[key] = deepClone(obj[key])
    })
    return cloned
  }
}

/**
 * 文本截断
 */
export function truncate(text, length = 100, suffix = '...') {
  if (!text || text.length <= length) return text
  return text.substring(0, length) + suffix
}

/**
 * 获取文件扩展名
 */
export function getFileExtension(filename) {
  return filename.split('.').pop().toLowerCase()
}

/**
 * 验证邮箱格式
 */
export function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/**
 * 验证手机号格式
 */
export function isValidPhone(phone) {
  const regex = /^1[3-9]\d{9}$/
  return regex.test(phone)
}

/**
 * 字符串转换为驼峰命名
 */
export function toCamelCase(str) {
  return str.replace(/-([a-z])/g, (g) => g[1].toUpperCase())
}

/**
 * 驼峰命名转换为短横线命名
 */
export function toKebabCase(str) {
  return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase()
}

/**
 * 滚动到元素
 */
export function scrollToElement(element, options = {}) {
  if (typeof element === 'string') {
    element = document.querySelector(element)
  }
  
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      ...options
    })
  }
}

/**
 * 复制到剪贴板
 */
export async function copyToClipboard(text) {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text)
      return true
    } else {
      // 降级方案
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      const success = document.execCommand('copy')
      document.body.removeChild(textArea)
      return success
    }
  } catch (err) {
    console.error('复制失败:', err)
    return false
  }
}

/**
 * 检测设备类型
 */
export function getDeviceType() {
  const width = window.innerWidth
  if (width < 768) return 'mobile'
  if (width < 1024) return 'tablet'
  return 'desktop'
}

/**
 * 检测是否支持WebP格式
 */
export function supportsWebP() {
  const canvas = document.createElement('canvas')
  canvas.width = 1
  canvas.height = 1
  return canvas.toDataURL('image/webp').indexOf('image/webp') === 5
}

/**
 * 创建元素
 */
export function createElement(tag, props = {}, ...children) {
  const element = document.createElement(tag)
  
  Object.entries(props).forEach(([key, value]) => {
    if (key === 'className') {
      element.className = value
    } else if (key === 'style' && typeof value === 'object') {
      Object.assign(element.style, value)
    } else if (key.startsWith('on') && typeof value === 'function') {
      element.addEventListener(key.slice(2).toLowerCase(), value)
    } else {
      element.setAttribute(key, value)
    }
  })
  
  children.forEach(child => {
    if (typeof child === 'string') {
      element.appendChild(document.createTextNode(child))
    } else if (child instanceof Node) {
      element.appendChild(child)
    }
  })
  
  return element
}

/**
 * 数组分组
 */
export function groupBy(array, keyFn) {
  return array.reduce((groups, item) => {
    const key = keyFn(item)
    if (!groups[key]) {
      groups[key] = []
    }
    groups[key].push(item)
    return groups
  }, {})
}

/**
 * 数组去重
 */
export function unique(array, keyFn) {
  const seen = new Set()
  return array.filter(item => {
    const key = keyFn ? keyFn(item) : item
    if (seen.has(key)) {
      return false
    }
    seen.add(key)
    return true
  })
}