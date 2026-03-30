// Reusable Loading component with spinner variants
// FEATURE: UI Components

import React from 'react';
import { cn } from '../../../utils/helpers';

type LoadingSize = 'sm' | 'md' | 'lg' | 'xl';
type LoadingVariant = 'spinner' | 'dots' | 'pulse';

interface LoadingProps {
  size?: LoadingSize;
  variant?: LoadingVariant;
  text?: string;
  fullScreen?: boolean;
  className?: string;
}

const sizeClasses: Record<LoadingSize, string> = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
  xl: 'h-16 w-16',
};

const Spinner: React.FC<{ size: LoadingSize; className?: string }> = ({ size, className }) => (
  <svg
    className={cn('animate-spin', sizeClasses[size], className)}
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle
      className="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="4"
    />
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    />
  </svg>
);

const Dots: React.FC<{ size: LoadingSize; className?: string }> = ({ size, className }) => {
  const dotSize = size === 'sm' ? 'h-2 w-2' : size === 'md' ? 'h-3 w-3' : size === 'lg' ? 'h-4 w-4' : 'h-5 w-5';
  
  return (
    <div className={cn('flex gap-1', className)}>
      <div className={cn(dotSize, 'bg-current rounded-full animate-bounce')} style={{ animationDelay: '0ms' }} />
      <div className={cn(dotSize, 'bg-current rounded-full animate-bounce')} style={{ animationDelay: '150ms' }} />
      <div className={cn(dotSize, 'bg-current rounded-full animate-bounce')} style={{ animationDelay: '300ms' }} />
    </div>
  );
};

const Pulse: React.FC<{ size: LoadingSize; className?: string }> = ({ size, className }) => (
  <div className={cn('rounded-full bg-current animate-pulse', sizeClasses[size], className)} />
);

export const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  variant = 'spinner',
  text,
  fullScreen = false,
  className,
}) => {
  const LoadingComponent = variant === 'spinner' ? Spinner : variant === 'dots' ? Dots : Pulse;

  const content = (
    <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
      <LoadingComponent size={size} className="text-blue-600 dark:text-blue-400" />
      {text && (
        <p className="text-sm text-gray-600 dark:text-gray-400 animate-pulse">
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        {content}
      </div>
    );
  }

  return content;
};
