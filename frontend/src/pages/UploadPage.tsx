import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, CheckCircle, AlertCircle, Clock } from 'lucide-react'
import toast from 'react-hot-toast'
import Card, { CardHeader, CardBody } from '../components/ui/Card'
import Button from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { uploadFile } from '../services/api'

interface UploadedFile {
  id: string
  file: File
  status: 'uploading' | 'uploaded' | 'processing' | 'completed' | 'error'
  progress: number
  paperId?: number
  error?: string
}

const UploadPage: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isUploading, setIsUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      status: 'uploading',
      progress: 0,
    }))

    setUploadedFiles((prev) => [...prev, ...newFiles])
    setIsUploading(true)

    // 处理每个文件的上传
    for (const uploadFile of newFiles) {
      try {
        await handleFileUpload(uploadFile)
      } catch (error) {
        console.error('Upload failed:', error)
      }
    }

    setIsUploading(false)
  }, [])

  const handleFileUpload = async (uploadFile: UploadedFile) => {
    try {
      // 模拟上传进度
      const progressInterval = setInterval(() => {
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === uploadFile.id
              ? { ...f, progress: Math.min(f.progress + 10, 90) }
              : f
          )
        )
      }, 200)

      // 实际上传文件
      const response = await uploadFile('/papers/upload', uploadFile.file, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === uploadFile.id
              ? { ...f, progress: percentCompleted }
              : f
          )
        )
      })

      clearInterval(progressInterval)

      // 上传完成，开始处理
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === uploadFile.id
            ? {
                ...f,
                status: 'processing',
                progress: 100,
                paperId: response.paper_id,
              }
            : f
        )
      )

      // 模拟处理过程
      setTimeout(() => {
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === uploadFile.id
              ? { ...f, status: 'completed' }
              : f
          )
        )
        toast.success(`${uploadFile.file.name} 处理完成！`)
      }, 3000)

    } catch (error: any) {
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === uploadFile.id
            ? {
                ...f,
                status: 'error',
                error: error.message || '上传失败',
              }
            : f
        )
      )
      toast.error(`${uploadFile.file.name} 上传失败`)
    }
  }

  const removeFile = (fileId: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== fileId))
  }

  const retryUpload = (fileId: string) => {
    const file = uploadedFiles.find((f) => f.id === fileId)
    if (file) {
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === fileId
            ? { ...f, status: 'uploading', progress: 0, error: undefined }
            : f
        )
      )
      handleFileUpload(file)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/markdown': ['.md'],
      'text/plain': ['.txt'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    disabled: isUploading,
  })

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return <Clock className="h-5 w-5 text-blue-500" />
      case 'uploaded':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'processing':
        return <Clock className="h-5 w-5 text-yellow-500" />
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />
      default:
        return null
    }
  }

  const getStatusText = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return '上传中...'
      case 'uploaded':
        return '上传完成'
      case 'processing':
        return '分析中...'
      case 'completed':
        return '分析完成'
      case 'error':
        return '上传失败'
      default:
        return ''
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">论文上传</h1>
        <p className="mt-2 text-gray-600">
          上传PDF或Markdown格式的研究论文，AI将自动分析并提取关键信息
        </p>
      </div>

      {/* 上传区域 */}
      <Card>
        <CardHeader 
          title="上传文件" 
          description="支持PDF、Markdown和纯文本格式，最大文件大小50MB"
        />
        <CardBody>
          <div
            {...getRootProps()}
            className={`
              relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer
              ${isDragActive 
                ? 'border-primary-400 bg-primary-50' 
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }
              ${isUploading ? 'pointer-events-none opacity-50' : ''}
            `}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
                <Upload className="h-8 w-8 text-primary-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {isDragActive ? '松开鼠标即可上传' : '拖拽文件到此处或点击选择'}
                </h3>
                <p className="text-sm text-gray-500">
                  支持 PDF、MD、TXT 格式，最大文件大小 50MB
                </p>
              </div>
              <Button variant="outline" disabled={isUploading}>
                选择文件
              </Button>
            </div>
          </div>

          {/* 上传提示 */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2 text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>支持批量上传</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>自动AI分析</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span>生成知识图谱</span>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* 上传文件列表 */}
      {uploadedFiles.length > 0 && (
        <Card>
          <CardHeader 
            title={`上传文件列表 (${uploadedFiles.length})`}
            description="文件上传和处理状态"
          />
          <CardBody>
            <div className="space-y-4">
              {uploadedFiles.map((uploadedFile) => (
                <div
                  key={uploadedFile.id}
                  className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg"
                >
                  {/* 文件图标 */}
                  <div className="flex-shrink-0">
                    <FileText className="h-8 w-8 text-gray-400" />
                  </div>

                  {/* 文件信息 */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {uploadedFile.file.name}
                      </p>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(uploadedFile.status)}
                        <span className="text-sm text-gray-600">
                          {getStatusText(uploadedFile.status)}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <p className="text-sm text-gray-500">
                        {(uploadedFile.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                      {uploadedFile.status !== 'error' && (
                        <span className="text-sm text-gray-600">
                          {uploadedFile.progress}%
                        </span>
                      )}
                    </div>

                    {/* 进度条 */}
                    {(uploadedFile.status === 'uploading' || uploadedFile.status === 'processing') && (
                      <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            uploadedFile.status === 'processing'
                              ? 'bg-yellow-500 animate-pulse'
                              : 'bg-primary-600'
                          }`}
                          style={{ width: `${uploadedFile.progress}%` }}
                        />
                      </div>
                    )}

                    {/* 错误信息 */}
                    {uploadedFile.error && (
                      <p className="mt-1 text-sm text-red-600">
                        {uploadedFile.error}
                      </p>
                    )}
                  </div>

                  {/* 操作按钮 */}
                  <div className="flex-shrink-0 flex items-center space-x-2">
                    {uploadedFile.status === 'error' && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => retryUpload(uploadedFile.id)}
                      >
                        重试
                      </Button>
                    )}
                    <button
                      type="button"
                      onClick={() => removeFile(uploadedFile.id)}
                      className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* 使用说明 */}
      <Card>
        <CardHeader title="使用说明" />
        <CardBody>
          <div className="prose text-sm text-gray-600 max-w-none">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">支持的文件格式</h4>
                <ul className="space-y-1">
                  <li>• PDF格式：研究论文、技术文档</li>
                  <li>• Markdown格式：预处理的论文文本</li>
                  <li>• 纯文本格式：简单的文本文档</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">AI分析功能</h4>
                <ul className="space-y-1">
                  <li>• 自动提取论文结构和内容</li>
                  <li>• 识别关键概念和术语</li>
                  <li>• 分析论文难度和预估阅读时间</li>
                  <li>• 生成知识图谱和概念关系</li>
                </ul>
              </div>
            </div>
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">💡 优化建议</h4>
              <p className="text-blue-800">
                为获得最佳分析效果，建议上传完整的研究论文PDF文件，
                确保文件清晰可读，避免扫描版本或图片格式的文档。
              </p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}

export default UploadPage