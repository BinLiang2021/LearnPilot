/**
 * 本地存储工具类
 */

class Storage {
  constructor(storage = localStorage) {
    this.storage = storage
  }

  /**
   * 设置存储项
   */
  set(key, value) {
    try {
      const serializedValue = JSON.stringify(value)
      this.storage.setItem(key, serializedValue)
      return true
    } catch (error) {
      console.error('存储失败:', error)
      return false
    }
  }

  /**
   * 获取存储项
   */
  get(key, defaultValue = null) {
    try {
      const item = this.storage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error('读取存储失败:', error)
      return defaultValue
    }
  }

  /**
   * 移除存储项
   */
  remove(key) {
    try {
      this.storage.removeItem(key)
      return true
    } catch (error) {
      console.error('移除存储失败:', error)
      return false
    }
  }

  /**
   * 清空所有存储
   */
  clear() {
    try {
      this.storage.clear()
      return true
    } catch (error) {
      console.error('清空存储失败:', error)
      return false
    }
  }

  /**
   * 检查是否存在某个key
   */
  has(key) {
    return this.storage.getItem(key) !== null
  }

  /**
   * 获取所有存储的keys
   */
  keys() {
    return Object.keys(this.storage)
  }

  /**
   * 获取存储大小（近似值）
   */
  size() {
    let total = 0
    for (let key in this.storage) {
      if (this.storage.hasOwnProperty(key)) {
        total += this.storage[key].length + key.length
      }
    }
    return total
  }
}

/**
 * 带过期时间的存储工具类
 */
class ExpiringStorage extends Storage {
  /**
   * 设置带过期时间的存储项
   */
  set(key, value, ttl = null) {
    const item = {
      value,
      timestamp: Date.now(),
      ttl
    }
    return super.set(key, item)
  }

  /**
   * 获取存储项，检查是否过期
   */
  get(key, defaultValue = null) {
    const item = super.get(key)
    
    if (!item) return defaultValue
    
    // 检查是否过期
    if (item.ttl && Date.now() - item.timestamp > item.ttl) {
      this.remove(key)
      return defaultValue
    }
    
    return item.value
  }

  /**
   * 清理过期项
   */
  cleanup() {
    const keys = this.keys()
    let cleaned = 0
    
    keys.forEach(key => {
      const item = super.get(key)
      if (item && item.ttl && Date.now() - item.timestamp > item.ttl) {
        this.remove(key)
        cleaned++
      }
    })
    
    return cleaned
  }
}

// 创建实例
export const localStorage_ = new Storage(window.localStorage)
export const sessionStorage_ = new Storage(window.sessionStorage)
export const expiringStorage = new ExpiringStorage(window.localStorage)

// 用户相关存储
export const userStorage = {
  setUser(user) {
    return localStorage_.set('user', user)
  },
  
  getUser() {
    return localStorage_.get('user')
  },
  
  removeUser() {
    return localStorage_.remove('user')
  },
  
  setToken(token) {
    return localStorage_.set('auth_token', token)
  },
  
  getToken() {
    return localStorage_.get('auth_token')
  },
  
  removeToken() {
    return localStorage_.remove('auth_token')
  },
  
  setPreferences(preferences) {
    return localStorage_.set('user_preferences', preferences)
  },
  
  getPreferences() {
    return localStorage_.get('user_preferences', {
      theme: 'light',
      language: 'zh-CN',
      notifications: true,
      analysisDepth: 'detailed',
      autoSave: true
    })
  }
}

// 应用设置存储
export const appStorage = {
  setSetting(key, value) {
    const settings = this.getSettings()
    settings[key] = value
    return localStorage_.set('app_settings', settings)
  },
  
  getSetting(key, defaultValue = null) {
    const settings = this.getSettings()
    return settings[key] ?? defaultValue
  },
  
  getSettings() {
    return localStorage_.get('app_settings', {})
  },
  
  resetSettings() {
    return localStorage_.remove('app_settings')
  }
}

// 缓存管理
export const cacheStorage = {
  set(key, data, ttl = 5 * 60 * 1000) { // 默认5分钟缓存
    return expiringStorage.set(`cache_${key}`, data, ttl)
  },
  
  get(key, defaultValue = null) {
    return expiringStorage.get(`cache_${key}`, defaultValue)
  },
  
  remove(key) {
    return expiringStorage.remove(`cache_${key}`)
  },
  
  cleanup() {
    return expiringStorage.cleanup()
  }
}

// 定期清理过期缓存
setInterval(() => {
  cacheStorage.cleanup()
}, 60000) // 每分钟清理一次