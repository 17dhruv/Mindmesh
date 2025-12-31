'use client';

import React, { useState, useEffect } from 'react';
import {
  ArrowRight,
  Check,
  Zap,
  Lock,
  Sparkles,
  Users,
  Shield,
  type LucideIcon
} from 'lucide-react';

interface Testimonial {
  quote: string;
  author: string;
  role: string;
  avatar: string;
}

interface Plan {
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  icon: LucideIcon;
  popular?: boolean;
  gradient: string;
}

const testimonials: Testimonial[] = [
  {
    quote: 'Mindmesh completely transformed how I brainstorm. The visual connections help me see patterns I never noticed before.',
    author: 'Sarah Chen',
    role: 'Product Designer',
    avatar: 'SC'
  },
  {
    quote: 'Finally, a tool that combines the flexibility of mind maps with the structure of docs. Absolute game-changer.',
    author: 'Marcus Johnson',
    role: 'Startup Founder',
    avatar: 'MJ'
  },
  {
    quote: 'The AI features are incredible. It suggests connections I would have never thought of on my own.',
    author: 'Emily Rodriguez',
    role: 'Research Analyst',
    avatar: 'ER'
  }
];

const plans: Plan[] = [
  {
    name: 'Free',
    description: 'Perfect for getting started',
    price: '$0',
    period: 'forever',
    icon: Sparkles,
    gradient: 'from-violet-500 to-purple-500',
    features: [
      'Up to 3 mind maps',
      'Basic block editor',
      '10 AI queries/month',
      'Export to PNG',
      'Community support'
    ]
  },
  {
    name: 'Pro',
    description: 'For power users',
    price: '$12',
    period: '/month',
    icon: Zap,
    popular: true,
    gradient: 'from-fuchsia-500 to-pink-500',
    features: [
      'Unlimited mind maps',
      'Advanced block editor',
      'Unlimited AI queries',
      'Export to SVG, PDF',
      'Version history',
      'Priority support'
    ]
  },
  {
    name: 'Team',
    description: 'For collaborative teams',
    price: '$29',
    period: '/user/month',
    icon: Users,
    gradient: 'from-purple-500 to-violet-500',
    features: [
      'Everything in Pro',
      'Real-time collaboration',
      'Team workspaces',
      'Admin dashboard',
      'SSO & SAML',
      'Dedicated support'
    ]
  }
];

export function Demo() {
  const [activeTestimonial, setActiveTestimonial] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {/* Testimonials Section */}
      <section className="relative py-32 bg-dark-surface overflow-hidden">
        <div className="absolute inset-0 grid-pattern opacity-30" />
        <div className="aurora-glow w-[400px] h-[400px] bg-accent-primary/10 top-1/4 left-1/4" />

        <div className="container mx-auto px-6 relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 glass-card px-4 py-2 mb-6">
              <Sparkles className="w-4 h-4 text-accent-primary" />
              <span className="text-sm text-text-secondary">Loved by Creators</span>
            </div>

            <h2 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Join thousands of
              <span className="gradient-text"> creative thinkers</span>
            </h2>
          </div>

          {/* Testimonial cards */}
          <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className={`glass-card p-6 transition-all duration-500 ${
                  index === activeTestimonial ? 'scale-105 border-accent-primary/30' : 'opacity-60'
                }`}
                onMouseEnter={() => setActiveTestimonial(index)}
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${index === 0 ? 'from-violet-500 to-purple-500' : index === 1 ? 'from-fuchsia-500 to-pink-500' : 'from-purple-500 to-violet-500'} flex items-center justify-center text-white font-semibold`}>
                    {testimonial.avatar}
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{testimonial.author}</h4>
                    <p className="text-sm text-text-muted">{testimonial.role}</p>
                  </div>
                </div>

                <p className="text-text-secondary leading-relaxed">
                  &ldquo;{testimonial.quote}&rdquo;
                </p>

                {/* Stars */}
                <div className="flex gap-1 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-4 h-4 rounded-full bg-accent-primary/80" />
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Trust badges */}
          <div className="mt-16 flex flex-wrap justify-center items-center gap-8 text-text-muted">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-accent-primary" />
              <span className="text-sm">SOC 2 Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-5 h-5 text-accent-primary" />
              <span className="text-sm">End-to-end encrypted</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-accent-primary" />
              <span className="text-sm">10,000+ Users</span>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="relative py-32 bg-dark-bg overflow-hidden">
        <div className="absolute inset-0 grid-pattern opacity-50" />
        <div className="aurora-glow w-[500px] h-[500px] bg-accent-secondary/10 bottom-0 right-0" />

        <div className="container mx-auto px-6 relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 glass-card px-4 py-2 mb-6">
              <Zap className="w-4 h-4 text-accent-primary" />
              <span className="text-sm text-text-secondary">Simple Pricing</span>
            </div>

            <h2 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Choose your
              <span className="gradient-text"> perfect plan</span>
            </h2>
          </div>

          {/* Pricing cards */}
          <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {plans.map((plan, index) => {
              const Icon = plan.icon;
              return (
                <div
                  key={index}
                  className={`group relative ${plan.popular ? 'md:-translate-y-4' : ''}`}
                >
                  {/* Popular badge */}
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-gradient-to-r from-accent-primary to-accent-secondary rounded-full text-xs font-semibold text-white">
                      Most Popular
                    </div>
                  )}

                  {/* Glow effect */}
                  <div
                    className={`absolute -inset-1 bg-gradient-to-r ${plan.gradient} rounded-2xl blur-xl opacity-0 group-hover:opacity-20 transition-opacity duration-500 ${plan.popular ? 'opacity-20' : ''}`}
                  />

                  {/* Card */}
                  <div className={`relative glass-card p-8 h-full ${plan.popular ? 'border-accent-primary/30' : ''} glass-card-hover`}>
                    {/* Icon */}
                    <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${plan.gradient} flex items-center justify-center mb-6`}>
                      <Icon className="w-7 h-7 text-white" />
                    </div>

                    {/* Name & description */}
                    <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                    <p className="text-text-secondary mb-6">{plan.description}</p>

                    {/* Price */}
                    <div className="mb-6">
                      <div className="flex items-baseline gap-1">
                        <span className="text-4xl font-bold text-white">{plan.price}</span>
                        <span className="text-text-muted">{plan.period}</span>
                      </div>
                    </div>

                    {/* Features */}
                    <ul className="space-y-3 mb-8">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-start gap-3">
                          <Check className="w-5 h-5 text-accent-primary flex-shrink-0 mt-0.5" />
                          <span className="text-text-secondary text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA button */}
                    <button
                      className={`w-full py-3 rounded-xl font-semibold transition-all duration-300 ${
                        plan.popular
                          ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white hover:scale-105 hover:shadow-xl hover:shadow-accent-primary/25'
                          : 'glass-button text-white'
                      }`}
                    >
                      Get Started
                      <ArrowRight className="inline ml-2 w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative py-32 bg-dark-surface overflow-hidden">
        <div className="absolute inset-0 grid-pattern opacity-30" />

        {/* Animated gradient background */}
        <div className="absolute inset-0">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-accent-primary/20 via-accent-secondary/20 to-accent-primary/20 rounded-full blur-3xl animate-pulse-slow" />
        </div>

        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="glass-card p-12 md:p-16 glow-primary">
              <Sparkles className="w-12 h-12 text-accent-primary mx-auto mb-6" />

              <h2 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-6">
                Ready to organize your
                <span className="gradient-text"> thoughts?</span>
              </h2>

              <p className="text-lg text-text-secondary mb-10 max-w-2xl mx-auto">
                Start your journey to better thinking today. No credit card required.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="group relative px-10 py-4 bg-gradient-to-r from-accent-primary to-accent-secondary rounded-full font-semibold text-white transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-accent-primary/25">
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    Start Writing Free
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </span>
                  <div className="absolute inset-0 rounded-full bg-gradient-to-r from-accent-primary to-accent-secondary blur-xl opacity-50 group-hover:opacity-75 transition-opacity" />
                </button>

                <button className="glass-button">
                  Schedule Demo
                </button>
              </div>

              {/* Trust indicators */}
              <div className="mt-10 flex flex-wrap justify-center items-center gap-6 text-sm text-text-muted">
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-accent-primary" />
                  <span>Free forever plan</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-accent-primary" />
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-accent-primary" />
                  <span>Cancel anytime</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
