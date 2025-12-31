'use client';

import React, { useState } from 'react';
import {
  Blocks,
  Network,
  Sparkles,
  ArrowUpRight,
  ChevronRight,
  Check,
  type LucideIcon
} from 'lucide-react';

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
  gradient: string;
  stats: string;
  items: string[];
}

const features: Feature[] = [
  {
    icon: Blocks,
    title: 'Block-Based Editor',
    description: 'Create content with Notion-like blocks. Type "/" to access text, headings, tasks, code, and more.',
    gradient: 'from-violet-500 to-purple-500',
    stats: '50+ Blocks',
    items: ['Rich Text', 'Code Blocks', 'Embeds', 'Tasks', 'Databases'],
  },
  {
    icon: Network,
    title: 'Visual Mind Mapping',
    description: 'Connect your thoughts visually with drag-and-drop nodes. See relationships between ideas.',
    gradient: 'from-fuchsia-500 to-pink-500',
    stats: 'Unlimited Nodes',
    items: ['Drag & Drop', 'Auto Layout', 'Color Coding', 'Export SVG', 'Share'],
  },
  {
    icon: Sparkles,
    title: 'AI-Powered Insights',
    description: 'Let AI help you brainstorm, organize, and discover connections you might have missed.',
    gradient: 'from-purple-500 to-violet-500',
    stats: 'GPT-4 Powered',
    items: ['Auto-Summarize', 'Brainstorm', 'Smart Connect', 'Suggestions'],
  },
];

export function Features() {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <section className="relative py-32 bg-dark-bg overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 grid-pattern opacity-50" />
      <div className="aurora-glow w-[600px] h-[600px] bg-accent-primary/10 top-0 right-0" />
      <div className="aurora-glow w-[500px] h-[500px] bg-accent-secondary/10 bottom-0 left-0" />

      <div className="container mx-auto px-6 relative z-10">
        {/* Section header */}
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 mb-6">
            <Sparkles className="w-4 h-4 text-accent-primary" />
            <span className="text-sm text-text-secondary">Powerful Features</span>
          </div>

          <h2 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-6">
            Everything You Need to
            <span className="gradient-text"> Create & Connect</span>
          </h2>

          <p className="text-lg text-text-secondary max-w-2xl mx-auto">
            Thoughtfully designed features that help you organize your thoughts
            without overwhelming you.
          </p>
        </div>

        {/* Feature cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="group relative"
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                {/* Glow effect */}
                <div
                  className={`absolute -inset-1 bg-gradient-to-r ${feature.gradient} rounded-2xl blur-xl opacity-0 group-hover:opacity-30 transition-opacity duration-500`}
                />

                {/* Card */}
                <div className="relative glass-card p-8 h-full glass-card-hover">
                  {/* Icon */}
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>

                  {/* Title */}
                  <h3 className="text-2xl font-bold text-white mb-3">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="text-text-secondary mb-6 leading-relaxed">
                    {feature.description}
                  </p>

                  {/* Stats badge */}
                  <div className="inline-flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-full mb-6">
                    <Check className="w-3.5 h-3.5 text-accent-primary" />
                    <span className="text-sm text-text-primary">{feature.stats}</span>
                  </div>

                  {/* Feature list */}
                  <ul className="space-y-2">
                    {feature.items.map((item, i) => (
                      <li
                        key={i}
                        className="flex items-center gap-2 text-sm text-text-muted group-hover:text-text-secondary transition-colors"
                      >
                        <ChevronRight className={`w-4 h-4 flex-shrink-0 ${hoveredIndex === index ? 'text-accent-primary translate-x-1' : 'text-text-muted'} transition-all duration-300`} />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>

                  {/* Arrow indicator */}
                  <div className="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/5 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <ArrowUpRight className="w-5 h-5 text-accent-primary" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="mt-20 text-center">
          <div className="glass-card max-w-2xl mx-auto p-8 glow-primary">
            <h3 className="text-2xl font-bold text-white mb-3">
              Ready to transform your workflow?
            </h3>
            <p className="text-text-secondary mb-6">
              Join thousands of users who are already organizing their thoughts better.
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-accent-primary to-accent-secondary rounded-full font-semibold text-white transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-accent-primary/25">
              Get Started Free
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
