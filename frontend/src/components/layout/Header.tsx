import React, { useState } from 'react'
import { Menu, Search, Bell, User, LogOut, Settings, ChevronDown } from 'lucide-react'
import { useAuthStore } from '../../stores/authStore'
import { useNavigate, Link } from 'react-router-dom'
import Button from '../ui/Button'

interface HeaderProps {
  onMenuClick: () => void
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
      <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
        {/* 左侧：菜单按钮 */}
        <div className="flex items-center">
          <button
            type="button"
            className="lg:hidden p-2 -ml-2 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-inset rounded-lg"
            onClick={onMenuClick}
          >
            <Menu size={20} />
          </button>
          
          {/* 桌面端 Logo */}
          <div className="hidden lg:flex lg:items-center lg:space-x-4">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">LP</span>
              </div>
              <span className="text-lg font-semibold text-gray-900">LearnPilot</span>
            </Link>
          </div>
        </div>

        {/* 中间：搜索框 */}
        <div className="flex-1 max-w-2xl mx-4">
          <form onSubmit={handleSearch} className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="搜索论文、概念、作者..."
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>
        </div>

        {/* 右侧：通知和用户菜单 */}
        <div className="flex items-center space-x-4">
          {/* 通知按钮 */}
          <button
            type="button"
            className="p-2 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-lg relative"
          >
            <Bell size={20} />
            {/* 未读通知徽章 */}
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* 用户菜单 */}
          <div className="relative">
            <button
              type="button"
              className="flex items-center space-x-2 p-2 text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-lg"
              onClick={() => setUserMenuOpen(!userMenuOpen)}
            >
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <User size={16} className="text-white" />
              </div>
              <div className="hidden md:block text-left">
                <p className="text-sm font-medium">{user?.full_name || user?.username}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <ChevronDown size={16} className="hidden md:block" />
            </button>

            {/* 下拉菜单 */}
            {userMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 z-50">
                <div className="py-1">
                  {/* 用户信息 */}
                  <div className="px-4 py-3 border-b border-gray-100">
                    <p className="text-sm font-medium text-gray-900">
                      {user?.full_name || user?.username}
                    </p>
                    <p className="text-sm text-gray-500">{user?.email}</p>
                  </div>

                  {/* 菜单项 */}
                  <Link
                    to="/settings"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setUserMenuOpen(false)}
                  >
                    <Settings size={16} className="mr-3" />
                    设置
                  </Link>

                  {user?.is_admin && (
                    <Link
                      to="/admin"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      <User size={16} className="mr-3" />
                      管理后台
                    </Link>
                  )}

                  <div className="border-t border-gray-100 my-1"></div>

                  <button
                    type="button"
                    className="w-full flex items-center px-4 py-2 text-sm text-red-700 hover:bg-red-50"
                    onClick={handleLogout}
                  >
                    <LogOut size={16} className="mr-3" />
                    退出登录
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 点击外部关闭用户菜单 */}
      {userMenuOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setUserMenuOpen(false)}
        />
      )}
    </header>
  )
}

export default Header