import { cn } from '../../utils/helpers.js'

/**
 * Modal 组件
 * 支持多种大小、样式和交互模式
 */
export class Modal {
  constructor(options = {}) {
    this.options = {
      size: 'md',
      closable: true,
      closeOnBackdrop: true,
      closeOnEscape: true,
      title: null,
      footer: null,
      showHeader: true,
      showFooter: true,
      ...options
    }
    this.isOpen = false
    this.backdrop = null
    this.modal = null
  }

  /**
   * 创建模态框元素
   */
  createElement(children, props = {}) {
    const { size, closable, title, footer, showHeader, showFooter } = this.options
    
    // 创建背景层
    this.backdrop = document.createElement('div')
    this.backdrop.className = 'fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50 p-4'
    
    // 创建模态框容器
    this.modal = document.createElement('div')
    
    // 大小样式
    const sizeClasses = {
      xs: 'max-w-xs',
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      '2xl': 'max-w-2xl',
      '3xl': 'max-w-3xl',
      '4xl': 'max-w-4xl',
      full: 'max-w-full mx-4'
    }
    
    this.modal.className = cn(
      'bg-white rounded-lg shadow-xl',
      'w-full',
      sizeClasses[size],
      'animate-fade-in',
      props.className
    )
    
    // 创建模态框内容
    this.renderContent(this.modal, children, title, footer, showHeader, showFooter, closable, props)
    
    // 绑定事件
    this.bindEvents(props)
    
    this.backdrop.appendChild(this.modal)
    return this.backdrop
  }

  /**
   * 渲染模态框内容
   */
  renderContent(modal, children, title, footer, showHeader, showFooter, closable, props) {
    // Header
    if (showHeader && (title || closable)) {
      const header = this.createHeader(title, closable, props.onClose)
      modal.appendChild(header)
    }
    
    // Body
    const body = document.createElement('div')
    body.className = cn(
      'px-6',
      showHeader ? 'pt-0' : 'pt-6',
      showFooter ? 'pb-4' : 'pb-6'
    )
    
    if (typeof children === 'string') {
      body.innerHTML = children
    } else if (children instanceof HTMLElement) {
      body.appendChild(children)
    } else if (Array.isArray(children)) {
      children.forEach(child => {
        if (typeof child === 'string') {
          const textNode = document.createTextNode(child)
          body.appendChild(textNode)
        } else if (child instanceof HTMLElement) {
          body.appendChild(child)
        }
      })
    }
    
    modal.appendChild(body)
    
    // Footer
    if (showFooter && footer) {
      const footerElement = this.createFooter(footer)
      modal.appendChild(footerElement)
    }
  }

  /**
   * 创建头部
   */
  createHeader(title, closable, onClose) {
    const header = document.createElement('div')
    header.className = 'px-6 py-4 border-b border-gray-200 flex items-center justify-between'
    
    if (title) {
      const titleElement = document.createElement('h3')
      titleElement.className = 'text-lg font-medium text-gray-900'
      titleElement.textContent = title
      header.appendChild(titleElement)
    }
    
    if (closable) {
      const closeButton = document.createElement('button')
      closeButton.className = 'text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded'
      closeButton.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      `
      closeButton.addEventListener('click', () => {
        this.close()
        if (onClose) onClose()
      })
      header.appendChild(closeButton)
    }
    
    return header
  }

  /**
   * 创建底部
   */
  createFooter(footer) {
    const footerElement = document.createElement('div')
    footerElement.className = 'px-6 py-4 border-t border-gray-200'
    
    if (typeof footer === 'string') {
      footerElement.innerHTML = footer
    } else if (footer instanceof HTMLElement) {
      footerElement.appendChild(footer)
    } else if (Array.isArray(footer)) {
      const buttonContainer = document.createElement('div')
      buttonContainer.className = 'flex space-x-3 justify-end'
      
      footer.forEach(button => {
        if (button instanceof HTMLElement) {
          buttonContainer.appendChild(button)
        }
      })
      
      footerElement.appendChild(buttonContainer)
    }
    
    return footerElement
  }

  /**
   * 绑定事件
   */
  bindEvents(props) {
    // 背景点击关闭
    if (this.options.closeOnBackdrop) {
      this.backdrop.addEventListener('click', (e) => {
        if (e.target === this.backdrop) {
          this.close()
          if (props.onClose) props.onClose()
        }
      })
    }
    
    // ESC键关闭
    if (this.options.closeOnEscape) {
      this.escapeHandler = (e) => {
        if (e.key === 'Escape' && this.isOpen) {
          this.close()
          if (props.onClose) props.onClose()
        }
      }
      document.addEventListener('keydown', this.escapeHandler)
    }
  }

  /**
   * 打开模态框
   */
  open() {
    if (this.isOpen) return
    
    this.isOpen = true
    document.body.appendChild(this.backdrop)
    document.body.style.overflow = 'hidden'
    
    // 设置焦点
    this.modal.focus()
  }

  /**
   * 关闭模态框
   */
  close() {
    if (!this.isOpen) return
    
    this.isOpen = false
    
    // 移除ESC键监听
    if (this.escapeHandler) {
      document.removeEventListener('keydown', this.escapeHandler)
    }
    
    // 添加关闭动画
    this.backdrop.classList.add('animate-fade-out')
    this.modal.classList.add('animate-scale-down')
    
    setTimeout(() => {
      if (this.backdrop.parentNode) {
        this.backdrop.parentNode.removeChild(this.backdrop)
      }
      document.body.style.overflow = 'auto'
    }, 200)
  }

  /**
   * 更新内容
   */
  updateContent(newChildren) {
    const body = this.modal.querySelector('.px-6')
    if (body) {
      body.innerHTML = ''
      
      if (typeof newChildren === 'string') {
        body.innerHTML = newChildren
      } else if (newChildren instanceof HTMLElement) {
        body.appendChild(newChildren)
      }
    }
  }

  /**
   * 静态工厂方法
   */
  static create(children, options = {}, props = {}) {
    const modal = new Modal(options)
    const element = modal.createElement(children, props)
    return { element, modal }
  }

  /**
   * 预设模态框
   */
  static confirm(options = {}) {
    const {
      title = '确认操作',
      message = '您确定要执行此操作吗？',
      confirmText = '确认',
      cancelText = '取消',
      onConfirm,
      onCancel
    } = options
    
    return new Promise((resolve) => {
      const modal = new Modal({
        size: 'sm',
        title,
        showFooter: true
      })
      
      // 创建消息内容
      const messageElement = document.createElement('p')
      messageElement.className = 'text-gray-700'
      messageElement.textContent = message
      
      // 创建按钮
      const cancelButton = document.createElement('button')
      cancelButton.className = 'btn btn-secondary btn-sm'
      cancelButton.textContent = cancelText
      cancelButton.addEventListener('click', () => {
        modal.close()
        if (onCancel) onCancel()
        resolve(false)
      })
      
      const confirmButton = document.createElement('button')
      confirmButton.className = 'btn btn-primary btn-sm'
      confirmButton.textContent = confirmText
      confirmButton.addEventListener('click', () => {
        modal.close()
        if (onConfirm) onConfirm()
        resolve(true)
      })
      
      const element = modal.createElement(messageElement, {
        onClose: () => {
          if (onCancel) onCancel()
          resolve(false)
        }
      })
      
      // 添加底部按钮
      const footer = modal.modal.querySelector('.border-t')
      if (footer) {
        const buttonContainer = document.createElement('div')
        buttonContainer.className = 'flex space-x-3 justify-end'
        buttonContainer.appendChild(cancelButton)
        buttonContainer.appendChild(confirmButton)
        footer.appendChild(buttonContainer)
      }
      
      modal.open()
    })
  }

  static alert(message, options = {}) {
    const {
      title = '提示',
      confirmText = '确定',
      onConfirm
    } = options
    
    return new Promise((resolve) => {
      const modal = new Modal({
        size: 'sm',
        title,
        showFooter: true
      })
      
      // 创建消息内容
      const messageElement = document.createElement('p')
      messageElement.className = 'text-gray-700'
      messageElement.textContent = message
      
      // 创建确定按钮
      const confirmButton = document.createElement('button')
      confirmButton.className = 'btn btn-primary btn-sm'
      confirmButton.textContent = confirmText
      confirmButton.addEventListener('click', () => {
        modal.close()
        if (onConfirm) onConfirm()
        resolve(true)
      })
      
      const element = modal.createElement(messageElement, {
        onClose: () => {
          if (onConfirm) onConfirm()
          resolve(true)
        }
      })
      
      // 添加底部按钮
      const footer = modal.modal.querySelector('.border-t')
      if (footer) {
        const buttonContainer = document.createElement('div')
        buttonContainer.className = 'flex justify-end'
        buttonContainer.appendChild(confirmButton)
        footer.appendChild(buttonContainer)
      }
      
      modal.open()
    })
  }
}

// 导出便利函数
export function createModal(children, options = {}, props = {}) {
  return Modal.create(children, options, props)
}

export function showConfirm(options = {}) {
  return Modal.confirm(options)
}

export function showAlert(message, options = {}) {
  return Modal.alert(message, options)
}