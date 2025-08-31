import React, { Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import Layout from './components/layout/Layout'
import LoadingSpinner from './components/ui/LoadingSpinner'

// 懒加载页面组件
const LoginPage = React.lazy(() => import('./pages/SimpleLoginPage'))
const RegisterPage = React.lazy(() => import('./pages/SimpleRegisterPage'))
const DashboardPage = React.lazy(() => import('./pages/SimpleDashboardPage'))
const UploadPage = React.lazy(() => import('./pages/UploadPage'))
const AnalysisPage = React.lazy(() => import('./pages/AnalysisPage'))
const PlanPage = React.lazy(() => import('./pages/PlanPage'))
const GraphPage = React.lazy(() => import('./pages/GraphPage'))
const SettingsPage = React.lazy(() => import('./pages/SettingsPage'))
const AdminPage = React.lazy(() => import('./pages/AdminPage'))

// 路由保护组件
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

// 管理员路由保护组件
const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, user } = useAuthStore()
  
  if (!isAuthenticated || !user?.is_admin) {
    return <Navigate to="/dashboard" replace />
  }
  
  return <>{children}</>
}

// 公开路由组件（已登录用户重定向到仪表板）
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }
  
  return <>{children}</>
}

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          {/* 公开路由 */}
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />

          {/* 受保护的路由 */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/upload" element={<UploadPage />} />
                    <Route path="/analysis" element={<AnalysisPage />} />
                    <Route path="/analysis/:paperId" element={<AnalysisPage />} />
                    <Route path="/plan" element={<PlanPage />} />
                    <Route path="/plan/:planId" element={<PlanPage />} />
                    <Route path="/graph" element={<GraphPage />} />
                    <Route path="/graph/:graphId" element={<GraphPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                    
                    {/* 管理员路由 */}
                    <Route
                      path="/admin"
                      element={
                        <AdminRoute>
                          <AdminPage />
                        </AdminRoute>
                      }
                    />
                    
                    {/* 404 页面 */}
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Suspense>
    </div>
  )
}

export default App