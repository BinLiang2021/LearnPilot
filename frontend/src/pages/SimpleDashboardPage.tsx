import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const SimpleDashboardPage: React.FC = () => {
  const navigate = useNavigate()

  useEffect(() => {
    // 检查是否有token
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const handleFeatureClick = (feature: string) => {
    switch (feature) {
      case 'upload':
        navigate('/upload')
        break
      case 'analysis':
        alert('📊 AI分析功能正在开发中...\n敬请期待！')
        break
      case 'graph':
        alert('🗺️ 知识图谱功能正在开发中...\n敬请期待！')
        break
      case 'plan':
        alert('📚 学习计划功能正在开发中...\n敬请期待！')
        break
      case 'profile':
        alert('👤 个人设置功能正在开发中...\n敬请期待！')
        break
      case 'history':
        alert('📈 学习进度功能正在开发中...\n敬请期待！')
        break
      default:
        alert('功能正在开发中，敬请期待！')
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f9fafb',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header */}
      <header style={{
        backgroundColor: 'white',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        padding: '16px 0'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{
              width: '40px',
              height: '40px',
              backgroundColor: '#3b82f6',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginRight: '12px'
            }}>
              <span style={{ color: 'white', fontWeight: 'bold', fontSize: '18px' }}>LP</span>
            </div>
            <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#1f2937' }}>
              LearnPilot
            </h1>
          </div>
          
          <button
            onClick={handleLogout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#ef4444',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            退出登录
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ padding: '40px 20px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Welcome Section */}
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '12px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            marginBottom: '30px'
          }}>
            <h2 style={{ margin: '0 0 16px 0', fontSize: '28px', fontWeight: 'bold', color: '#1f2937' }}>
              🎉 欢迎使用 LearnPilot！
            </h2>
            <p style={{ margin: 0, fontSize: '16px', color: '#6b7280', lineHeight: '1.5' }}>
              您已成功登录LearnPilot AI论文学习助手。开始您的智能学习之旅吧！
            </p>
          </div>

          {/* Feature Cards */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
            gap: '24px',
            marginBottom: '30px'
          }}>
            <div 
              onClick={() => handleFeatureClick('upload')}
              style={{
                backgroundColor: 'white',
                padding: '24px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}
            >
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#dbeafe',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px auto'
              }}>
                <span style={{ fontSize: '24px' }}>📄</span>
              </div>
              <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
                论文上传
              </h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#6b7280', lineHeight: '1.4' }}>
                上传PDF或Markdown格式的研究论文，AI将自动进行智能分析
              </p>
            </div>

            <div 
              onClick={() => handleFeatureClick('analysis')}
              style={{
                backgroundColor: 'white',
                padding: '24px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}
            >
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#dcfce7',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px auto'
              }}>
                <span style={{ fontSize: '24px' }}>🤖</span>
              </div>
              <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
                AI智能分析
              </h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#6b7280', lineHeight: '1.4' }}>
                AI自动识别研究问题、方法论、核心贡献和技术复杂度
              </p>
            </div>

            <div 
              onClick={() => handleFeatureClick('graph')}
              style={{
                backgroundColor: 'white',
                padding: '24px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}
            >
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#fef3c7',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px auto'
              }}>
                <span style={{ fontSize: '24px' }}>📊</span>
              </div>
              <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
                知识图谱
              </h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#6b7280', lineHeight: '1.4' }}>
                构建概念关系网络，可视化展示知识结构和依赖关系
              </p>
            </div>

            <div style={{
              backgroundColor: 'white',
              padding: '24px',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              textAlign: 'center'
            }}>
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#e0e7ff',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px auto'
              }}>
                <span style={{ fontSize: '24px' }}>📚</span>
              </div>
              <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
                学习计划
              </h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#6b7280', lineHeight: '1.4' }}>
                根据您的水平和时间生成个性化的学习路径和任务计划
              </p>
            </div>
          </div>

          {/* Getting Started */}
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '12px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
          }}>
            <h3 style={{ margin: '0 0 20px 0', fontSize: '20px', fontWeight: '600', color: '#1f2937' }}>
              🚀 开始使用
            </h3>
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '16px'
            }}>
              <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
                <strong style={{ color: '#1f2937' }}>步骤 1：</strong>
                <span style={{ color: '#6b7280', marginLeft: '8px' }}>上传您要学习的研究论文</span>
              </div>
              <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
                <strong style={{ color: '#1f2937' }}>步骤 2：</strong>
                <span style={{ color: '#6b7280', marginLeft: '8px' }}>查看AI生成的智能分析结果</span>
              </div>
              <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
                <strong style={{ color: '#1f2937' }}>步骤 3：</strong>
                <span style={{ color: '#6b7280', marginLeft: '8px' }}>获取个性化的学习计划</span>
              </div>
              <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
                <strong style={{ color: '#1f2937' }}>步骤 4：</strong>
                <span style={{ color: '#6b7280', marginLeft: '8px' }}>探索知识图谱，深入理解概念关系</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default SimpleDashboardPage