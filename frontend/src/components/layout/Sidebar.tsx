import React from 'react'
import { NavLink, Link } from 'react-router-dom'
import { 
  Home, 
  Upload, 
  BarChart3, 
  Calendar, 
  Network, 
  Settings, 
  Users, 
  X,
  BookOpen,
  Brain,
  Target
} from 'lucide-react'
import { useAuthStore } from '../../stores/authStore'
import { clsx } from 'clsx'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const navigationItems = [
  { name: '仪表板', href: '/dashboard', icon: Home },
  { name: '论文上传', href: '/upload', icon: Upload },
  { name: '分析结果', href: '/analysis', icon: BarChart3 },
  { name: '学习计划', href: '/plan', icon: Calendar },
  { name: '知识图谱', href: '/graph', icon: Network },
  { name: '设置', href: '/settings', icon: Settings },
]

const quickLinks = [
  { name: '我的论文', href: '/papers', icon: BookOpen },
  { name: '学习进度', href: '/progress', icon: Target },
  { name: '知识概念', href: '/concepts', icon: Brain },
]

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { user } = useAuthStore()

  const NavItem: React.FC<{
    item: { name: string; href: string; icon: React.ComponentType<any> }
  }> = ({ item }) => (
    <NavLink
      to={item.href}
      onClick={onClose}
      className={({ isActive }) =>
        clsx(
          'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200',
          isActive
            ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
        )
      }
    >
      {({ isActive }) => (
        <>
          <item.icon
            className={clsx(
              'mr-3 flex-shrink-0 h-5 w-5',
              isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-500'
            )}
          />
          {item.name}
        </>
      )}
    </NavLink>
  )

  const QuickLink: React.FC<{
    item: { name: string; href: string; icon: React.ComponentType<any> }
  }> = ({ item }) => (
    <Link
      to={item.href}
      onClick={onClose}
      className="group flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-200"
    >
      <item.icon className="mr-3 flex-shrink-0 h-4 w-4 text-gray-400 group-hover:text-gray-500" />
      {item.name}
    </Link>
  )

  return (
    <>
      {/* 桌面端侧边栏 */}
      <div className="hidden lg:flex lg:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex-1 min-h-0 bg-white border-r border-gray-200">
            <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
              {/* Logo */}
              <div className="flex items-center flex-shrink-0 px-6 mb-8">
                <Link to="/dashboard" className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">LP</span>
                  </div>
                  <span className="text-xl font-semibold text-gray-900">LearnPilot</span>
                </Link>
              </div>

              {/* 导航菜单 */}
              <nav className="flex-1 px-3 space-y-1">
                {navigationItems.map((item) => (
                  <NavItem key={item.name} item={item} />
                ))}

                {/* 管理员菜单 */}
                {user?.is_admin && (
                  <>
                    <div className="pt-6 pb-2">
                      <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        管理功能
                      </h3>
                    </div>
                    <NavItem item={{ name: '用户管理', href: '/admin', icon: Users }} />
                  </>
                )}

                {/* 快捷链接 */}
                <div className="pt-6 pb-2">
                  <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    快捷访问
                  </h3>
                </div>
                {quickLinks.map((item) => (
                  <QuickLink key={item.name} item={item} />
                ))}
              </nav>

              {/* 底部用户信息 */}
              <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
                <div className="flex items-center space-x-3 w-full group">
                  <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium text-sm">
                      {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {user?.full_name || user?.username}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {user?.email}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 移动端侧边栏 */}
      <div
        className={clsx(
          'fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out lg:hidden',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <Link to="/dashboard" className="flex items-center space-x-2" onClick={onClose}>
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">LP</span>
            </div>
            <span className="text-xl font-semibold text-gray-900">LearnPilot</span>
          </Link>
          <button
            type="button"
            className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg p-1"
            onClick={onClose}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navigationItems.map((item) => (
            <NavItem key={item.name} item={item} />
          ))}

          {/* 管理员菜单 */}
          {user?.is_admin && (
            <>
              <div className="pt-6 pb-2">
                <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  管理功能
                </h3>
              </div>
              <NavItem item={{ name: '用户管理', href: '/admin', icon: Users }} />
            </>
          )}

          {/* 快捷链接 */}
          <div className="pt-6 pb-2">
            <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
              快捷访问
            </h3>
          </div>
          {quickLinks.map((item) => (
            <QuickLink key={item.name} item={item} />
          ))}
        </nav>

        {/* 移动端底部用户信息 */}
        <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
          <div className="flex items-center space-x-3 w-full group">
            <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-white font-medium text-sm">
                {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.full_name || user?.username}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user?.email}
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar