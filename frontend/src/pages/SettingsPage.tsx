import React, { useState } from 'react'
import { User, Bell, Shield, Palette, Globe, Clock, Save } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import toast from 'react-hot-toast'

const SettingsPage: React.FC = () => {
  const { user, updateProfile } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('profile')

  // 个人资料表单状态
  const [profileForm, setProfileForm] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    research_interests: user?.research_interests || [],
    language: user?.language || 'zh-CN',
  })

  // 学习偏好状态
  const [preferences, setPreferences] = useState({
    daily_learning_hours: 2,
    difficulty_preference: 'intermediate',
    theme: 'light',
  })

  // 通知设置状态
  const [notifications, setNotifications] = useState({
    email_notifications: true,
    analysis_complete: true,
    plan_reminders: true,
    system_updates: false,
  })

  const tabs = [
    { id: 'profile', name: '个人资料', icon: User },
    { id: 'preferences', name: '学习偏好', icon: Clock },
    { id: 'notifications', name: '通知设置', icon: Bell },
    { id: 'appearance', name: '外观设置', icon: Palette },
    { id: 'security', name: '安全设置', icon: Shield },
  ]

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await updateProfile(profileForm)
      toast.success('个人资料更新成功！')
    } catch (error) {
      toast.error('更新失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handlePreferencesSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // 这里应该调用API更新偏好设置
    toast.success('偏好设置已保存！')
  }

  const handleNotificationsSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // 这里应该调用API更新通知设置
    toast.success('通知设置已保存！')
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <form onSubmit={handleProfileSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="全名"
                value={profileForm.full_name}
                onChange={(e) => setProfileForm(prev => ({ ...prev, full_name: e.target.value }))}
                placeholder="请输入您的全名"
              />
              <Input
                label="邮箱地址"
                type="email"
                value={profileForm.email}
                onChange={(e) => setProfileForm(prev => ({ ...prev, email: e.target.value }))}
                placeholder="请输入邮箱地址"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                语言偏好
              </label>
              <select
                value={profileForm.language}
                onChange={(e) => setProfileForm(prev => ({ ...prev, language: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="zh-CN">中文 (简体)</option>
                <option value="en-US">English</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                研究兴趣 (用逗号分隔)
              </label>
              <textarea
                value={profileForm.research_interests.join(', ')}
                onChange={(e) => setProfileForm(prev => ({ 
                  ...prev, 
                  research_interests: e.target.value.split(',').map(s => s.trim()).filter(s => s)
                }))}
                placeholder="如：机器学习, 自然语言处理, 计算机视觉"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <Button type="submit" loading={loading} icon={<Save size={16} />}>
              保存更改
            </Button>
          </form>
        )

      case 'preferences':
        return (
          <form onSubmit={handlePreferencesSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                每日学习时长目标
              </label>
              <select
                value={preferences.daily_learning_hours}
                onChange={(e) => setPreferences(prev => ({ 
                  ...prev, 
                  daily_learning_hours: Number(e.target.value) 
                }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value={0.5}>30分钟</option>
                <option value={1}>1小时</option>
                <option value={2}>2小时</option>
                <option value={3}>3小时</option>
                <option value={4}>4小时</option>
                <option value={5}>5小时以上</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                论文难度偏好
              </label>
              <select
                value={preferences.difficulty_preference}
                onChange={(e) => setPreferences(prev => ({ 
                  ...prev, 
                  difficulty_preference: e.target.value 
                }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="beginner">初学者</option>
                <option value="intermediate">中级</option>
                <option value="advanced">高级</option>
                <option value="expert">专家</option>
              </select>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-2">个性化建议</h4>
              <p className="text-blue-800 text-sm">
                基于您的设置，系统将为您推荐适合的论文和学习计划。
                您可以随时调整这些偏好以获得更好的学习体验。
              </p>
            </div>

            <Button type="submit" icon={<Save size={16} />}>
              保存偏好
            </Button>
          </form>
        )

      case 'notifications':
        return (
          <form onSubmit={handleNotificationsSubmit} className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">邮件通知</h4>
                  <p className="text-sm text-gray-600">接收重要更新的邮件通知</p>
                </div>
                <input
                  type="checkbox"
                  checked={notifications.email_notifications}
                  onChange={(e) => setNotifications(prev => ({ 
                    ...prev, 
                    email_notifications: e.target.checked 
                  }))}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">分析完成通知</h4>
                  <p className="text-sm text-gray-600">论文分析完成时通知您</p>
                </div>
                <input
                  type="checkbox"
                  checked={notifications.analysis_complete}
                  onChange={(e) => setNotifications(prev => ({ 
                    ...prev, 
                    analysis_complete: e.target.checked 
                  }))}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">学习计划提醒</h4>
                  <p className="text-sm text-gray-600">学习计划截止日期提醒</p>
                </div>
                <input
                  type="checkbox"
                  checked={notifications.plan_reminders}
                  onChange={(e) => setNotifications(prev => ({ 
                    ...prev, 
                    plan_reminders: e.target.checked 
                  }))}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">系统更新</h4>
                  <p className="text-sm text-gray-600">新功能和系统更新通知</p>
                </div>
                <input
                  type="checkbox"
                  checked={notifications.system_updates}
                  onChange={(e) => setNotifications(prev => ({ 
                    ...prev, 
                    system_updates: e.target.checked 
                  }))}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>
            </div>

            <Button type="submit" icon={<Save size={16} />}>
              保存通知设置
            </Button>
          </form>
        )

      case 'appearance':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                主题模式
              </label>
              <div className="grid grid-cols-3 gap-3">
                {['light', 'dark', 'auto'].map((theme) => (
                  <label
                    key={theme}
                    className={`
                      flex flex-col items-center p-4 border-2 rounded-lg cursor-pointer transition-all
                      ${preferences.theme === theme ? 'border-primary-500 bg-primary-50' : 'border-gray-200'}
                    `}
                  >
                    <input
                      type="radio"
                      name="theme"
                      value={theme}
                      checked={preferences.theme === theme}
                      onChange={(e) => setPreferences(prev => ({ ...prev, theme: e.target.value }))}
                      className="sr-only"
                    />
                    <div className={`w-8 h-8 rounded mb-2 ${
                      theme === 'light' ? 'bg-white border border-gray-300' :
                      theme === 'dark' ? 'bg-gray-800' : 'bg-gradient-to-r from-white to-gray-800'
                    }`}></div>
                    <span className="text-sm font-medium text-gray-900 capitalize">
                      {theme === 'light' ? '浅色' : theme === 'dark' ? '深色' : '自动'}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <Button icon={<Save size={16} />}>
              保存外观设置
            </Button>
          </div>
        )

      case 'security':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader title="修改密码" />
              <CardBody>
                <form className="space-y-4">
                  <Input
                    label="当前密码"
                    type="password"
                    placeholder="请输入当前密码"
                    required
                  />
                  <Input
                    label="新密码"
                    type="password"
                    placeholder="请输入新密码"
                    required
                  />
                  <Input
                    label="确认新密码"
                    type="password"
                    placeholder="请再次输入新密码"
                    required
                  />
                  <Button type="submit">
                    更新密码
                  </Button>
                </form>
              </CardBody>
            </Card>

            <Card>
              <CardHeader title="账户安全" />
              <CardBody>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">两步验证</h4>
                      <p className="text-sm text-gray-600">为您的账户添加额外安全层</p>
                    </div>
                    <Button variant="outline" size="sm">
                      启用
                    </Button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">登录活动</h4>
                      <p className="text-sm text-gray-600">查看最近的登录记录</p>
                    </div>
                    <Button variant="outline" size="sm">
                      查看详情
                    </Button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">数据导出</h4>
                      <p className="text-sm text-gray-600">下载您的个人数据</p>
                    </div>
                    <Button variant="outline" size="sm">
                      请求导出
                    </Button>
                  </div>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardHeader title="危险操作" />
              <CardBody>
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h4 className="font-medium text-red-900 mb-2">删除账户</h4>
                  <p className="text-red-800 text-sm mb-4">
                    删除账户将永久移除您的所有数据，包括论文、分析结果和学习计划。此操作无法撤销。
                  </p>
                  <Button variant="danger" size="sm">
                    删除账户
                  </Button>
                </div>
              </CardBody>
            </Card>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">设置</h1>
        <p className="mt-2 text-gray-600">
          管理您的账户设置和个人偏好
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 设置导航 */}
        <div className="lg:col-span-1">
          <Card>
            <CardBody>
              <nav className="space-y-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`
                        w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors text-left
                        ${activeTab === tab.id
                          ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                          : 'text-gray-700 hover:bg-gray-100'
                        }
                      `}
                    >
                      <Icon className="mr-3 h-5 w-5" />
                      {tab.name}
                    </button>
                  )
                })}
              </nav>
            </CardBody>
          </Card>
        </div>

        {/* 设置内容 */}
        <div className="lg:col-span-3">
          <Card>
            <CardHeader 
              title={tabs.find(tab => tab.id === activeTab)?.name} 
            />
            <CardBody>
              {renderTabContent()}
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage