import { supabase } from './supabase'

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Types for API responses
export interface User {
  id: string
  email: string
  full_name: string
  created_at: string
}

export interface Plan {
  id: string
  user_id: string
  title: string
  description: string
  status: 'draft' | 'accepted' | 'archived' | 'active'
  original_thought?: string
  ai_generated_data?: string
  ai_metadata?: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: string
  plan_id: string
  title: string
  description: string
  priority: number
  status: 'pending' | 'in_progress' | 'completed'
  ai_category?: string
  ai_priority_score?: number
  ai_reasoning?: string
  created_at: string
  updated_at: string
}

// API Client class
export class ApiClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async getAuthHeaders(): Promise<Record<string, string>> {
    const { data: { session } } = await supabase.auth.getSession()
    return {
      'Content-Type': 'application/json',
      ...(session?.access_token && { Authorization: `Bearer ${session.access_token}` }),
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.message || `HTTP ${response.status}: ${response.statusText}`)
    }
    return response.json()
  }

  // Plans API
  async getPlans(): Promise<Plan[]> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/plans`, { headers })
    return this.handleResponse<Plan[]>(response)
  }

  async getPlan(planId: string): Promise<Plan> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/plans/${planId}`, { headers })
    return this.handleResponse<Plan>(response)
  }

  async createPlan(data: { title: string; description: string; original_thought?: string }): Promise<Plan> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/plans`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    })
    return this.handleResponse<Plan>(response)
  }

  async updatePlan(planId: string, data: Partial<Plan>): Promise<Plan> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/plans/${planId}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
    })
    return this.handleResponse<Plan>(response)
  }

  async deletePlan(planId: string): Promise<void> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/plans/${planId}`, {
      method: 'DELETE',
      headers,
    })
    await this.handleResponse<void>(response)
  }

  // Tasks API
  async getTasks(planId?: string): Promise<Task[]> {
    const headers = await this.getAuthHeaders()
    const url = planId ? `${this.baseURL}/api/tasks?plan_id=${planId}` : `${this.baseURL}/api/tasks`
    const response = await fetch(url, { headers })
    return this.handleResponse<Task[]>(response)
  }

  async getTask(taskId: string): Promise<Task> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/tasks/${taskId}`, { headers })
    return this.handleResponse<Task>(response)
  }

  async createTask(data: { plan_id: string; title: string; description: string; priority: number }): Promise<Task> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/tasks`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    })
    return this.handleResponse<Task>(response)
  }

  async updateTask(taskId: string, data: Partial<Task>): Promise<Task> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
    })
    return this.handleResponse<Task>(response)
  }

  async deleteTask(taskId: string): Promise<void> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers,
    })
    await this.handleResponse<void>(response)
  }

  // AI API
  async generateDashboard(planId: string): Promise<Record<string, unknown>> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/ai/generate-dashboard?plan_id=${planId}`, {
      method: 'POST',
      headers,
    })
    return this.handleResponse<Record<string, unknown>>(response)
  }

  async approveDashboard(data: { approved: boolean; feedback?: string }): Promise<Record<string, unknown>> {
    const headers = await this.getAuthHeaders()
    const response = await fetch(`${this.baseURL}/api/ai/approve-dashboard`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    })
    return this.handleResponse<Record<string, unknown>>(response)
  }

  async getInteractionHistory(planId?: string): Promise<Record<string, unknown>[]> {
    const headers = await this.getAuthHeaders()
    const url = planId ? `${this.baseURL}/api/ai/interaction-history?plan_id=${planId}` : `${this.baseURL}/api/ai/interaction-history`
    const response = await fetch(url, { headers })
    return this.handleResponse<Record<string, unknown>[]>(response)
  }
}

// Create singleton instance
export const apiClient = new ApiClient()