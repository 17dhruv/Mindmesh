import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'glass' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
  ...props
}: ButtonProps) {
  const baseStyles = 'relative inline-flex items-center justify-center rounded-full font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-accent-primary/50 disabled:opacity-50 disabled:pointer-events-none overflow-hidden';

  const variants = {
    primary: 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white hover:scale-105 hover:shadow-xl hover:shadow-accent-primary/25 border border-transparent',
    secondary: 'bg-white/5 text-white hover:bg-white/10 border border-white/10 hover:border-white/20',
    glass: 'bg-white/5 backdrop-blur-xl text-white hover:bg-white/10 border border-white/10 hover:border-accent-primary/50 hover:shadow-lg hover:shadow-accent-primary/20',
    ghost: 'bg-transparent text-white hover:bg-white/5 border border-transparent',
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <button
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      <span className="relative z-10 flex items-center gap-2">{children}</span>
      {variant === 'primary' && (
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-accent-primary to-accent-secondary blur-xl opacity-50 transition-opacity" />
      )}
    </button>
  );
}
