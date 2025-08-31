import React from 'react'
import { clsx } from 'clsx'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
}

const variantClasses = {
  default: 'bg-white border border-gray-200 shadow-sm',
  elevated: 'bg-white shadow-md border border-gray-100',
  outlined: 'bg-white border-2 border-gray-200',
}

const paddingClasses = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
}

const Card: React.FC<CardProps> = ({
  variant = 'default',
  padding = 'md',
  hoverable = false,
  className,
  children,
  ...props
}) => {
  const classes = clsx(
    'rounded-xl transition-all duration-200',
    variantClasses[variant],
    paddingClasses[padding],
    hoverable && 'hover:shadow-lg hover:border-gray-300 cursor-pointer',
    className
  )

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  )
}

// Card 子组件
interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string
  description?: string
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  title,
  description,
  className,
  children,
  ...props
}) => {
  return (
    <div className={clsx('pb-4 mb-4 border-b border-gray-200', className)} {...props}>
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
      {children}
    </div>
  )
}

interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardBody: React.FC<CardBodyProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={clsx('flex-1', className)} {...props}>
      {children}
    </div>
  )
}

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardFooter: React.FC<CardFooterProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={clsx('pt-4 mt-4 border-t border-gray-200', className)} {...props}>
      {children}
    </div>
  )
}

export default Card