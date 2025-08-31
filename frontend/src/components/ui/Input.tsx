import React, { forwardRef } from 'react'
import { clsx } from 'clsx'
import { Eye, EyeOff } from 'lucide-react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({
    label,
    error,
    hint,
    leftIcon,
    rightIcon,
    fullWidth = false,
    className,
    type = 'text',
    ...props
  }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false)
    const isPassword = type === 'password'
    const inputType = isPassword && showPassword ? 'text' : type

    const inputClasses = clsx(
      'block w-full rounded-lg border px-3 py-2 text-sm shadow-sm transition-colors',
      'placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0',
      leftIcon && 'pl-10',
      (rightIcon || isPassword) && 'pr-10',
      error
        ? 'border-red-500 text-red-900 focus:border-red-500 focus:ring-red-500'
        : 'border-gray-300 text-gray-900 focus:border-primary-500 focus:ring-primary-500',
      props.disabled && 'bg-gray-50 text-gray-500 cursor-not-allowed',
      fullWidth ? 'w-full' : '',
      className
    )

    const containerClasses = clsx(
      'relative',
      fullWidth ? 'w-full' : ''
    )

    return (
      <div className={containerClasses}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        <div className="relative">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span className="text-gray-400 text-sm">
                {leftIcon}
              </span>
            </div>
          )}
          
          <input
            ref={ref}
            type={inputType}
            className={inputClasses}
            {...props}
          />
          
          {isPassword ? (
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          ) : rightIcon ? (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <span className="text-gray-400 text-sm">
                {rightIcon}
              </span>
            </div>
          ) : null}
        </div>
        
        {(error || hint) && (
          <div className="mt-2">
            {error && (
              <p className="text-sm text-red-600">
                {error}
              </p>
            )}
            {hint && !error && (
              <p className="text-sm text-gray-500">
                {hint}
              </p>
            )}
          </div>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export default Input