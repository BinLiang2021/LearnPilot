import { cn } from '../../utils/helpers.js'

/**
 * Card 组件
 * 支持多种样式、交互状态和布局
 */
export class Card {
  constructor(options = {}) {
    this.options = {
      variant: 'default',
      padding: 'md',
      hoverable: false,
      clickable: false,
      header: null,
      footer: null,
      ...options
    }
  }

  /**
   * 创建卡片元素
   */
  createElement(children, props = {}) {
    const { variant, padding, hoverable, clickable, header, footer } = this.options
    
    // 决定使用的HTML标签
    const tag = clickable || props.onClick ? 'button' : 'div'
    const card = document.createElement(tag)
    
    // 基础样式类
    const baseClasses = 'card'
    const variantClasses = {
      default: 'shadow-sm',
      outlined: 'border border-gray-200 shadow-none',
      elevated: 'shadow-md'
    }
    
    const paddingClasses = {
      none: '',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8'
    }
    
    const interactionClasses = cn(
      hoverable && 'card-hover',
      clickable && 'card-clickable text-left w-full'
    )
    
    // 合并样式类
    card.className = cn(
      baseClasses,
      variantClasses[variant],
      paddingClasses[padding],
      interactionClasses,
      props.className
    )
    
    // 设置属性
    if (tag === 'button') {
      card.type = 'button'
      if (props.ariaLabel) {
        card.setAttribute('aria-label', props.ariaLabel)
      }
    }
    
    // 绑定事件
    if (props.onClick) {
      card.addEventListener('click', props.onClick)
    }
    
    // 渲染内容
    this.renderContent(card, children, header, footer, padding)
    
    return card
  }

  /**
   * 渲染卡片内容
   */
  renderContent(card, children, header, footer, padding) {
    // 渲染 header
    if (header) {
      const headerElement = this.createSection(header, 'header', padding)
      card.appendChild(headerElement)
    }
    
    // 渲染主要内容
    if (children) {
      const contentElement = this.createSection(children, 'content', padding)
      card.appendChild(contentElement)
    }
    
    // 渲染 footer
    if (footer) {
      const footerElement = this.createSection(footer, 'footer', padding)
      card.appendChild(footerElement)
    }
  }

  /**
   * 创建卡片区域
   */
  createSection(content, type, padding) {
    const section = document.createElement('div')
    
    // 设置区域样式
    const sectionClasses = {
      header: cn(
        'border-b border-gray-200 pb-4 mb-4',
        padding === 'none' && 'px-6 pt-6'
      ),
      content: cn(
        padding === 'none' && 'px-6'
      ),
      footer: cn(
        'border-t border-gray-200 pt-4 mt-4',
        padding === 'none' && 'px-6 pb-6'
      )
    }
    
    section.className = sectionClasses[type]
    
    // 添加内容
    if (typeof content === 'string') {
      section.innerHTML = content
    } else if (content instanceof HTMLElement) {
      section.appendChild(content)
    } else if (Array.isArray(content)) {
      content.forEach(item => {
        if (typeof item === 'string') {
          const textNode = document.createTextNode(item)
          section.appendChild(textNode)
        } else if (item instanceof HTMLElement) {
          section.appendChild(item)
        }
      })
    }
    
    return section
  }

  /**
   * 静态工厂方法
   */
  static create(children, options = {}, props = {}) {
    const card = new Card(options)
    return card.createElement(children, props)
  }

  /**
   * 预设卡片样式
   */
  static default(children, options = {}, props = {}) {
    return Card.create(children, { variant: 'default', ...options }, props)
  }

  static outlined(children, options = {}, props = {}) {
    return Card.create(children, { variant: 'outlined', ...options }, props)
  }

  static elevated(children, options = {}, props = {}) {
    return Card.create(children, { variant: 'elevated', ...options }, props)
  }

  static clickable(children, options = {}, props = {}) {
    return Card.create(children, { clickable: true, hoverable: true, ...options }, props)
  }
}

/**
 * 特殊卡片组件 - 统计卡片
 */
export class StatCard extends Card {
  constructor(options = {}) {
    super({
      variant: 'default',
      padding: 'md',
      ...options
    })
  }

  createElement(data, props = {}) {
    const { title, value, change, trend, icon } = data
    
    const card = super.createElement(null, props)
    
    // 创建统计卡片内容
    const content = document.createElement('div')
    content.className = 'flex items-center justify-between'
    
    // 左侧内容
    const leftContent = document.createElement('div')
    leftContent.className = 'flex-1'
    
    // 标题
    const titleElement = document.createElement('p')
    titleElement.className = 'text-sm font-medium text-gray-600'
    titleElement.textContent = title
    leftContent.appendChild(titleElement)
    
    // 数值
    const valueElement = document.createElement('p')
    valueElement.className = 'text-2xl font-bold text-gray-900 mt-1'
    valueElement.textContent = value
    leftContent.appendChild(valueElement)
    
    // 变化趋势
    if (change !== undefined) {
      const changeElement = document.createElement('p')
      const isPositive = change > 0
      const trendIcon = trend === 'up' ? '↗' : trend === 'down' ? '↘' : ''
      
      changeElement.className = cn(
        'text-sm font-medium mt-1 flex items-center',
        isPositive ? 'text-success-600' : 'text-error-600'
      )
      changeElement.innerHTML = `${trendIcon} ${Math.abs(change)}%`
      leftContent.appendChild(changeElement)
    }
    
    content.appendChild(leftContent)
    
    // 右侧图标
    if (icon) {
      const iconContainer = document.createElement('div')
      iconContainer.className = 'flex-shrink-0 w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center'
      
      if (typeof icon === 'string') {
        iconContainer.innerHTML = icon
      } else if (icon instanceof HTMLElement) {
        iconContainer.appendChild(icon)
      }
      
      content.appendChild(iconContainer)
    }
    
    card.appendChild(content)
    return card
  }

  static create(data, options = {}, props = {}) {
    const statCard = new StatCard(options)
    return statCard.createElement(data, props)
  }
}

/**
 * 论文卡片组件
 */
export class PaperCard extends Card {
  constructor(options = {}) {
    super({
      variant: 'default',
      padding: 'md',
      hoverable: true,
      ...options
    })
  }

  createElement(paper, props = {}) {
    const card = super.createElement(null, props)
    
    // 创建论文卡片内容
    const content = document.createElement('div')
    content.className = 'space-y-3'
    
    // 论文标题
    const titleElement = document.createElement('h3')
    titleElement.className = 'text-lg font-semibold text-gray-900 line-clamp-2'
    titleElement.textContent = paper.title
    content.appendChild(titleElement)
    
    // 作者信息
    if (paper.authors && paper.authors.length > 0) {
      const authorsElement = document.createElement('p')
      authorsElement.className = 'text-sm text-gray-600'
      authorsElement.textContent = paper.authors.slice(0, 3).join(', ') + 
        (paper.authors.length > 3 ? ` 等 ${paper.authors.length} 位作者` : '')
      content.appendChild(authorsElement)
    }
    
    // 论文摘要或描述
    if (paper.abstract || paper.description) {
      const abstractElement = document.createElement('p')
      abstractElement.className = 'text-sm text-gray-700 line-clamp-3'
      abstractElement.textContent = paper.abstract || paper.description
      content.appendChild(abstractElement)
    }
    
    // 底部信息栏
    const footer = document.createElement('div')
    footer.className = 'flex items-center justify-between pt-3 border-t border-gray-200'
    
    // 状态标签
    if (paper.status) {
      const statusBadge = document.createElement('span')
      const statusClasses = {
        uploading: 'badge badge-warning',
        analyzing: 'badge badge-primary',
        completed: 'badge badge-success',
        failed: 'badge badge-error'
      }
      statusBadge.className = cn('badge-sm', statusClasses[paper.status] || 'badge badge-primary')
      statusBadge.textContent = this.getStatusText(paper.status)
      footer.appendChild(statusBadge)
    }
    
    // 时间信息
    if (paper.uploadedAt || paper.createdAt) {
      const timeElement = document.createElement('span')
      timeElement.className = 'text-xs text-gray-500'
      const date = new Date(paper.uploadedAt || paper.createdAt)
      timeElement.textContent = date.toLocaleDateString('zh-CN')
      footer.appendChild(timeElement)
    }
    
    content.appendChild(footer)
    card.appendChild(content)
    
    return card
  }

  getStatusText(status) {
    const statusMap = {
      uploading: '上传中',
      analyzing: '分析中',
      completed: '已完成',
      failed: '失败'
    }
    return statusMap[status] || status
  }

  static create(paper, options = {}, props = {}) {
    const paperCard = new PaperCard(options)
    return paperCard.createElement(paper, props)
  }
}

// 导出便利函数
export function createCard(children, options = {}, props = {}) {
  return Card.create(children, options, props)
}

export function createStatCard(data, options = {}, props = {}) {
  return StatCard.create(data, options, props)
}

export function createPaperCard(paper, options = {}, props = {}) {
  return PaperCard.create(paper, options, props)
}