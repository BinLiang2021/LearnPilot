import { cn } from '../../utils/helpers.js'

/**
 * Button 组件
 * 支持多种变体、尺寸和状态
 */
export class Button {
  constructor(options = {}) {
    this.options = {
      variant: 'primary',
      size: 'md',
      disabled: false,
      loading: false,
      fullWidth: false,
      leftIcon: null,
      rightIcon: null,
      ...options
    }
  }

  /**
   * 创建按钮元素
   */
  createElement(children, props = {}) {
    const button = document.createElement('button')
    const { variant, size, disabled, loading, fullWidth, leftIcon, rightIcon } = this.options
    
    // 基础样式类
    const baseClasses = 'btn'
    const variantClass = `btn-${variant}`
    const sizeClass = `btn-${size}`
    
    // 状态类
    const stateClasses = cn(
      fullWidth && 'w-full',
      (disabled || loading) && 'opacity-50 cursor-not-allowed'
    )
    
    // 合并所有类名
    button.className = cn(baseClasses, variantClass, sizeClass, stateClasses, props.className)
    
    // 设置属性
    button.disabled = disabled || loading
    
    if (props.ariaLabel) {
      button.setAttribute('aria-label', props.ariaLabel)
    }
    
    if (props.ariaDescribedBy) {
      button.setAttribute('aria-describedby', props.ariaDescribedBy)
    }

    // 添加内容
    this.renderContent(button, children, loading, leftIcon, rightIcon)
    
    // 绑定事件
    if (props.onClick && !disabled && !loading) {
      button.addEventListener('click', props.onClick)
    }
    
    return button
  }

  /**
   * 渲染按钮内容
   */
  renderContent(button, children, loading, leftIcon, rightIcon) {
    const content = document.createElement('div')
    content.className = 'flex items-center justify-center space-x-2'
    
    // Loading 状态
    if (loading) {
      const spinner = document.createElement('div')
      spinner.className = 'w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin'
      content.appendChild(spinner)
    } else if (leftIcon) {
      // 左侧图标
      const iconElement = this.createIcon(leftIcon)
      if (iconElement) content.appendChild(iconElement)
    }
    
    // 文字内容
    if (typeof children === 'string') {
      const textSpan = document.createElement('span')
      textSpan.textContent = children
      content.appendChild(textSpan)
    } else if (children instanceof HTMLElement) {
      content.appendChild(children)
    }
    
    // 右侧图标
    if (rightIcon && !loading) {
      const iconElement = this.createIcon(rightIcon)
      if (iconElement) content.appendChild(iconElement)
    }
    
    button.appendChild(content)
  }

  /**
   * 创建图标元素
   */
  createIcon(icon) {
    if (typeof icon === 'string') {
      const iconElement = document.createElement('span')
      iconElement.className = 'w-4 h-4'
      iconElement.innerHTML = icon
      return iconElement
    } else if (icon instanceof HTMLElement) {
      icon.className = cn(icon.className, 'w-4 h-4')
      return icon
    }
    return null
  }

  /**
   * 更新按钮状态
   */
  updateState(button, newOptions) {
    this.options = { ...this.options, ...newOptions }
    
    // 重新应用样式类
    const { variant, size, disabled, loading, fullWidth } = this.options
    const baseClasses = 'btn'
    const variantClass = `btn-${variant}`
    const sizeClass = `btn-${size}`
    const stateClasses = cn(
      fullWidth && 'w-full',
      (disabled || loading) && 'opacity-50 cursor-not-allowed'
    )
    
    button.className = cn(baseClasses, variantClass, sizeClass, stateClasses)
    button.disabled = disabled || loading
    
    // 重新渲染内容
    button.innerHTML = ''
    this.renderContent(button, newOptions.children || '', loading, 
                      this.options.leftIcon, this.options.rightIcon)
  }

  /**
   * 静态工厂方法
   */
  static create(children, options = {}, props = {}) {
    const button = new Button(options)
    return button.createElement(children, props)
  }

  /**
   * 预设按钮样式
   */
  static primary(children, options = {}, props = {}) {
    return Button.create(children, { variant: 'primary', ...options }, props)
  }

  static secondary(children, options = {}, props = {}) {
    return Button.create(children, { variant: 'secondary', ...options }, props)
  }

  static success(children, options = {}, props = {}) {
    return Button.create(children, { variant: 'success', ...options }, props)
  }

  static danger(children, options = {}, props = {}) {
    return Button.create(children, { variant: 'danger', ...options }, props)
  }

  static ghost(children, options = {}, props = {}) {
    return Button.create(children, { variant: 'ghost', ...options }, props)
  }
}

// 导出便利函数
export function createButton(children, options = {}, props = {}) {
  return Button.create(children, options, props)
}