import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '../types'
import * as authApi from '../services/authApi'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  login: (username: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
  clearError: () => void
  checkAuth: () => Promise<void>
  updateProfile: (userData: Partial<User>) => Promise<void>
}

interface RegisterData {
  username: string
  email: string
  password: string
  full_name?: string
  language?: string
  research_interests?: string[]
}

type AuthStore = AuthState & AuthActions

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      login: async (username: string, password: string) => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await authApi.login({ username, password })
          
          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error: any) {
          set({
            error: error.message || '登录失败',
            isLoading: false,
            isAuthenticated: false,
            user: null,
            token: null,
          })
          throw error
        }
      },

      register: async (userData: RegisterData) => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await authApi.register(userData)
          
          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error: any) {
          set({
            error: error.message || '注册失败',
            isLoading: false,
          })
          throw error
        }
      },

      logout: () => {
        set(initialState)
        // 可以在这里添加 API 调用来通知服务器
      },

      clearError: () => {
        set({ error: null })
      },

      checkAuth: async () => {
        const { token } = get()
        if (!token) {
          return
        }

        try {
          set({ isLoading: true })
          const user = await authApi.getCurrentUser()
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          // Token 可能过期或无效
          set(initialState)
        }
      },

      updateProfile: async (userData: Partial<User>) => {
        try {
          set({ isLoading: true, error: null })
          
          const updatedUser = await authApi.updateProfile(userData)
          
          set({
            user: updatedUser,
            isLoading: false,
          })
        } catch (error: any) {
          set({
            error: error.message || '更新个人资料失败',
            isLoading: false,
          })
          throw error
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)