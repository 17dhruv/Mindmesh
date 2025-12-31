import React from 'react';
import { cn } from '@/lib/utils';

interface PaperCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'sketch' | 'lined';
  texture?: 'subtle' | 'medium' | 'strong';
}

export function PaperCard({
  children,
  variant = 'default',
  texture = 'subtle',
  className,
  ...props
}: PaperCardProps) {
  const baseStyles = 'relative bg-paper-white rounded-xl shadow-paper border transition-all duration-200 hover:shadow-paper-lg';

  const variants = {
    default: 'border-ink-black/20',
    sketch: 'border-2 border-dashed border-ink-black/40',
    lined: 'border-ink-black/10'
  };

  const textureStyles = {
    subtle: 'bg-paper-texture opacity-10',
    medium: 'bg-paper-texture opacity-20',
    strong: 'bg-paper-texture opacity-30'
  };

  return (
    <div
      className={cn(
        baseStyles,
        variants[variant],
        className
      )}
      {...props}
    >
      {/* Paper texture overlay */}
      <div className={cn('absolute inset-0 rounded-xl pointer-events-none', textureStyles[texture])} />

      {/* Subtle corner accent for sketch variant */}
      {variant === 'sketch' && (
        <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-ink-black/30 rounded-tr-sm" />
      )}

      {/* Content */}
      <div className="relative z-10 p-6">
        {children}
      </div>

      {/* Subtle shadow effect */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-transparent to-black/5 pointer-events-none" />
    </div>
  );
}