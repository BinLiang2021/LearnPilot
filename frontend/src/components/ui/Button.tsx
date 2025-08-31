import React from 'react'
import { Loader2 } from 'lucide-react'
import { clsx } from 'clsx'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  fullWidth?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
}

const variantClasses = {
  primary: 'bg-primary-600 hover:bg-primary-700 focus:ring-primary-500 text-white shadow-sm',
  secondary: 'bg-gray-600 hover:bg-gray-700 focus:ring-gray-500 text-white shadow-sm',
  outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500 bg-transparent',
  ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500 bg-transparent',
  danger: 'bg-red-600 hover:bg-red-700 focus:ring-red-500 text-white shadow-sm',
}

const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm font-medium',
  md: 'px-4 py-2 text-sm font-medium',
  lg: 'px-6 py-3 text-base font-medium',
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  fullWidth = false,
  icon,
  iconPosition = 'left',
  children,
  className,
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'
  
  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    fullWidth && 'w-full',
    className
  )

  const isDisabled = disabled || loading

  const renderIcon = () => {
    if (loading) {
      return <Loader2 className="w-4 h-4 animate-spin" />
    }
    return icon
  }

  const iconElement = renderIcon()

  return (
    <button
      className={classes}
      disabled={isDisabled}
      {...props}
    >
      {iconElement && iconPosition === 'left' && (
        <span className={clsx('flex items-center', children && 'mr-2')}>
          {iconElement}
        </span>
      )}
      {children}
      {iconElement && iconPosition === 'right' && (
        <span className={clsx('flex items-center', children && 'ml-2')}>
          {iconElement}
        </span>
      )}
    </button>
  )
}

export default Button