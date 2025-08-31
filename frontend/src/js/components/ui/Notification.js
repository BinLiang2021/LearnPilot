import { cn } from '../../utils/helpers.js'

/**
 * Notification 组件
 * 支持多种类型、自动隐藏、操作按钮等
 */
export class Notification {
  constructor(options = {}) {
    this.options = {
      variant: 'info',
      title: null,
      message: '',
      dismissible: true,
      autoHide: false,
      hideAfter: 5000,
      actions: [],
      position: 'top-right',
      ...options
    }
  }

  /**
   * 创建通知元素
   */
  createElement(props = {}) {
    const { variant, title, message, dismissible, actions } = this.options
    
    const notification = document.createElement('div')
    
    // 样式类
    const baseClasses = 'rounded-lg border p-4 shadow-lg max-w-sm w-full'
    const variantClasses = {
      success: 'bg-success-50 border-success-200 text-success-800',
      warning: 'bg-warning-50 border-warning-200 text-warning-800',
      error: 'bg-error-50 border-error-200 text-error-800',
      info: 'bg-info-50 border-info-200 text-info-800'
    }
    
    notification.className = cn(
      baseClasses,
      variantClasses[variant],
      'animate-slide-up',
      props.className
    )
    
    // 创建通知内容
    this.renderContent(notification, title, message, variant, dismissible, actions, props)
    
    // 自动隐藏
    if (this.options.autoHide) {
      this.setupAutoHide(notification, props.onDismiss)
    }
    
    return notification
  }

  /**
   * 渲染通知内容
   */
  renderContent(notification, title, message, variant, dismissible, actions, props) {
    const content = document.createElement('div')
    content.className = 'flex items-start'
    
    // 图标
    const iconContainer = document.createElement('div')
    iconContainer.className = 'flex-shrink-0'
    iconContainer.appendChild(this.createIcon(variant))
    content.appendChild(iconContainer)
    
    // 文本内容
    const textContainer = document.createElement('div')
    textContainer.className = 'ml-3 flex-1'
    
    // 标题
    if (title) {
      const titleElement = document.createElement('h3')
      titleElement.className = 'text-sm font-medium mb-1'
      titleElement.textContent = title
      textContainer.appendChild(titleElement)
    }
    
    // 消息
    const messageElement = document.createElement('p')
    messageElement.className = 'text-sm'
    messageElement.textContent = message
    textContainer.appendChild(messageElement)
    
    // 操作按钮
    if (actions.length > 0) {
      const actionsContainer = document.createElement('div')
      actionsContainer.className = 'mt-3 flex space-x-3'
      
      actions.forEach(action => {
        const button = document.createElement('button')
        button.className = cn(
          'text-sm font-medium underline hover:no-underline',
          action.variant === 'primary' ? 'text-current' : 'text-current opacity-75 hover:opacity-100'
        )
        button.textContent = action.label
        button.addEventListener('click', action.onClick)
        actionsContainer.appendChild(button)
      })
      
      textContainer.appendChild(actionsContainer)
    }
    
    content.appendChild(textContainer)
    
    // 关闭按钮
    if (dismissible) {
      const closeButton = this.createCloseButton(notification, props.onDismiss)
      content.appendChild(closeButton)
    }
    
    notification.appendChild(content)
  }

  /**
   * 创建图标
   */
  createIcon(variant) {
    const icon = document.createElement('div')
    icon.className = 'w-5 h-5'
    
    const iconMap = {
      success: `<svg fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>`,
      warning: `<svg fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>`,
      error: `<svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>`,
      info: `<svg fill="currentColor" viewBox="0 0 20 20">
               <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
             </svg>`
    }
    
    icon.innerHTML = iconMap[variant] || iconMap.info
    return icon
  }

  /**
   * 创建关闭按钮
   */
  createCloseButton(notification, onDismiss) {
    const closeContainer = document.createElement('div')
    closeContainer.className = 'ml-4 flex-shrink-0'
    
    const closeButton = document.createElement('button')
    closeButton.className = 'inline-flex rounded-md text-current opacity-70 hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-current'
    closeButton.innerHTML = `
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    `
    
    closeButton.addEventListener('click', () => {
      this.dismiss(notification, onDismiss)
    })
    
    closeContainer.appendChild(closeButton)
    return closeContainer
  }

  /**
   * 设置自动隐藏
   */
  setupAutoHide(notification, onDismiss) {
    setTimeout(() => {
      this.dismiss(notification, onDismiss)
    }, this.options.hideAfter)
  }

  /**
   * 关闭通知
   */
  dismiss(notification, onDismiss) {
    notification.classList.add('animate-fade-out')
    
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification)
      }
      if (onDismiss) {
        onDismiss()
      }
    }, 200)
  }

  /**
   * 静态工厂方法
   */
  static create(options = {}, props = {}) {
    const notification = new Notification(options)
    return notification.createElement(props)
  }

  /**
   * 预设通知类型
   */
  static success(message, options = {}, props = {}) {
    return Notification.create({
      variant: 'success',
      message,
      ...options
    }, props)
  }

  static warning(message, options = {}, props = {}) {
    return Notification.create({
      variant: 'warning',
      message,
      ...options
    }, props)
  }

  static error(message, options = {}, props = {}) {
    return Notification.create({
      variant: 'error',
      message,
      ...options
    }, props)
  }

  static info(message, options = {}, props = {}) {
    return Notification.create({
      variant: 'info',
      message,
      ...options
    }, props)
  }
}

/**
 * 通知管理器
 */
export class NotificationManager {
  constructor() {
    this.container = null
    this.notifications = new Map()
    this.init()
  }

  /**
   * 初始化容器
   */
  init() {
    this.container = document.createElement('div')
    this.container.className = 'fixed top-4 right-4 z-50 space-y-4'
    document.body.appendChild(this.container)
  }

  /**
   * 显示通知
   */
  show(options = {}, props = {}) {
    const notification = Notification.create(options, {
      ...props,
      onDismiss: () => {
        this.remove(notification)
        if (props.onDismiss) {
          props.onDismiss()
        }
      }
    })
    
    this.container.appendChild(notification)
    this.notifications.set(notification, options)
    
    return notification
  }

  /**
   * 移除通知
   */
  remove(notification) {
    if (this.notifications.has(notification)) {
      this.notifications.delete(notification)
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification)
      }
    }
  }

  /**
   * 清空所有通知
   */
  clear() {
    this.notifications.clear()
    this.container.innerHTML = ''
  }

  /**
   * 便利方法
   */
  success(message, options = {}) {
    return this.show({ variant: 'success', message, ...options })
  }

  warning(message, options = {}) {
    return this.show({ variant: 'warning', message, ...options })
  }

  error(message, options = {}) {
    return this.show({ variant: 'error', message, ...options })
  }

  info(message, options = {}) {
    return this.show({ variant: 'info', message, ...options })
  }
}

// 全局通知管理器实例
export const notificationManager = new NotificationManager()

// 导出便利函数
export function showNotification(options = {}, props = {}) {
  return notificationManager.show(options, props)
}

export function showSuccess(message, options = {}) {
  return notificationManager.success(message, options)
}

export function showWarning(message, options = {}) {
  return notificationManager.warning(message, options)
}

export function showError(message, options = {}) {
  return notificationManager.error(message, options)
}

export function showInfo(message, options = {}) {
  return notificationManager.info(message, options)
}