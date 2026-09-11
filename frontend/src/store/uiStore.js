import { create } from 'zustand'

export const useUiStore = create((set) => ({
  accessToken: null,
  sidebarCollapsed: false,
  setAccessToken: (accessToken) => set({ accessToken }),
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
}))
