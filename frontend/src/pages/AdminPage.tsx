import React, { useState } from 'react'
import { 
  Users, 
  FileText, 
  BarChart3, 
  Settings, 
  Search, 
  Plus, 
  Shield, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Eye,
  Edit,
  Trash2,
  Filter
} from 'lucide-react'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Modal, { ConfirmModal } from '../components/ui/Modal'

// 模拟数据
const mockUsers = [
  {
    id: 1,
    username: 'john_doe',
    full_name: 'John Doe',
    email: 'john@example.com',
    is_active: true,
    is_admin: false,
    created_at: '2024-01-15T10:00:00Z',
    last_login: '2024-01-20T15:30:00Z',
    paper_count: 12,
    plan_count: 3,
  },
  {
    id: 2,
    username: 'jane_smith',
    full_name: 'Jane Smith',
    email: 'jane@example.com',
    is_active: true,
    is_admin: false,
    created_at: '2024-01-10T09:00:00Z',
    last_login: '2024-01-19T14:20:00Z',
    paper_count: 8,
    plan_count: 2,
  },
  {
    id: 3,
    username: 'inactive_user',
    full_name: 'Inactive User',
    email: 'inactive@example.com',
    is_active: false,
    is_admin: false,
    created_at: '2024-01-05T08:00:00Z',
    last_login: '2024-01-06T12:00:00Z',
    paper_count: 0,
    plan_count: 0,
  },
]

const mockSystemStats = {
  total_users: 156,
  active_users: 142,
  total_papers: 1247,
  total_analyses: 1189,
  total_plans: 234,
  average_analysis_time: 3.2,
  server_status: 'healthy',
  storage_used: '12.4 GB',
  storage_limit: '100 GB',
}

const AdminPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedUser, setSelectedUser] = useState<any>(null)
  const [showUserModal, setShowUserModal] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [userToDelete, setUserToDelete] = useState<any>(null)

  const tabs = [
    { id: 'overview', name: '系统概览', icon: BarChart3 },
    { id: 'users', name: '用户管理', icon: Users },
    { id: 'papers', name: '论文管理', icon: FileText },
    { id: 'system', name: '系统设置', icon: Settings },
  ]

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const filteredUsers = mockUsers.filter(user =>
    user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.full_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleDeleteUser = (user: any) => {
    setUserToDelete(user)
    setShowDeleteConfirm(true)
  }

  const confirmDeleteUser = () => {
    // 这里应该调用API删除用户
    console.log('Deleting user:', userToDelete)
    setShowDeleteConfirm(false)
    setUserToDelete(null)
  }

  const toggleUserStatus = (userId: number) => {
    // 这里应该调用API切换用户状态
    console.log('Toggling user status:', userId)
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            {/* 系统统计卡片 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardBody>
                  <div className="flex items-center">
                    <div className="p-3 bg-blue-500 rounded-lg">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">总用户数</p>
                      <p className="text-2xl font-bold text-gray-900">{mockSystemStats.total_users}</p>
                    </div>
                  </div>
                </CardBody>
              </Card>

              <Card>
                <CardBody>
                  <div className="flex items-center">
                    <div className="p-3 bg-green-500 rounded-lg">
                      <CheckCircle className="h-6 w-6 text-white" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">活跃用户</p>
                      <p className="text-2xl font-bold text-gray-900">{mockSystemStats.active_users}</p>
                    </div>
                  </div>
                </CardBody>
              </Card>

              <Card>
                <CardBody>
                  <div className="flex items-center">
                    <div className="p-3 bg-purple-500 rounded-lg">
                      <FileText className="h-6 w-6 text-white" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">论文总数</p>
                      <p className="text-2xl font-bold text-gray-900">{mockSystemStats.total_papers}</p>
                    </div>
                  </div>
                </CardBody>
              </Card>

              <Card>
                <CardBody>
                  <div className="flex items-center">
                    <div className="p-3 bg-yellow-500 rounded-lg">
                      <Clock className="h-6 w-6 text-white" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">平均分析时间</p>
                      <p className="text-2xl font-bold text-gray-900">{mockSystemStats.average_analysis_time}分钟</p>
                    </div>
                  </div>
                </CardBody>
              </Card>
            </div>

            {/* 系统状态 */}
            <Card>
              <CardHeader title="系统状态" />
              <CardBody>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">服务器状态</h4>
                      <p className="text-sm text-gray-600">所有服务正常运行</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span className="text-sm font-medium text-green-700">健康</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">存储使用</h4>
                      <p className="text-sm text-gray-600">
                        {mockSystemStats.storage_used} / {mockSystemStats.storage_limit}
                      </p>
                    </div>
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: '12.4%' }}
                      />
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">分析队列</h4>
                      <p className="text-sm text-gray-600">等待分析的论文数量</p>
                    </div>
                    <span className="text-lg font-semibold text-gray-900">3</span>
                  </div>
                </div>
              </CardBody>
            </Card>

            {/* 最近活动 */}
            <Card>
              <CardHeader title="最近活动" />
              <CardBody>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="p-2 bg-blue-100 rounded-full">
                      <Users className="h-4 w-4 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">新用户注册</p>
                      <p className="text-xs text-gray-600">jane_smith 刚刚注册了账户</p>
                    </div>
                    <span className="text-xs text-gray-500">5分钟前</span>
                  </div>

                  <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="p-2 bg-green-100 rounded-full">
                      <FileText className="h-4 w-4 text-green-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">论文分析完成</p>
                      <p className="text-xs text-gray-600">"Attention Is All You Need" 分析完成</p>
                    </div>
                    <span className="text-xs text-gray-500">15分钟前</span>
                  </div>

                  <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="p-2 bg-yellow-100 rounded-full">
                      <AlertTriangle className="h-4 w-4 text-yellow-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">系统警告</p>
                      <p className="text-xs text-gray-600">存储使用量达到70%</p>
                    </div>
                    <span className="text-xs text-gray-500">1小时前</span>
                  </div>
                </div>
              </CardBody>
            </Card>
          </div>
        )

      case 'users':
        return (
          <div className="space-y-6">
            {/* 用户管理控制栏 */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                  <input
                    type="text"
                    placeholder="搜索用户..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <Button variant="outline" size="sm" icon={<Filter size={16} />}>
                  筛选
                </Button>
              </div>
              <Button variant="primary" size="sm" icon={<Plus size={16} />}>
                新建用户
              </Button>
            </div>

            {/* 用户列表 */}
            <Card>
              <CardHeader title={`用户列表 (${filteredUsers.length})`} />
              <CardBody>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          用户信息
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          状态
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          统计
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          注册时间
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          操作
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {filteredUsers.map((user) => (
                        <tr key={user.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                                <span className="text-white font-medium text-sm">
                                  {user.full_name.charAt(0).toUpperCase()}
                                </span>
                              </div>
                              <div className="ml-4">
                                <div className="text-sm font-medium text-gray-900">
                                  {user.full_name}
                                </div>
                                <div className="text-sm text-gray-500">
                                  @{user.username}
                                </div>
                                <div className="text-sm text-gray-500">
                                  {user.email}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="space-y-1">
                              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                user.is_active
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {user.is_active ? '活跃' : '停用'}
                              </span>
                              {user.is_admin && (
                                <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                                  管理员
                                </span>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            <div>
                              <div>{user.paper_count} 篇论文</div>
                              <div className="text-gray-500">{user.plan_count} 个计划</div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(user.created_at)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                            <Button
                              size="sm"
                              variant="ghost"
                              icon={<Eye size={16} />}
                              onClick={() => {
                                setSelectedUser(user)
                                setShowUserModal(true)
                              }}
                            >
                              查看
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              icon={<Edit size={16} />}
                            >
                              编辑
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              icon={user.is_active ? <Shield size={16} /> : <CheckCircle size={16} />}
                              onClick={() => toggleUserStatus(user.id)}
                            >
                              {user.is_active ? '停用' : '启用'}
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              icon={<Trash2 size={16} />}
                              onClick={() => handleDeleteUser(user)}
                            >
                              删除
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardBody>
            </Card>
          </div>
        )

      case 'papers':
        return (
          <Card>
            <CardHeader title="论文管理" />
            <CardBody>
              <div className="text-center py-12">
                <FileText className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">论文管理功能</h3>
                <p className="mt-1 text-sm text-gray-500">
                  此功能正在开发中...
                </p>
              </div>
            </CardBody>
          </Card>
        )

      case 'system':
        return (
          <Card>
            <CardHeader title="系统设置" />
            <CardBody>
              <div className="text-center py-12">
                <Settings className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">系统设置功能</h3>
                <p className="mt-1 text-sm text-gray-500">
                  此功能正在开发中...
                </p>
              </div>
            </CardBody>
          </Card>
        )

      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">管理后台</h1>
        <p className="mt-2 text-gray-600">
          系统管理和用户管理控制台
        </p>
      </div>

      {/* 标签导航 */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="mr-2 h-5 w-5" />
                {tab.name}
              </button>
            )
          })}
        </nav>
      </div>

      {/* 标签内容 */}
      {renderTabContent()}

      {/* 用户详情模态框 */}
      <Modal
        isOpen={showUserModal}
        onClose={() => setShowUserModal(false)}
        title="用户详情"
        size="lg"
      >
        {selectedUser && (
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-xl">
                  {selectedUser.full_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {selectedUser.full_name}
                </h3>
                <p className="text-gray-600">@{selectedUser.username}</p>
                <p className="text-gray-600">{selectedUser.email}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-700">注册时间</p>
                <p className="text-sm text-gray-600">{formatDate(selectedUser.created_at)}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">最后登录</p>
                <p className="text-sm text-gray-600">{formatDate(selectedUser.last_login)}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">论文数量</p>
                <p className="text-sm text-gray-600">{selectedUser.paper_count} 篇</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">学习计划</p>
                <p className="text-sm text-gray-600">{selectedUser.plan_count} 个</p>
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* 删除确认对话框 */}
      <ConfirmModal
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={confirmDeleteUser}
        title="确认删除用户"
        message={`您确定要删除用户 "${userToDelete?.username}" 吗？此操作无法撤销。`}
        confirmText="删除"
        type="danger"
      />
    </div>
  )
}

export default AdminPage