import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpen, 
  BarChart3, 
  Calendar, 
  Network, 
  Upload, 
  TrendingUp, 
  Clock,
  Target,
  Brain,
  Plus,
  ArrowRight
} from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'

// 模拟数据 - 在实际应用中应从API获取
const mockStats = {
  totalPapers: 12,
  analyzedPapers: 8,
  activePlans: 3,
  completedPlans: 1,
  totalLearningHours: 45,
  currentStreak: 7,
  weeklyProgress: 85,
}

const mockRecentPapers = [
  {
    id: 1,
    title: "Attention Is All You Need",
    status: "analyzed",
    difficulty: "advanced",
    createdAt: "2024-01-15",
    progress: 100,
  },
  {
    id: 2,
    title: "BERT: Pre-training of Deep Bidirectional Transformers",
    status: "analyzing",
    difficulty: "intermediate",
    createdAt: "2024-01-14",
    progress: 45,
  },
  {
    id: 3,
    title: "ResNet: Deep Residual Learning for Image Recognition",
    status: "uploaded",
    difficulty: "intermediate",
    createdAt: "2024-01-13",
    progress: 0,
  },
]

const mockRecentPlans = [
  {
    id: 1,
    title: "Transformer架构深度学习",
    papersCount: 5,
    progress: 60,
    dueDate: "2024-02-15",
    status: "active",
  },
  {
    id: 2,
    title: "计算机视觉基础",
    papersCount: 3,
    progress: 25,
    dueDate: "2024-02-28",
    status: "active",
  },
]

const DashboardPage: React.FC = () => {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 模拟加载数据
    const timer = setTimeout(() => setLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return <LoadingSpinner message="正在加载仪表板..." size="lg" />
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'analyzed': return 'bg-green-100 text-green-800'
      case 'analyzing': return 'bg-yellow-100 text-yellow-800'
      case 'uploaded': return 'bg-gray-100 text-gray-800'
      case 'error': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-blue-100 text-blue-800'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'advanced': return 'bg-orange-100 text-orange-800'
      case 'expert': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* 欢迎横幅 */}
      <div className="bg-gradient-to-r from-primary-600 to-blue-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">
              欢迎回来，{user?.full_name || user?.username}！
            </h1>
            <p className="text-primary-100">
              今天是您连续学习的第 {mockStats.currentStreak} 天，继续保持！
            </p>
          </div>
          <div className="hidden md:block">
            <div className="bg-white/10 rounded-lg px-4 py-2">
              <div className="text-sm font-medium">本周学习进度</div>
              <div className="text-2xl font-bold">{mockStats.weeklyProgress}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card hoverable className="bg-gradient-to-br from-blue-50 to-blue-100">
          <CardBody>
            <div className="flex items-center">
              <div className="p-3 bg-blue-500 rounded-lg">
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">论文总数</p>
                <p className="text-2xl font-bold text-gray-900">{mockStats.totalPapers}</p>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card hoverable className="bg-gradient-to-br from-green-50 to-green-100">
          <CardBody>
            <div className="flex items-center">
              <div className="p-3 bg-green-500 rounded-lg">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">已分析论文</p>
                <p className="text-2xl font-bold text-gray-900">{mockStats.analyzedPapers}</p>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card hoverable className="bg-gradient-to-br from-yellow-50 to-yellow-100">
          <CardBody>
            <div className="flex items-center">
              <div className="p-3 bg-yellow-500 rounded-lg">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">活跃计划</p>
                <p className="text-2xl font-bold text-gray-900">{mockStats.activePlans}</p>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card hoverable className="bg-gradient-to-br from-purple-50 to-purple-100">
          <CardBody>
            <div className="flex items-center">
              <div className="p-3 bg-purple-500 rounded-lg">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">学习时长</p>
                <p className="text-2xl font-bold text-gray-900">{mockStats.totalLearningHours}h</p>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* 主要内容区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 最近论文 */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader 
              title="最近论文" 
              description="您最近上传和处理的论文"
            >
              <div className="flex items-center space-x-2">
                <Button size="sm" variant="outline" icon={<Upload size={16} />}>
                  <Link to="/upload">上传论文</Link>
                </Button>
                <Button size="sm" variant="ghost">
                  <Link to="/analysis" className="flex items-center">
                    查看全部 <ArrowRight size={16} className="ml-1" />
                  </Link>
                </Button>
              </div>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                {mockRecentPapers.map((paper) => (
                  <div
                    key={paper.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-1">
                        {paper.title}
                      </h4>
                      <div className="flex items-center space-x-2 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(paper.status)}`}>
                          {paper.status === 'analyzed' ? '已分析' : 
                           paper.status === 'analyzing' ? '分析中' : '已上传'}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(paper.difficulty)}`}>
                          {paper.difficulty === 'advanced' ? '高级' : 
                           paper.difficulty === 'intermediate' ? '中级' : '初级'}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {paper.progress}%
                      </div>
                      <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                        <div 
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${paper.progress}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* 侧边栏 - 学习计划和快捷操作 */}
        <div className="space-y-6">
          {/* 学习计划 */}
          <Card>
            <CardHeader title="学习计划" description="您的活跃学习计划">
              <Button size="sm" variant="outline" icon={<Plus size={16} />}>
                <Link to="/plan">新建计划</Link>
              </Button>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {mockRecentPlans.map((plan) => (
                  <div key={plan.id} className="p-3 border border-gray-200 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-2">{plan.title}</h4>
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                      <span>{plan.papersCount} 篇论文</span>
                      <span>{plan.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-accent-600 h-2 rounded-full transition-all"
                        style={{ width: `${plan.progress}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>

          {/* 快捷操作 */}
          <Card>
            <CardHeader title="快捷操作" />
            <CardBody>
              <div className="grid grid-cols-1 gap-3">
                <Link
                  to="/upload"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors group"
                >
                  <Upload className="h-5 w-5 text-gray-400 group-hover:text-primary-600" />
                  <span className="ml-3 font-medium group-hover:text-primary-600">上传论文</span>
                </Link>
                <Link
                  to="/graph"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors group"
                >
                  <Network className="h-5 w-5 text-gray-400 group-hover:text-primary-600" />
                  <span className="ml-3 font-medium group-hover:text-primary-600">知识图谱</span>
                </Link>
                <Link
                  to="/plan"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors group"
                >
                  <Target className="h-5 w-5 text-gray-400 group-hover:text-primary-600" />
                  <span className="ml-3 font-medium group-hover:text-primary-600">制定计划</span>
                </Link>
                <Link
                  to="/concepts"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors group"
                >
                  <Brain className="h-5 w-5 text-gray-400 group-hover:text-primary-600" />
                  <span className="ml-3 font-medium group-hover:text-primary-600">浏览概念</span>
                </Link>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>

      {/* 学习趋势图表区域 - 占位符 */}
      <Card>
        <CardHeader 
          title="学习趋势" 
          description="您最近30天的学习活动统计"
        />
        <CardBody>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <div className="text-center text-gray-500">
              <TrendingUp className="h-12 w-12 mx-auto mb-2" />
              <p>学习趋势图表</p>
              <p className="text-sm">（图表组件将在后续版本中实现）</p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}

export default DashboardPage