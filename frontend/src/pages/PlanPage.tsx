import React, { useState } from 'react'
import { Plus, Calendar, Clock, BookOpen, Target, Play, Pause, CheckCircle, Circle } from 'lucide-react'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import Modal from '../components/ui/Modal'
import Input from '../components/ui/Input'

// 模拟数据
const mockPlans = [
  {
    id: 1,
    title: "Transformer架构深度学习",
    description: "系统学习Transformer相关论文和技术",
    papers: [
      { id: 1, title: "Attention Is All You Need", completed: true },
      { id: 2, title: "BERT: Pre-training of Deep Bidirectional Transformers", completed: true },
      { id: 3, title: "GPT: Improving Language Understanding", completed: false },
      { id: 4, title: "T5: Text-to-Text Transfer Transformer", completed: false },
      { id: 5, title: "Vision Transformer", completed: false },
    ],
    total_estimated_hours: 25,
    difficulty_level: "advanced",
    status: "active",
    progress: 40,
    created_at: "2024-01-10",
    due_date: "2024-02-15",
    milestones: [
      {
        id: 1,
        title: "基础概念理解",
        description: "理解注意力机制和Transformer基础",
        papers: [1, 2],
        estimated_hours: 10,
        status: "completed",
        completed_at: "2024-01-20"
      },
      {
        id: 2,
        title: "变体架构学习",
        description: "学习GPT、BERT等Transformer变体",
        papers: [3, 4],
        estimated_hours: 8,
        status: "in_progress",
      },
      {
        id: 3,
        title: "应用扩展",
        description: "了解Vision Transformer等跨领域应用",
        papers: [5],
        estimated_hours: 7,
        status: "not_started",
      }
    ]
  },
  {
    id: 2,
    title: "计算机视觉基础",
    description: "从CNN到现代视觉模型的学习路径",
    papers: [
      { id: 6, title: "ResNet: Deep Residual Learning", completed: false },
      { id: 7, title: "DenseNet: Densely Connected Networks", completed: false },
      { id: 8, title: "EfficientNet: Rethinking Model Scaling", completed: false },
    ],
    total_estimated_hours: 18,
    difficulty_level: "intermediate",
    status: "active",
    progress: 25,
    created_at: "2024-01-12",
    due_date: "2024-02-28",
    milestones: [
      {
        id: 4,
        title: "经典架构",
        description: "学习ResNet等经典卷积网络架构",
        papers: [6, 7],
        estimated_hours: 12,
        status: "in_progress",
      },
      {
        id: 5,
        title: "效率优化",
        description: "了解模型压缩和效率优化技术",
        papers: [8],
        estimated_hours: 6,
        status: "not_started",
      }
    ]
  }
]

const PlanPage: React.FC = () => {
  const [plans, setPlans] = useState(mockPlans)
  const [selectedPlan, setSelectedPlan] = useState<typeof mockPlans[0] | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newPlanTitle, setNewPlanTitle] = useState('')

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'completed': return 'bg-blue-100 text-blue-800'
      case 'paused': return 'bg-yellow-100 text-yellow-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
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

  const getMilestoneStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600'
      case 'in_progress': return 'text-blue-600'
      case 'not_started': return 'text-gray-400'
      default: return 'text-gray-400'
    }
  }

  const getMilestoneIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5" />
      case 'in_progress': return <Play className="w-5 h-5" />
      case 'not_started': return <Circle className="w-5 h-5" />
      default: return <Circle className="w-5 h-5" />
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN')
  }

  const createNewPlan = () => {
    // 这里应该调用API创建新计划
    setShowCreateModal(false)
    setNewPlanTitle('')
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">学习计划</h1>
          <p className="mt-2 text-gray-600">
            制定和管理您的个性化论文学习计划
          </p>
        </div>
        <Button 
          variant="primary" 
          icon={<Plus size={16} />}
          onClick={() => setShowCreateModal(true)}
        >
          新建计划
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 计划列表 */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader title="我的计划" />
            <CardBody>
              <div className="space-y-3">
                {plans.map((plan) => (
                  <div
                    key={plan.id}
                    className={`p-4 rounded-lg cursor-pointer transition-colors border ${
                      selectedPlan?.id === plan.id
                        ? 'bg-primary-50 border-primary-200'
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    }`}
                    onClick={() => setSelectedPlan(plan)}
                  >
                    <h4 className="font-medium text-gray-900 mb-2">
                      {plan.title}
                    </h4>
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {plan.description}
                    </p>
                    
                    <div className="flex items-center justify-between mb-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(plan.status)}`}>
                        {plan.status === 'active' ? '进行中' : '已完成'}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(plan.difficulty_level)}`}>
                        {plan.difficulty_level === 'advanced' ? '高级' : 
                         plan.difficulty_level === 'intermediate' ? '中级' : '初级'}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <BookOpen size={14} />
                        <span>{plan.papers.length} 篇论文</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock size={14} />
                        <span>{plan.total_estimated_hours}h</span>
                      </div>
                    </div>
                    
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span className="text-gray-600">进度</span>
                        <span className="font-medium">{plan.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${plan.progress}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* 计划详情 */}
        <div className="lg:col-span-2">
          {selectedPlan ? (
            <div className="space-y-6">
              {/* 计划概览 */}
              <Card>
                <CardBody>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h2 className="text-xl font-bold text-gray-900 mb-2">
                        {selectedPlan.title}
                      </h2>
                      <p className="text-gray-600 mb-4">
                        {selectedPlan.description}
                      </p>
                      <div className="flex items-center space-x-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedPlan.status)}`}>
                          {selectedPlan.status === 'active' ? '进行中' : '已完成'}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(selectedPlan.difficulty_level)}`}>
                          难度: {selectedPlan.difficulty_level === 'advanced' ? '高级' : 
                                selectedPlan.difficulty_level === 'intermediate' ? '中级' : '初级'}
                        </span>
                        <div className="flex items-center space-x-1 text-gray-600">
                          <Calendar size={16} />
                          <span className="text-sm">截止 {formatDate(selectedPlan.due_date)}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" icon={<Pause size={16} />}>
                        暂停
                      </Button>
                      <Button variant="outline" size="sm">
                        编辑
                      </Button>
                    </div>
                  </div>

                  {/* 整体进度 */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">整体进度</span>
                      <span className="text-sm font-bold text-gray-900">{selectedPlan.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all"
                        style={{ width: `${selectedPlan.progress}%` }}
                      />
                    </div>
                  </div>
                </CardBody>
              </Card>

              {/* 里程碑 */}
              <Card>
                <CardHeader title="学习里程碑" description="按阶段完成您的学习目标" />
                <CardBody>
                  <div className="space-y-4">
                    {selectedPlan.milestones.map((milestone, index) => (
                      <div key={milestone.id} className="flex items-start space-x-4">
                        <div className={`flex-shrink-0 ${getMilestoneStatusColor(milestone.status)}`}>
                          {getMilestoneIcon(milestone.status)}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <h4 className="font-medium text-gray-900">
                              {milestone.title}
                            </h4>
                            <div className="flex items-center space-x-2 text-sm text-gray-600">
                              <Clock size={14} />
                              <span>{milestone.estimated_hours}h</span>
                            </div>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">
                            {milestone.description}
                          </p>
                          <div className="flex items-center space-x-2 text-sm">
                            <span className="text-gray-500">
                              包含 {milestone.papers.length} 篇论文
                            </span>
                            {milestone.completed_at && (
                              <span className="text-green-600">
                                • 完成于 {formatDate(milestone.completed_at)}
                              </span>
                            )}
                          </div>
                          {index < selectedPlan.milestones.length - 1 && (
                            <div className="mt-3 ml-2 w-0.5 h-4 bg-gray-300"></div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardBody>
              </Card>

              {/* 论文列表 */}
              <Card>
                <CardHeader title="计划论文" description="按顺序阅读以下论文" />
                <CardBody>
                  <div className="space-y-3">
                    {selectedPlan.papers.map((paper, index) => (
                      <div
                        key={paper.id}
                        className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex-shrink-0">
                          {paper.completed ? (
                            <CheckCircle className="w-5 h-5 text-green-600" />
                          ) : (
                            <Circle className="w-5 h-5 text-gray-400" />
                          )}
                        </div>
                        <div className="flex-1">
                          <h4 className={`font-medium ${paper.completed ? 'text-gray-900' : 'text-gray-700'}`}>
                            {paper.title}
                          </h4>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-500">
                            #{index + 1}
                          </span>
                          <Button size="sm" variant="ghost">
                            查看
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardBody>
              </Card>
            </div>
          ) : (
            <Card>
              <CardBody>
                <div className="text-center py-12">
                  <Target className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">选择学习计划</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    从左侧列表中选择一个学习计划查看详细信息
                  </p>
                </div>
              </CardBody>
            </Card>
          )}
        </div>
      </div>

      {/* 新建计划模态框 */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="新建学习计划"
        description="创建个性化的论文学习计划"
      >
        <div className="space-y-4">
          <Input
            label="计划名称"
            placeholder="输入计划名称"
            value={newPlanTitle}
            onChange={(e) => setNewPlanTitle(e.target.value)}
            required
          />
          <div className="flex justify-end space-x-3 pt-4">
            <Button variant="ghost" onClick={() => setShowCreateModal(false)}>
              取消
            </Button>
            <Button variant="primary" onClick={createNewPlan}>
              创建计划
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default PlanPage