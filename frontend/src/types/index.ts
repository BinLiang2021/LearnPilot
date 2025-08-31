// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_admin: boolean
  language?: string
  research_interests?: string[]
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
  language?: string
  research_interests?: string[]
}

// 论文相关类型
export interface Paper {
  id: number
  title: string
  authors: string[]
  abstract: string
  keywords?: string[]
  publication_date?: string
  journal?: string
  doi?: string
  arxiv_id?: string
  pdf_path?: string
  markdown_path?: string
  user_id: number
  status: 'uploaded' | 'processing' | 'analyzed' | 'error'
  created_at: string
  updated_at: string
  analysis?: PaperAnalysis
  upload_progress?: number
}

export interface PaperAnalysis {
  id: number
  paper_id: number
  research_question: string
  methodology: string
  key_contributions: string[]
  difficulty_level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  estimated_reading_time: number
  prerequisites: string[]
  key_concepts: Concept[]
  summary: string
  strengths: string[]
  limitations: string[]
  created_at: string
}

export interface Concept {
  id: number
  name: string
  description: string
  importance: 'low' | 'medium' | 'high' | 'critical'
  category: string
  related_concepts: string[]
}

// 学习计划相关类型
export interface LearningPlan {
  id: number
  user_id: number
  title: string
  description: string
  papers: Paper[]
  total_estimated_hours: number
  difficulty_level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  status: 'draft' | 'active' | 'completed' | 'paused'
  progress: number
  milestones: Milestone[]
  created_at: string
  updated_at: string
}

export interface Milestone {
  id: number
  plan_id: number
  title: string
  description: string
  papers: number[]
  estimated_hours: number
  status: 'not_started' | 'in_progress' | 'completed'
  due_date?: string
  completed_at?: string
}

// 知识图谱相关类型
export interface KnowledgeGraph {
  id: number
  user_id: number
  title: string
  description: string
  papers: number[]
  nodes: GraphNode[]
  edges: GraphEdge[]
  layout: 'force' | 'hierarchical' | 'circular'
  created_at: string
  updated_at: string
}

export interface GraphNode {
  id: string
  label: string
  type: 'concept' | 'paper' | 'category'
  level: number
  importance: 'low' | 'medium' | 'high' | 'critical'
  description?: string
  papers?: number[]
  x?: number
  y?: number
}

export interface GraphEdge {
  id: string
  from: string
  to: string
  type: 'prerequisite' | 'related' | 'derived' | 'applied'
  strength: number
  description?: string
}

// API 响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// 上传相关类型
export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

export interface FileUploadResponse {
  paper_id: number
  filename: string
  size: number
  status: string
  message: string
}

// 设置相关类型
export interface UserPreferences {
  language: 'zh-CN' | 'en-US'
  theme: 'light' | 'dark' | 'auto'
  daily_learning_hours: number
  difficulty_preference: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  research_interests: string[]
  notification_settings: NotificationSettings
}

export interface NotificationSettings {
  email_notifications: boolean
  analysis_complete: boolean
  plan_reminders: boolean
  system_updates: boolean
}

// 统计相关类型
export interface UserStats {
  total_papers: number
  analyzed_papers: number
  active_plans: number
  completed_plans: number
  total_learning_hours: number
  current_streak: number
  longest_streak: number
  favorite_topics: string[]
}

export interface SystemStats {
  total_users: number
  active_users: number
  total_papers: number
  total_analyses: number
  total_plans: number
  average_analysis_time: number
}

// 表单相关类型
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'multiselect' | 'file'
  required?: boolean
  placeholder?: string
  options?: { value: string; label: string }[]
  validation?: {
    minLength?: number
    maxLength?: number
    pattern?: RegExp
    message?: string
  }
}

// 错误类型
export interface ApiError {
  message: string
  code: string
  details?: any
}

// 通知类型
export interface Notification {
  id: number
  user_id: number
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  is_read: boolean
  created_at: string
  action_url?: string
}

// 搜索相关类型
export interface SearchFilters {
  query?: string
  status?: string[]
  difficulty?: string[]
  date_range?: {
    start: string
    end: string
  }
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'difficulty'
  sort_order?: 'asc' | 'desc'
}