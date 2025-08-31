import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const SimpleUploadPage: React.FC = () => {
  const navigate = useNavigate()
  const [files, setFiles] = useState<FileList | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error' | 'info'>('info')

  useEffect(() => {
    // 检查是否有token
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
    }
  }, [navigate])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files
    setFiles(selectedFiles)
    if (selectedFiles && selectedFiles.length > 0) {
      setMessage(`已选择 ${selectedFiles.length} 个文件`)
      setMessageType('info')
    }
  }

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      setMessage('请先选择文件')
      setMessageType('error')
      return
    }

    setUploading(true)
    setMessage('正在上传文件...')
    setMessageType('info')

    try {
      // 创建FormData用于文件上传
      const formData = new FormData()
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i])
      }

      // 发送到后端API
      const response = await fetch('/api/papers/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        const result = await response.json()
        setMessage(`成功上传 ${files.length} 个文件！${result.message || ''}`)
        setMessageType('success')
        setFiles(null)
        
        // 清空文件选择
        const fileInput = document.getElementById('file-input') as HTMLInputElement
        if (fileInput) fileInput.value = ''
      } else {
        const error = await response.json()
        setMessage(`上传失败: ${error.detail || '请重试'}`)
        setMessageType('error')
      }
    } catch (error) {
      setMessage('上传失败：网络错误，请重试')
      setMessageType('error')
      console.error('Upload error:', error)
    } finally {
      setUploading(false)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.currentTarget.style.backgroundColor = '#f0f9ff'
    e.currentTarget.style.borderColor = '#3b82f6'
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    e.currentTarget.style.backgroundColor = '#f9fafb'
    e.currentTarget.style.borderColor = '#d1d5db'
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.currentTarget.style.backgroundColor = '#f9fafb'
    e.currentTarget.style.borderColor = '#d1d5db'
    
    const droppedFiles = e.dataTransfer.files
    setFiles(droppedFiles)
    if (droppedFiles && droppedFiles.length > 0) {
      setMessage(`已拖拽选择 ${droppedFiles.length} 个文件`)
      setMessageType('info')
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
            <Link 
              to="/dashboard" 
              style={{ 
                textDecoration: 'none', 
                color: '#3b82f6',
                marginRight: '20px',
                fontSize: '14px',
                fontWeight: '500'
              }}
            >
              ← 返回控制台
            </Link>
            <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '600', color: '#1f2937' }}>
              📄 论文上传
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div style={{
        maxWidth: '800px',
        margin: '40px auto',
        padding: '0 20px'
      }}>
        
        {/* Upload Area */}
        <div 
          style={{
            backgroundColor: '#f9fafb',
            border: '2px dashed #d1d5db',
            borderRadius: '12px',
            padding: '60px 40px',
            textAlign: 'center',
            marginBottom: '30px',
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out'
          }}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <div style={{
            fontSize: '48px',
            marginBottom: '20px'
          }}>
            📁
          </div>
          <h3 style={{
            margin: '0 0 12px 0',
            fontSize: '20px',
            fontWeight: '600',
            color: '#1f2937'
          }}>
            点击选择文件或拖拽到此处
          </h3>
          <p style={{
            margin: '0 0 20px 0',
            fontSize: '16px',
            color: '#6b7280'
          }}>
            支持 PDF、Markdown (.md)、文本 (.txt) 格式
          </p>
          <p style={{
            margin: 0,
            fontSize: '14px',
            color: '#9ca3af'
          }}>
            单个文件最大 50MB，最多上传 10 个文件
          </p>
          
          <input
            id="file-input"
            type="file"
            multiple
            accept=".pdf,.md,.txt,.markdown"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>

        {/* Selected Files */}
        {files && files.length > 0 && (
          <div style={{
            backgroundColor: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <h4 style={{
              margin: '0 0 16px 0',
              fontSize: '16px',
              fontWeight: '600',
              color: '#1f2937'
            }}>
              已选择的文件 ({files.length})
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {Array.from(files).map((file, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  backgroundColor: '#f3f4f6',
                  borderRadius: '6px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <span style={{ marginRight: '8px' }}>
                      {file.name.endsWith('.pdf') ? '📄' : 
                       file.name.endsWith('.md') || file.name.endsWith('.markdown') ? '📝' : '📋'}
                    </span>
                    <span style={{ fontSize: '14px', color: '#374151' }}>
                      {file.name}
                    </span>
                  </div>
                  <span style={{
                    fontSize: '12px',
                    color: '#6b7280'
                  }}>
                    {(file.size / 1024 / 1024).toFixed(1)} MB
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Message */}
        {message && (
          <div style={{
            padding: '12px 16px',
            borderRadius: '8px',
            marginBottom: '20px',
            backgroundColor: messageType === 'success' ? '#d1fae5' : 
                           messageType === 'error' ? '#fee2e2' : '#dbeafe',
            color: messageType === 'success' ? '#065f46' : 
                   messageType === 'error' ? '#991b1b' : '#1e40af',
            border: `1px solid ${messageType === 'success' ? '#a7f3d0' : 
                                messageType === 'error' ? '#fecaca' : '#93c5fd'}`
          }}>
            {message}
          </div>
        )}

        {/* Upload Button */}
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <button
            onClick={handleUpload}
            disabled={uploading || !files || files.length === 0}
            style={{
              backgroundColor: uploading || !files || files.length === 0 ? '#d1d5db' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '12px 24px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: uploading || !files || files.length === 0 ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s ease-in-out',
              minWidth: '120px'
            }}
          >
            {uploading ? '上传中...' : '开始上传'}
          </button>
        </div>

        {/* Instructions */}
        <div style={{
          padding: '20px',
          backgroundColor: 'white',
          borderRadius: '8px',
          border: '1px solid #e5e7eb'
        }}>
          <h4 style={{
            margin: '0 0 16px 0',
            fontSize: '16px',
            fontWeight: '600',
            color: '#1f2937'
          }}>
            📋 使用说明
          </h4>
          <ul style={{
            margin: 0,
            paddingLeft: '20px',
            color: '#6b7280',
            lineHeight: '1.6'
          }}>
            <li>支持上传 PDF、Markdown 和文本格式的研究论文</li>
            <li>AI 将自动分析论文内容，提取关键信息和概念</li>
            <li>分析完成后，您可以查看分析结果和生成学习计划</li>
            <li>建议上传英文学术论文以获得最佳分析效果</li>
            <li>文件上传后将进入后台处理队列，处理时间取决于论文长度</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default SimpleUploadPage