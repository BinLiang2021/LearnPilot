import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { Mail, Lock, User, UserCheck, ArrowRight } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Card from '../components/ui/Card'

interface RegisterFormData {
  username: string
  email: string
  full_name: string
  password: string
  confirmPassword: string
  acceptTerms: boolean
}

const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const { register: registerUser, isLoading } = useAuthStore()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch
  } = useForm<RegisterFormData>()

  const password = watch('password')

  const onSubmit = async (data: RegisterFormData) => {
    if (data.password !== data.confirmPassword) {
      toast.error('两次输入的密码不一致')
      return
    }

    if (!data.acceptTerms) {
      toast.error('请同意用户协议和隐私政策')
      return
    }

    try {
      await registerUser({
        username: data.username,
        email: data.email,
        password: data.password,
        full_name: data.full_name,
      })
      toast.success('注册成功！欢迎加入 LearnPilot！')
      navigate('/dashboard')
    } catch (error: any) {
      toast.error(error.message || '注册失败，请稍后重试')
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
            加入 LearnPilot
          </h1>
          <p className="mt-2 text-sm text-gray-600 text-center">
            创建您的账户<br />
            开启 AI 驱动的论文学习体验
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="py-8 px-6 shadow-xl bg-white/80 backdrop-blur-sm">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {/* 用户名输入 */}
            <div>
              <Input
                label="用户名"
                type="text"
                autoComplete="username"
                required
                fullWidth
                leftIcon={<User size={16} />}
                placeholder="请输入用户名"
                error={errors.username?.message}
                {...register('username', {
                  required: '请输入用户名',
                  minLength: {
                    value: 3,
                    message: '用户名至少3个字符'
                  },
                  pattern: {
                    value: /^[a-zA-Z0-9_]+$/,
                    message: '用户名只能包含字母、数字和下划线'
                  }
                })}
              />
            </div>

            {/* 邮箱输入 */}
            <div>
              <Input
                label="邮箱地址"
                type="email"
                autoComplete="email"
                required
                fullWidth
                leftIcon={<Mail size={16} />}
                placeholder="请输入邮箱地址"
                error={errors.email?.message}
                {...register('email', {
                  required: '请输入邮箱地址',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: '请输入有效的邮箱地址'
                  }
                })}
              />
            </div>

            {/* 全名输入 */}
            <div>
              <Input
                label="真实姓名"
                type="text"
                autoComplete="name"
                fullWidth
                leftIcon={<UserCheck size={16} />}
                placeholder="请输入真实姓名（可选）"
                error={errors.full_name?.message}
                {...register('full_name', {
                  minLength: {
                    value: 2,
                    message: '姓名至少2个字符'
                  }
                })}
              />
            </div>

            {/* 密码输入 */}
            <div>
              <Input
                label="密码"
                type="password"
                autoComplete="new-password"
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
                  },
                  pattern: {
                    value: /^(?=.*[a-z])(?=.*[A-Z\d])/,
                    message: '密码必须包含小写字母和大写字母或数字'
                  }
                })}
              />
            </div>

            {/* 确认密码输入 */}
            <div>
              <Input
                label="确认密码"
                type="password"
                autoComplete="new-password"
                required
                fullWidth
                leftIcon={<Lock size={16} />}
                placeholder="请再次输入密码"
                error={errors.confirmPassword?.message}
                {...register('confirmPassword', {
                  required: '请确认密码',
                  validate: value => value === password || '两次输入的密码不一致'
                })}
              />
            </div>

            {/* 同意条款 */}
            <div className="flex items-start">
              <input
                id="accept-terms"
                type="checkbox"
                className="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                {...register('acceptTerms', {
                  required: '请同意用户协议和隐私政策'
                })}
              />
              <label htmlFor="accept-terms" className="ml-2 text-sm text-gray-700">
                我同意{' '}
                <Link
                  to="/terms"
                  className="text-primary-600 hover:text-primary-500 font-medium"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  用户协议
                </Link>
                {' '}和{' '}
                <Link
                  to="/privacy"
                  className="text-primary-600 hover:text-primary-500 font-medium"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  隐私政策
                </Link>
              </label>
            </div>

            {errors.acceptTerms && (
              <p className="text-sm text-red-600 mt-1">
                {errors.acceptTerms.message}
              </p>
            )}

            {/* 注册按钮 */}
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={isSubmitting || isLoading}
              icon={<ArrowRight size={18} />}
              iconPosition="right"
            >
              注册账户
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

            {/* 登录链接 */}
            <div className="text-center">
              <span className="text-sm text-gray-600">
                已有账户？{' '}
                <Link
                  to="/login"
                  className="font-medium text-primary-600 hover:text-primary-500 transition-colors"
                >
                  立即登录
                </Link>
              </span>
            </div>
          </form>
        </Card>

        {/* 安全提示 */}
        <div className="mt-8 text-center">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-700">
            <h3 className="font-medium mb-2">🔒 您的数据安全</h3>
            <p>
              我们采用企业级加密技术保护您的数据，
              并承诺不会泄露您的个人信息和学习内容。
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage