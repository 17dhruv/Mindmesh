'use client'

import React from 'react'
import { Task } from '@/types'

export interface TaskWithStatus {
  title: string
  description: string
  priority: number
  reasoning: string
}

export interface CategoryData {
  name: string
  description: string
  icon: string
  color: string
  tasks: {
    todo: TaskWithStatus[]
    doing: TaskWithStatus[]
    upcoming: TaskWithStatus[]
  }
}

interface CategoryThreeRowProps {
  category: CategoryData
}

const colorStyles = {
  blue: {
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/20',
    text: 'text-blue-400',
    accent: 'bg-blue-500/20'
  },
  green: {
    bg: 'bg-green-500/10',
    border: 'border-green-500/20',
    text: 'text-green-400',
    accent: 'bg-green-500/20'
  },
  purple: {
    bg: 'bg-purple-500/10',
    border: 'border-purple-500/20',
    text: 'text-purple-400',
    accent: 'bg-purple-500/20'
  },
  orange: {
    bg: 'bg-orange-500/10',
    border: 'border-orange-500/20',
    text: 'text-orange-400',
    accent: 'bg-orange-500/20'
  },
  red: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/20',
    text: 'text-red-400',
    accent: 'bg-red-500/20'
  },
  yellow: {
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/20',
    text: 'text-yellow-400',
    accent: 'bg-yellow-500/20'
  },
  pink: {
    bg: 'bg-pink-500/10',
    border: 'border-pink-500/20',
    text: 'text-pink-400',
    accent: 'bg-pink-500/20'
  },
  gray: {
    bg: 'bg-gray-500/10',
    border: 'border-gray-500/20',
    text: 'text-gray-400',
    accent: 'bg-gray-500/20'
  }
}

const statusConfig = {
  todo: {
    label: 'TO DO',
    icon: '📋',
    bgColor: 'bg-gray-500/5',
    borderColor: 'border-gray-500/10'
  },
  doing: {
    label: 'IN PROGRESS',
    icon: '🚀',
    bgColor: 'bg-yellow-500/5',
    borderColor: 'border-yellow-500/10'
  },
  upcoming: {
    label: 'UPCOMING',
    icon: '🔜',
    bgColor: 'bg-green-500/5',
    borderColor: 'border-green-500/10'
  }
}

const priorityColors = {
  high: 'text-red-400',
  medium: 'text-yellow-400',
  low: 'text-green-400'
}

function getPriorityColor(priority: number): string {
  if (priority >= 8) return priorityColors.high
  if (priority >= 5) return priorityColors.medium
  return priorityColors.low
}

function getStatusColor(status: string): string {
  switch (status) {
    case 'todo': return 'bg-red-500/20'
    case 'doing': return 'bg-yellow-500/20'
    case 'upcoming': return 'bg-green-500/20'
    default: return 'bg-gray-500/20'
  }
}

export function CategoryThreeRow({ category }: CategoryThreeRowProps) {
  const styles = colorStyles[category.color as keyof typeof colorStyles] || colorStyles.blue
  const todoCount = category.tasks.todo.length
  const doingCount = category.tasks.doing.length
  const upcomingCount = category.tasks.upcoming.length

  return (
    <div className={`glass-card rounded-xl border ${styles.border} overflow-hidden mb-6`}>
      {/* Category Header */}
      <div className={`p-4 border-b border-white/10 ${styles.bg}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{category.icon}</span>
            <div>
              <h3 className={`text-lg font-semibold ${styles.text}`}>{category.name}</h3>
              <p className="text-sm text-gray-400">{category.description}</p>
            </div>
          </div>
          <button className={`px-3 py-1.5 rounded-lg ${styles.accent} ${styles.text} text-sm font-medium hover:opacity-80 transition-opacity`}>
            + Add Task
          </button>
        </div>
      </div>

      {/* TODO Row */}
      <div className={`border-b border-white/10 ${statusConfig.todo.bgColor}`}>
        <div className={`px-4 py-2 flex items-center justify-between ${statusConfig.todo.borderColor} border-b`}>
          <div className="flex items-center gap-2">
            <span>{statusConfig.todo.icon}</span>
            <span className="text-sm font-medium text-gray-300">{statusConfig.todo.label}</span>
          </div>
          <span className="text-xs text-gray-500">{todoCount} task{todoCount !== 1 ? 's' : ''}</span>
        </div>
        <div className="p-3 space-y-2">
          {category.tasks.todo.map((task, idx) => (
            <TaskCard key={`todo-${idx}`} task={task} status="todo" />
          ))}
          {todoCount === 0 && (
            <div className="text-center py-4 text-gray-500 text-sm">No tasks yet</div>
          )}
        </div>
      </div>

      {/* DOING Row */}
      <div className={`border-b border-white/10 ${statusConfig.doing.bgColor}`}>
        <div className={`px-4 py-2 flex items-center justify-between ${statusConfig.doing.borderColor} border-b`}>
          <div className="flex items-center gap-2">
            <span>{statusConfig.doing.icon}</span>
            <span className="text-sm font-medium text-gray-300">{statusConfig.doing.label}</span>
          </div>
          <span className="text-xs text-gray-500">{doingCount} task{doingCount !== 1 ? 's' : ''}</span>
        </div>
        <div className="p-3 space-y-2">
          {category.tasks.doing.map((task, idx) => (
            <TaskCard key={`doing-${idx}`} task={task} status="doing" />
          ))}
          {doingCount === 0 && (
            <div className="text-center py-4 text-gray-500 text-sm">No tasks in progress</div>
          )}
        </div>
      </div>

      {/* UPCOMING Row */}
      <div className={`${statusConfig.upcoming.bgColor}`}>
        <div className={`px-4 py-2 flex items-center justify-between ${statusConfig.upcoming.borderColor} border-b`}>
          <div className="flex items-center gap-2">
            <span>{statusConfig.upcoming.icon}</span>
            <span className="text-sm font-medium text-gray-300">{statusConfig.upcoming.label}</span>
          </div>
          <span className="text-xs text-gray-500">{upcomingCount} task{upcomingCount !== 1 ? 's' : ''}</span>
        </div>
        <div className="p-3 space-y-2">
          {category.tasks.upcoming.map((task, idx) => (
            <TaskCard key={`upcoming-${idx}`} task={task} status="upcoming" />
          ))}
          {upcomingCount === 0 && (
            <div className="text-center py-4 text-gray-500 text-sm">No upcoming tasks</div>
          )}
        </div>
      </div>
    </div>
  )
}

interface TaskCardProps {
  task: TaskWithStatus
  status: string
}

function TaskCard({ task, status }: TaskCardProps) {
  const priorityColor = getPriorityColor(task.priority)
  const statusColor = getStatusColor(status)

  return (
    <div className="glass-card rounded-lg p-3 hover:bg-white/5 transition-colors cursor-pointer group">
      <div className="flex items-start gap-3">
        {/* Status indicator */}
        <div className={`w-2 h-2 rounded-full ${statusColor} mt-2 flex-shrink-0`} />

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h4 className="text-sm font-medium text-gray-200 group-hover:text-white transition-colors">
              {task.title}
            </h4>
            <div className={`text-xs font-semibold ${priorityColor} flex-shrink-0`}>
              P{task.priority}
            </div>
          </div>

          {task.description && (
            <p className="text-xs text-gray-400 mt-1 line-clamp-2">{task.description}</p>
          )}

          {task.reasoning && (
            <div className="mt-2 flex items-start gap-1">
              <svg className="w-3 h-3 text-gray-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-xs text-gray-500 line-clamp-1">{task.reasoning}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
