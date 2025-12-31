import React from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({
  label,
  error,
  className,
  ...props
}: InputProps) {
  const id = props.id || label?.toLowerCase().replace(/\s/g, '-');

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={id}
          className="block text-sm font-medium text-gray-300 mb-2"
        >
          {label}
        </label>
      )}
      <input
        id={id}
        className={cn(
          'w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10',
          'text-white placeholder-gray-500',
          'focus:outline-none focus:ring-2 focus:ring-accent-primary/50 focus:border-accent-primary/50',
          'transition-all duration-200',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          error && 'border-red-500/50 focus:ring-red-500/50 focus:border-red-500/50',
          className
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
}
