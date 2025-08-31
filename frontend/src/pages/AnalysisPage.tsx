import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { 
  FileText, 
  Clock, 
  BarChart3, 
  Brain, 
  Users, 
  Calendar, 
  Download,
  Eye,
  Star,
  Tag,
  ArrowLeft,
  ExternalLink
} from 'lucide-react'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'

// 模拟数据
const mockPapers = [
  {
    id: 1,
    title: "Attention Is All You Need",
    authors: ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
    status: "analyzed",
    difficulty: "advanced",
    createdAt: "2024-01-15",
    analysis: {
      research_question: "如何设计一个完全基于注意力机制的神经网络架构来处理序列到序列的任务？",
      methodology: "提出了Transformer架构，完全依赖自注意力机制，摒弃了循环和卷积结构。",
      key_contributions: [
        "提出了完全基于注意力机制的Transformer架构",
        "在机器翻译任务上达到了当时最先进的性能",
        "大大减少了训练时间，提高了并行化程度"
      ],
      difficulty_level: "advanced",
      estimated_reading_time: 45,
      prerequisites: ["深度学习基础", "注意力机制", "序列到序列模型"],
      summary: "本文提出了Transformer架构，这是一种完全基于注意力机制的神经网络模型...",
      strengths: ["创新的架构设计", "优秀的性能表现", "高度可并行化"],
      limitations: ["对位置编码的依赖", "注意力复杂度较高", "需要大量数据训练"]
    }
  },
  {
    id: 2,
    title: "BERT: Pre-training of Deep Bidirectional Transformers",
    authors: ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee"],
    status: "analyzing",
    difficulty: "intermediate",
    createdAt: "2024-01-14",
    progress: 65
  }
]

const AnalysisPage: React.FC = () => {
  const { paperId } = useParams()
  const [papers, setPapers] = useState(mockPapers)
  const [selectedPaper, setSelectedPaper] = useState(paperId ? mockPapers[0] : null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 模拟加载数据
    const timer = setTimeout(() => setLoading(false), 800)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return <LoadingSpinner message="正在加载分析结果..." size="lg" />
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'analyzed': return 'bg-green-100 text-green-800'
      case 'analyzing': return 'bg-yellow-100 text-yellow-800'
      case 'uploaded': return 'bg-gray-100 text-gray-800'
      case 'error': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">论文分析</h1>
          <p className="mt-2 text-gray-600">
            查看AI分析的论文内容、概念和学习建议
          </p>
        </div>
        {selectedPaper && (
          <Button variant="ghost" icon={<ArrowLeft size={16} />}>
            <Link to="/analysis">返回列表</Link>
          </Button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 论文列表 */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader title="论文列表" />
            <CardBody>
              <div className="space-y-3">
                {papers.map((paper) => (
                  <div
                    key={paper.id}
                    className={`p-3 rounded-lg cursor-pointer transition-colors border ${
                      selectedPaper?.id === paper.id
                        ? 'bg-primary-50 border-primary-200'
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    }`}
                    onClick={() => setSelectedPaper(paper)}
                  >
                    <h4 className="font-medium text-gray-900 text-sm mb-2 line-clamp-2">
                      {paper.title}
                    </h4>
                    <div className="flex items-center justify-between">
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
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* 详细分析内容 */}
        <div className="lg:col-span-3">
          {selectedPaper ? (
            <div className="space-y-6">
              {/* 论文基本信息 */}
              <Card>
                <CardBody>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h2 className="text-xl font-bold text-gray-900 mb-2">
                        {selectedPaper.title}
                      </h2>
                      <p className="text-gray-600 mb-3">
                        {selectedPaper.authors.join(", ")}
                      </p>
                      <div className="flex items-center space-x-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedPaper.status)}`}>
                          {selectedPaper.status === 'analyzed' ? '已分析' : '分析中'}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(selectedPaper.difficulty)}`}>
                          难度: {selectedPaper.difficulty === 'advanced' ? '高级' : 
                                selectedPaper.difficulty === 'intermediate' ? '中级' : '初级'}
                        </span>
                        {selectedPaper.analysis && (
                          <div className="flex items-center space-x-1 text-gray-600">
                            <Clock size={16} />
                            <span className="text-sm">预估 {selectedPaper.analysis.estimated_reading_time} 分钟</span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" icon={<Eye size={16} />}>
                        预览
                      </Button>
                      <Button variant="outline" size="sm" icon={<Download size={16} />}>
                        下载
                      </Button>
                    </div>
                  </div>
                </CardBody>
              </Card>

              {selectedPaper.status === 'analyzing' && (
                <Card>
                  <CardBody>
                    <div className="text-center py-8">
                      <LoadingSpinner size="lg" message="AI正在分析论文内容，请稍候..." />
                      <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${selectedPaper.progress}%` }}
                        />
                      </div>
                      <p className="mt-2 text-sm text-gray-600">分析进度: {selectedPaper.progress}%</p>
                    </div>
                  </CardBody>
                </Card>
              )}

              {selectedPaper.analysis && (
                <>
                  {/* 论文摘要和关键信息 */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Card>
                      <CardHeader title="研究问题" />
                      <CardBody>
                        <p className="text-gray-700">
                          {selectedPaper.analysis.research_question}
                        </p>
                      </CardBody>
                    </Card>

                    <Card>
                      <CardHeader title="研究方法" />
                      <CardBody>
                        <p className="text-gray-700">
                          {selectedPaper.analysis.methodology}
                        </p>
                      </CardBody>
                    </Card>
                  </div>

                  {/* 主要贡献 */}
                  <Card>
                    <CardHeader title="主要贡献" />
                    <CardBody>
                      <ul className="space-y-2">
                        {selectedPaper.analysis.key_contributions.map((contribution, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <span className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></span>
                            <span className="text-gray-700">{contribution}</span>
                          </li>
                        ))}
                      </ul>
                    </CardBody>
                  </Card>

                  {/* 详细分析 */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <Card>
                      <CardHeader title="前置知识" />
                      <CardBody>
                        <div className="space-y-2">
                          {selectedPaper.analysis.prerequisites.map((prereq, index) => (
                            <span
                              key={index}
                              className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-md text-sm mr-2 mb-2"
                            >
                              {prereq}
                            </span>
                          ))}
                        </div>
                      </CardBody>
                    </Card>

                    <Card>
                      <CardHeader title="论文优势" />
                      <CardBody>
                        <ul className="space-y-2">
                          {selectedPaper.analysis.strengths.map((strength, index) => (
                            <li key={index} className="flex items-center space-x-2">
                              <Star className="w-4 h-4 text-green-500" />
                              <span className="text-sm text-gray-700">{strength}</span>
                            </li>
                          ))}
                        </ul>
                      </CardBody>
                    </Card>

                    <Card>
                      <CardHeader title="局限性" />
                      <CardBody>
                        <ul className="space-y-2">
                          {selectedPaper.analysis.limitations.map((limitation, index) => (
                            <li key={index} className="flex items-start space-x-2">
                              <span className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></span>
                              <span className="text-sm text-gray-700">{limitation}</span>
                            </li>
                          ))}
                        </ul>
                      </CardBody>
                    </Card>
                  </div>

                  {/* 论文摘要 */}
                  <Card>
                    <CardHeader title="AI生成摘要" />
                    <CardBody>
                      <p className="text-gray-700 leading-relaxed">
                        {selectedPaper.analysis.summary}
                      </p>
                    </CardBody>
                  </Card>

                  {/* 学习建议 */}
                  <Card>
                    <CardHeader title="学习建议" />
                    <CardBody>
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 className="font-medium text-blue-900 mb-2">💡 个性化建议</h4>
                        <div className="space-y-2 text-blue-800">
                          <p>• 建议先学习注意力机制和序列到序列模型的基础知识</p>
                          <p>• 可以结合代码实现来理解Transformer的具体工作原理</p>
                          <p>• 推荐阅读相关的后续改进论文，如BERT、GPT等</p>
                        </div>
                        <div className="mt-4 flex space-x-2">
                          <Button size="sm" variant="outline">
                            <Link to="/plan" className="flex items-center">
                              制定学习计划 <ArrowLeft className="ml-1 w-4 h-4" />
                            </Link>
                          </Button>
                          <Button size="sm" variant="outline">
                            <Link to="/graph" className="flex items-center">
                              查看知识图谱 <ExternalLink className="ml-1 w-4 h-4" />
                            </Link>
                          </Button>
                        </div>
                      </div>
                    </CardBody>
                  </Card>
                </>
              )}
            </div>
          ) : (
            <Card>
              <CardBody>
                <div className="text-center py-12">
                  <FileText className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">选择一篇论文</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    从左侧列表中选择一篇论文查看详细的AI分析结果
                  </p>
                </div>
              </CardBody>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default AnalysisPage