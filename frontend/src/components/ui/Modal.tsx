import React, { useEffect } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'
import { clsx } from 'clsx'
import Button from './Button'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  description?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  closable?: boolean
  maskClosable?: boolean
  children: React.ReactNode
}

const sizeClasses = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
  full: 'max-w-7xl mx-4',
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  description,
  size = 'md',
  closable = true,
  maskClosable = true,
  children,
}) => {
  // 处理 ESC 键关闭
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && closable) {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, closable, onClose])

  if (!isOpen) return null

  const handleMaskClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget && maskClosable) {
      onClose()
    }
  }

  const modalContent = (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 遮罩层 */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm transition-opacity"
        onClick={handleMaskClick}
      />
      
      {/* 模态框内容 */}
      <div
        className={clsx(
          'relative bg-white rounded-xl shadow-xl transform transition-all',
          'w-full m-4 max-h-[90vh] flex flex-col',
          sizeClasses[size]
        )}
      >
        {/* 头部 */}
        {(title || description || closable) && (
          <div className="flex items-start justify-between p-6 border-b border-gray-200">
            <div className="flex-1 min-w-0">
              {title && (
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {title}
                </h3>
              )}
              {description && (
                <p className="text-sm text-gray-600">
                  {description}
                </p>
              )}
            </div>
            
            {closable && (
              <button
                type="button"
                className="ml-4 text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600 transition-colors"
                onClick={onClose}
              >
                <X size={20} />
              </button>
            )}
          </div>
        )}
        
        {/* 主体内容 */}
        <div className="flex-1 overflow-y-auto p-6">
          {children}
        </div>
      </div>
    </div>
  )

  return createPortal(modalContent, document.body)
}

// Modal 确认对话框子组件
interface ConfirmModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  type?: 'info' | 'warning' | 'danger'
  loading?: boolean
}

export const ConfirmModal: React.FC<ConfirmModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = '确认',
  cancelText = '取消',
  type = 'info',
  loading = false,
}) => {
  const handleConfirm = () => {
    onConfirm()
  }

  const getButtonVariant = () => {
    switch (type) {
      case 'danger':
        return 'danger'
      case 'warning':
        return 'secondary'
      default:
        return 'primary'
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      size="sm"
      closable={!loading}
      maskClosable={!loading}
    >
      <div className="space-y-4">
        <p className="text-gray-700">
          {message}
        </p>
        
        <div className="flex justify-end space-x-3">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={loading}
          >
            {cancelText}
          </Button>
          <Button
            variant={getButtonVariant()}
            onClick={handleConfirm}
            loading={loading}
          >
            {confirmText}
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default Modal