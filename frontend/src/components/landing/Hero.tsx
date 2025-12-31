'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, Sparkles, Brain, Zap } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-animated overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 grid-pattern" />

      {/* Floating orbs */}
      <div className="aurora-glow w-96 h-96 bg-accent-primary/20 top-20 -left-48 animate-float" />
      <div className="aurora-glow w-80 h-80 bg-accent-secondary/20 bottom-20 -right-40 animate-float" style={{ animationDelay: '2s' }} />
      <div className="aurora-glow w-64 h-64 bg-accent-primary/10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse-slow" />

      {/* Noise overlay */}
      <div className="absolute inset-0 noise-overlay pointer-events-none" />

      {/* Main content */}
      <div className="container mx-auto px-6 relative z-10">
        <div className="max-w-5xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 mb-8 animate-slide-down">
            <Sparkles className="w-4 h-4 text-accent-primary" />
            <span className="text-sm text-text-secondary">Next-Gen Mind Mapping</span>
          </div>

          {/* Main heading */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold text-white mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Organize Your
            <br />
            <span className="gradient-text animate-gradient">Thoughts Naturally</span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl md:text-2xl text-text-secondary mb-12 max-w-3xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '0.2s' }}>
            A powerful blend of visual mind mapping and block-based note-taking.
            Transform the way you capture, connect, and create.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16 animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <Link href="/auth/signup" className="group relative px-8 py-4 bg-gradient-to-r from-accent-primary to-accent-secondary rounded-full font-semibold text-white transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-accent-primary/25">
              <span className="relative z-10 flex items-center gap-2">
                Get Started Free
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-accent-primary to-accent-secondary blur-xl opacity-50 group-hover:opacity-75 transition-opacity" />
            </Link>

            <Link href="/auth/login" className="glass-button group">
              <span className="relative z-10 flex items-center gap-2">
                <Zap className="w-5 h-5 text-accent-primary" />
                Sign In
              </span>
            </Link>
          </div>

          {/* Feature pills */}
          <div className="flex flex-wrap justify-center gap-3 animate-slide-up" style={{ animationDelay: '0.4s' }}>
            {[
              { icon: Brain, text: 'Visual Mind Mapping' },
              { icon: Sparkles, text: 'AI-Powered Insights' },
              { icon: Zap, text: 'Real-time Collaboration' },
            ].map((feature, index) => (
              <div
                key={index}
                className="glass-card px-4 py-2 flex items-center gap-2 glass-card-hover cursor-pointer"
              >
                <feature.icon className="w-4 h-4 text-accent-primary" />
                <span className="text-sm text-text-primary">{feature.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Hero visual - Glass card showcase */}
        <div className="mt-20 relative animate-scale-in" style={{ animationDelay: '0.5s' }}>
          <div className="glass-card p-8 max-w-4xl mx-auto glow-primary">
            <div className="grid grid-cols-3 gap-4">
              {[
                { title: 'Central Idea', color: 'from-accent-primary to-accent-secondary' },
                { title: 'Branch Out', color: 'from-accent-secondary to-accent-primary' },
                { title: 'Connect', color: 'from-accent-primary to-accent-secondary' },
              ].map((item, index) => (
                <div
                  key={index}
                  className="glass-card p-6 text-center glass-card-hover"
                >
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${item.color} mx-auto mb-3 flex items-center justify-center`}>
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-white font-medium mb-1">{item.title}</h3>
                  <p className="text-sm text-text-muted">Connect ideas</p>
                </div>
              ))}
            </div>

            {/* Connection lines visualization */}
            <div className="absolute inset-0 pointer-events-none">
              <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.3" />
                    <stop offset="100%" stopColor="#ec4899" stopOpacity="0.3" />
                  </linearGradient>
                </defs>
                <line x1="33%" y1="50%" x2="66%" y2="50%" stroke="url(#lineGradient)" strokeWidth="2" strokeDasharray="5,5" />
              </svg>
            </div>
          </div>

          {/* Glow effect under card */}
          <div className="absolute -inset-4 bg-gradient-to-r from-accent-primary/20 to-accent-secondary/20 blur-3xl -z-10 rounded-full" />
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/20 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white/40 rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  );
}
