import React, { useState, useEffect } from 'react'
import { Network, Download, Settings, ZoomIn, ZoomOut, RotateCw, Eye } from 'lucide-react'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'

// 模拟知识图谱数据
const mockGraphData = {
  nodes: [
    { id: 1, label: "Attention Mechanism", type: "concept", level: 1, importance: "critical" },
    { id: 2, label: "Transformer", type: "concept", level: 2, importance: "critical" },
    { id: 3, label: "BERT", type: "paper", level: 3, importance: "high" },
    { id: 4, label: "GPT", type: "paper", level: 3, importance: "high" },
    { id: 5, label: "Neural Networks", type: "concept", level: 0, importance: "critical" },
    { id: 6, label: "Sequence-to-Sequence", type: "concept", level: 1, importance: "medium" },
    { id: 7, label: "Self-Attention", type: "concept", level: 2, importance: "high" },
    { id: 8, label: "Multi-Head Attention", type: "concept", level: 2, importance: "high" },
    { id: 9, label: "Vision Transformer", type: "paper", level: 3, importance: "medium" },
    { id: 10, label: "T5", type: "paper", level: 3, importance: "medium" },
  ],
  edges: [
    { from: 5, to: 1, type: "prerequisite" },
    { from: 6, to: 1, type: "related" },
    { from: 1, to: 7, type: "derived" },
    { from: 1, to: 8, type: "derived" },
    { from: 7, to: 2, type: "applied" },
    { from: 8, to: 2, type: "applied" },
    { from: 2, to: 3, type: "applied" },
    { from: 2, to: 4, type: "applied" },
    { from: 2, to: 9, type: "applied" },
    { from: 2, to: 10, type: "applied" },
  ]
}

const GraphPage: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [layoutType, setLayoutType] = useState('force')
  const [zoom, setZoom] = useState(100)

  useEffect(() => {
    // 模拟加载图谱数据
    const timer = setTimeout(() => setLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return <LoadingSpinner message="正在生成知识图谱..." size="lg" />
  }

  const getNodeColor = (type: string, importance: string) => {
    if (type === 'concept') {
      switch (importance) {
        case 'critical': return 'bg-red-500'
        case 'high': return 'bg-orange-500'
        case 'medium': return 'bg-yellow-500'
        case 'low': return 'bg-gray-500'
        default: return 'bg-blue-500'
      }
    } else {
      return 'bg-green-500'
    }
  }

  const getNodeTypeIcon = (type: string) => {
    return type === 'concept' ? '💡' : '📄'
  }

  const handleNodeClick = (node: any) => {
    setSelectedNode(node)
  }

  const zoomIn = () => setZoom(prev => Math.min(prev + 10, 200))
  const zoomOut = () => setZoom(prev => Math.max(prev - 10, 50))

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">知识图谱</h1>
          <p className="mt-2 text-gray-600">
            可视化浏览论文中的概念关系和知识结构
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" icon={<Download size={16} />}>
            导出图谱
          </Button>
          <Button variant="outline" size="sm" icon={<Settings size={16} />}>
            设置
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 图谱控制面板 */}
        <div className="lg:col-span-1 space-y-6">
          {/* 布局控制 */}
          <Card>
            <CardHeader title="布局设置" />
            <CardBody>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    布局类型
                  </label>
                  <select
                    value={layoutType}
                    onChange={(e) => setLayoutType(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="force">力导向布局</option>
                    <option value="hierarchical">层次布局</option>
                    <option value="circular">圆形布局</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    缩放 ({zoom}%)
                  </label>
                  <div className="flex items-center space-x-2">
                    <Button size="sm" variant="outline" onClick={zoomOut}>
                      <ZoomOut size={16} />
                    </Button>
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${zoom}%` }}
                      />
                    </div>
                    <Button size="sm" variant="outline" onClick={zoomIn}>
                      <ZoomIn size={16} />
                    </Button>
                  </div>
                </div>

                <Button size="sm" variant="outline" fullWidth icon={<RotateCw size={16} />}>
                  重新布局
                </Button>
              </div>
            </CardBody>
          </Card>

          {/* 图例 */}
          <Card>
            <CardHeader title="图例说明" />
            <CardBody>
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">节点类型</h4>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">概念</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">论文</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">重要性</h4>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-red-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">关键</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-orange-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">重要</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">一般</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardBody>
          </Card>

          {/* 节点详情 */}
          {selectedNode && (
            <Card>
              <CardHeader title="节点详情" />
              <CardBody>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">
                      {getNodeTypeIcon(selectedNode.type)}
                    </span>
                    <h4 className="font-medium text-gray-900">
                      {selectedNode.label}
                    </h4>
                  </div>
                  
                  <div className="text-sm">
                    <p className="text-gray-600">类型: {selectedNode.type === 'concept' ? '概念' : '论文'}</p>
                    <p className="text-gray-600">层级: 第 {selectedNode.level + 1} 层</p>
                    <p className="text-gray-600">
                      重要性: {
                        selectedNode.importance === 'critical' ? '关键' :
                        selectedNode.importance === 'high' ? '重要' :
                        selectedNode.importance === 'medium' ? '一般' : '较低'
                      }
                    </p>
                  </div>

                  <div className="pt-2">
                    <Button size="sm" variant="outline" fullWidth icon={<Eye size={16} />}>
                      查看详情
                    </Button>
                  </div>
                </div>
              </CardBody>
            </Card>
          )}
        </div>

        {/* 主图谱显示区域 */}
        <div className="lg:col-span-3">
          <Card>
            <CardHeader 
              title="知识图谱可视化" 
              description="点击节点查看详细信息，拖拽节点调整布局"
            />
            <CardBody>
              <div className="relative bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 h-96 lg:h-[600px] overflow-hidden">
                {/* 模拟图谱显示 */}
                <div 
                  className="absolute inset-0 flex items-center justify-center"
                  style={{ transform: `scale(${zoom / 100})` }}
                >
                  <svg
                    width="100%"
                    height="100%"
                    viewBox="0 0 800 600"
                    className="absolute inset-0"
                  >
                    {/* 绘制连接线 */}
                    {mockGraphData.edges.map((edge, index) => {
                      const fromNode = mockGraphData.nodes.find(n => n.id === edge.from)
                      const toNode = mockGraphData.nodes.find(n => n.id === edge.to)
                      if (!fromNode || !toNode) return null
                      
                      // 简单的位置计算（实际应用中会更复杂）
                      const fromX = 100 + (fromNode.id % 5) * 150
                      const fromY = 100 + Math.floor(fromNode.level) * 120
                      const toX = 100 + (toNode.id % 5) * 150
                      const toY = 100 + Math.floor(toNode.level) * 120
                      
                      return (
                        <line
                          key={index}
                          x1={fromX}
                          y1={fromY}
                          x2={toX}
                          y2={toY}
                          stroke="#e5e7eb"
                          strokeWidth="2"
                          markerEnd="url(#arrowhead)"
                        />
                      )
                    })}
                    
                    {/* 箭头标记 */}
                    <defs>
                      <marker
                        id="arrowhead"
                        markerWidth="10"
                        markerHeight="7"
                        refX="9"
                        refY="3.5"
                        orient="auto"
                      >
                        <polygon
                          points="0 0, 10 3.5, 0 7"
                          fill="#e5e7eb"
                        />
                      </marker>
                    </defs>
                  </svg>
                  
                  {/* 绘制节点 */}
                  {mockGraphData.nodes.map((node) => {
                    const x = 100 + (node.id % 5) * 150
                    const y = 100 + Math.floor(node.level) * 120
                    
                    return (
                      <div
                        key={node.id}
                        className="absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer"
                        style={{ left: x, top: y }}
                        onClick={() => handleNodeClick(node)}
                      >
                        <div className={`
                          w-16 h-16 rounded-full flex items-center justify-center text-white font-medium text-sm
                          shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110
                          ${getNodeColor(node.type, node.importance)}
                          ${selectedNode?.id === node.id ? 'ring-4 ring-primary-300' : ''}
                        `}>
                          {getNodeTypeIcon(node.type)}
                        </div>
                        <div className="mt-2 text-center">
                          <div className="bg-white px-2 py-1 rounded shadow text-xs font-medium max-w-20 truncate">
                            {node.label}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
                
                {/* 无数据时的占位符 */}
                {mockGraphData.nodes.length === 0 && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center text-gray-500">
                      <Network className="h-12 w-12 mx-auto mb-2" />
                      <p>暂无知识图谱数据</p>
                      <p className="text-sm">上传并分析论文后即可生成</p>
                    </div>
                  </div>
                )}
              </div>
            </CardBody>
          </Card>

          {/* 图谱统计 */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardBody>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">概念节点</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {mockGraphData.nodes.filter(n => n.type === 'concept').length}
                    </p>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-lg">
                    <Network className="h-6 w-6 text-blue-600" />
                  </div>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardBody>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">论文节点</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {mockGraphData.nodes.filter(n => n.type === 'paper').length}
                    </p>
                  </div>
                  <div className="p-3 bg-green-100 rounded-lg">
                    <Network className="h-6 w-6 text-green-600" />
                  </div>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardBody>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">连接关系</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {mockGraphData.edges.length}
                    </p>
                  </div>
                  <div className="p-3 bg-purple-100 rounded-lg">
                    <Network className="h-6 w-6 text-purple-600" />
                  </div>
                </div>
              </CardBody>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GraphPage