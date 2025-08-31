import { cn } from '../../utils/helpers.js'
import { generateId } from '../../utils/helpers.js'

/**
 * Input 组件
 * 支持标签、帮助文本、错误提示、图标等
 */
export class Input {
  constructor(options = {}) {
    this.options = {
      type: 'text',
      label: null,
      placeholder: '',
      helperText: null,
      error: null,
      leftIcon: null,
      rightIcon: null,
      size: 'md',
      variant: 'default',
      disabled: false,
      required: false,
      ...options
    }
    this.id = generateId()
  }

  /**
   * 创建输入框容器
   */
  createElement(props = {}) {
    const container = document.createElement('div')
    container.className = 'w-full'
    
    const { label, helperText, error, leftIcon, rightIcon } = this.options
    
    // 创建标签
    if (label) {
      const labelElement = this.createLabel()
      container.appendChild(labelElement)
    }
    
    // 创建输入框容器
    const inputContainer = this.createInputContainer()
    container.appendChild(inputContainer)
    
    // 创建左侧图标
    if (leftIcon) {
      const leftIconElement = this.createIcon(leftIcon, 'left')
      inputContainer.appendChild(leftIconElement)
    }
    
    // 创建输入框
    const input = this.createInput(props)
    inputContainer.appendChild(input)
    
    // 创建右侧图标
    if (rightIcon) {
      const rightIconElement = this.createIcon(rightIcon, 'right')
      inputContainer.appendChild(rightIconElement)
    }
    
    // 创建帮助文本或错误提示
    if (error || helperText) {
      const helpElement = this.createHelpText()
      container.appendChild(helpElement)
    }
    
    return container
  }

  /**
   * 创建标签元素
   */
  createLabel() {
    const label = document.createElement('label')
    label.htmlFor = this.id
    label.className = 'block text-sm font-medium text-gray-700 mb-1'
    label.textContent = this.options.label
    
    if (this.options.required) {
      const asterisk = document.createElement('span')
      asterisk.className = 'text-error-500 ml-1'
      asterisk.textContent = '*'
      label.appendChild(asterisk)
    }
    
    return label
  }

  /**
   * 创建输入框容器
   */
  createInputContainer() {
    const container = document.createElement('div')
    container.className = 'relative'
    return container
  }

  /**
   * 创建输入框
   */
  createInput(props = {}) {
    const input = document.createElement('input')
    const { type, placeholder, size, variant, disabled, leftIcon, rightIcon, error } = this.options
    
    // 基础属性
    input.id = this.id
    input.type = type
    input.placeholder = placeholder
    input.disabled = disabled
    
    if (this.options.required) {
      input.required = true
    }
    
    // 样式类
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-5 py-3 text-lg'
    }
    
    const variantClasses = {
      default: 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
      filled: 'border-0 bg-gray-100 focus:bg-white focus:ring-primary-500',
      outlined: 'border-2 border-gray-300 focus:border-primary-500'
    }
    
    const baseClasses = 'input'
    const sizeClass = sizeClasses[size]
    const variantClass = variantClasses[variant]
    const iconClasses = cn(
      leftIcon && 'pl-10',
      rightIcon && 'pr-10'
    )
    const errorClass = error && 'input-error'
    
    input.className = cn(baseClasses, sizeClass, variantClass, iconClasses, errorClass, props.className)
    
    // 绑定事件
    if (props.onChange) {
      input.addEventListener('input', props.onChange)
    }
    
    if (props.onFocus) {
      input.addEventListener('focus', props.onFocus)
    }
    
    if (props.onBlur) {
      input.addEventListener('blur', props.onBlur)
    }
    
    if (props.onKeyDown) {
      input.addEventListener('keydown', props.onKeyDown)
    }
    
    return input
  }

  /**
   * 创建图标元素
   */
  createIcon(icon, position) {
    const iconContainer = document.createElement('div')
    const positionClasses = {
      left: 'absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none',
      right: 'absolute inset-y-0 right-0 flex items-center pr-3'
    }
    
    iconContainer.className = positionClasses[position]
    
    let iconElement
    if (typeof icon === 'string') {
      iconElement = document.createElement('span')
      iconElement.className = 'text-gray-400 w-5 h-5'
      iconElement.innerHTML = icon
    } else if (icon instanceof HTMLElement) {
      iconElement = icon
      iconElement.className = cn(iconElement.className, 'text-gray-400 w-5 h-5')
    }
    
    if (iconElement) {
      iconContainer.appendChild(iconElement)
    }
    
    return iconContainer
  }

  /**
   * 创建帮助文本
   */
  createHelpText() {
    const helpElement = document.createElement('p')
    const { error, helperText } = this.options
    
    helpElement.className = cn(
      'mt-1 text-sm',
      error ? 'text-error-500' : 'text-gray-500'
    )
    helpElement.textContent = error || helperText
    
    return helpElement
  }

  /**
   * 更新输入框状态
   */
  updateState(container, newOptions) {
    this.options = { ...this.options, ...newOptions }
    
    // 重新渲染整个组件
    const parent = container.parentNode
    const newContainer = this.createElement()
    parent.replaceChild(newContainer, container)
    
    return newContainer
  }

  /**
   * 获取输入框值
   */
  getValue(container) {
    const input = container.querySelector('input')
    return input ? input.value : ''
  }

  /**
   * 设置输入框值
   */
  setValue(container, value) {
    const input = container.querySelector('input')
    if (input) {
      input.value = value
    }
  }

  /**
   * 设置焦点
   */
  focus(container) {
    const input = container.querySelector('input')
    if (input) {
      input.focus()
    }
  }

  /**
   * 设置错误状态
   */
  setError(container, error) {
    this.options.error = error
    return this.updateState(container, { error })
  }

  /**
   * 清除错误状态
   */
  clearError(container) {
    this.options.error = null
    return this.updateState(container, { error: null })
  }

  /**
   * 静态工厂方法
   */
  static create(options = {}, props = {}) {
    const input = new Input(options)
    return input.createElement(props)
  }

  /**
   * 预设输入框类型
   */
  static text(options = {}, props = {}) {
    return Input.create({ type: 'text', ...options }, props)
  }

  static email(options = {}, props = {}) {
    return Input.create({ type: 'email', ...options }, props)
  }

  static password(options = {}, props = {}) {
    return Input.create({ type: 'password', ...options }, props)
  }

  static number(options = {}, props = {}) {
    return Input.create({ type: 'number', ...options }, props)
  }

  static search(options = {}, props = {}) {
    return Input.create({ 
      type: 'search',
      leftIcon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>`,
      ...options 
    }, props)
  }
}

// 导出便利函数
export function createInput(options = {}, props = {}) {
  return Input.create(options, props)
}