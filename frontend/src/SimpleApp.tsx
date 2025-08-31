import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import SimpleLoginPage from './pages/SimpleLoginPage'
import SimpleRegisterPage from './pages/SimpleRegisterPage'
import SimpleDashboardPage from './pages/SimpleDashboardPage'
import SimpleUploadPage from './pages/SimpleUploadPage'

const SimpleApp: React.FC = () => {
  return (
    <div className="min-h-screen">
      <Routes>
        {/* 默认路由重定向到登录页 */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        {/* 登录和注册页面 */}
        <Route path="/login" element={<SimpleLoginPage />} />
        <Route path="/register" element={<SimpleRegisterPage />} />
        
        {/* Dashboard */}
        <Route path="/dashboard" element={<SimpleDashboardPage />} />
        
        {/* Upload */}
        <Route path="/upload" element={<SimpleUploadPage />} />
        
        {/* 404 - 重定向到登录 */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </div>
  )
}

export default SimpleApp