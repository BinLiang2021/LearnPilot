import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Card from '../components/ui/Card'

interface LoginFormData {
  username: string
  password: string
}

const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const { login, isLoading, error } = useAuthStore()
  const [showPassword, setShowPassword] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginFormData>()

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.username, data.password)
      toast.success('登录成功！')
      navigate('/dashboard')
    } catch (error: any) {
      toast.error(error.message || '登录失败，请检查用户名和密码')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-blue-50 to-indigo-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        {/* Logo 和标题 */}
        <div className="flex flex-col items-center">
          <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-2xl">LP</span>
          </div>
          <h1 className="mt-6 text-3xl font-bold text-gray-900">
            欢迎回来
          </h1>
          <p className="mt-2 text-sm text-gray-600 text-center">
            登录到您的 LearnPilot 账户<br />
            开始您的 AI 论文学习之旅
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="py-8 px-6 shadow-xl bg-white/80 backdrop-blur-sm">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {/* 用户名输入 */}
            <div>
              <Input
                label="用户名或邮箱"
                type="text"
                autoComplete="username"
                required
                fullWidth
                leftIcon={<Mail size={16} />}
                placeholder="请输入用户名或邮箱"
                error={errors.username?.message}
                {...register('username', {
                  required: '请输入用户名或邮箱',
                  minLength: {
                    value: 3,
                    message: '用户名至少3个字符'
                  }
                })}
              />
            </div>

            {/* 密码输入 */}
            <div>
              <Input
                label="密码"
                type="password"
                autoComplete="current-password"
                required
                fullWidth
                leftIcon={<Lock size={16} />}
                placeholder="请输入密码"
                error={errors.password?.message}
                {...register('password', {
                  required: '请输入密码',
                  minLength: {
                    value: 6,
                    message: '密码至少6个字符'
                  }
                })}
              />
            </div>

            {/* 记住我和忘记密码 */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
                  记住我
                </label>
              </div>
              
              <Link
                to="/forgot-password"
                className="text-sm text-primary-600 hover:text-primary-500 font-medium"
              >
                忘记密码？
              </Link>
            </div>

            {/* 登录按钮 */}
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={isSubmitting || isLoading}
              icon={<ArrowRight size={18} />}
              iconPosition="right"
            >
              登录
            </Button>

            {/* 分割线 */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">或</span>
              </div>
            </div>

            {/* 注册链接 */}
            <div className="text-center">
              <span className="text-sm text-gray-600">
                还没有账户？{' '}
                <Link
                  to="/register"
                  className="font-medium text-primary-600 hover:text-primary-500 transition-colors"
                >
                  立即注册
                </Link>
              </span>
            </div>
          </form>
        </Card>

        {/* 功能特色 */}
        <div className="mt-8 text-center">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 text-sm text-gray-600">
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center mb-2">
                <span className="text-primary-600 font-semibold">AI</span>
              </div>
              <span>智能论文分析</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 bg-accent-100 rounded-full flex items-center justify-center mb-2">
                <span className="text-accent-600 font-semibold">📊</span>
              </div>
              <span>知识图谱可视化</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                <span className="text-blue-600 font-semibold">📚</span>
              </div>
              <span>个性化学习计划</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage