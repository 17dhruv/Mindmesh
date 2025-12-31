import { create } from 'zustand'

interface UIState {
  // Mobile menu
  isMobileMenuOpen: boolean
  toggleMobileMenu: () => void
  closeMobileMenu: () => void
  openMobileMenu: () => void

  // Modals
  isCreatePlanModalOpen: boolean
  isAuthModalOpen: boolean
  isAuthModalMode: 'signin' | 'signup'

  openCreatePlanModal: () => void
  closeCreatePlanModal: () => void
  openAuthModal: (mode: 'signin' | 'signup') => void
  closeAuthModal: () => void

  // Notifications
  notifications: Array<{ id: string; message: string; type: 'success' | 'error' | 'info'; duration?: number }>
  addNotification: (message: string, type: 'success' | 'error' | 'info', duration?: number) => void
  removeNotification: (id: string) => void
  clearNotifications: () => void

  // Loading states
  isLoading: boolean
  setLoading: (loading: boolean) => void

  // Theme
  isDarkMode: boolean
  toggleTheme: () => void
}

export const useUIStore = create<UIState>((set, get) => ({
  // Mobile menu
  isMobileMenuOpen: false,
  toggleMobileMenu: () => set((state) => ({ isMobileMenuOpen: !state.isMobileMenuOpen })),
  closeMobileMenu: () => set({ isMobileMenuOpen: false }),
  openMobileMenu: () => set({ isMobileMenuOpen: true }),

  // Modals
  isCreatePlanModalOpen: false,
  isAuthModalOpen: false,
  isAuthModalMode: 'signin',

  openCreatePlanModal: () => set({ isCreatePlanModalOpen: true }),
  closeCreatePlanModal: () => set({ isCreatePlanModalOpen: false }),
  openAuthModal: (mode) => set({ isAuthModalOpen: true, isAuthModalMode: mode }),
  closeAuthModal: () => set({ isAuthModalOpen: false }),

  // Notifications
  notifications: [],
  addNotification: (message, type, duration = 5000) => {
    const id = Math.random().toString(36).substr(2, 9)
    const notification = { id, message, type, duration }

    set((state) => ({
      notifications: [...state.notifications, notification],
    }))

    // Auto-remove notification after duration
    if (duration > 0) {
      setTimeout(() => {
        get().removeNotification(id)
      }, duration)
    }
  },
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
  clearNotifications: () => set({ notifications: [] }),

  // Loading
  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),

  // Theme
  isDarkMode: false,
  toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
}))