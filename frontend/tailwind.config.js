/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.8s ease-out',
        'slide-up': 'slideUp 0.6s ease-out',
        'float': 'float 10s ease-in-out infinite',
        'glow': 'glow 0.8s ease-out',
      },
      colors: {
        // Light theme colors
        'light-bg': '#F4F2F8',
        'light-hero': '#E9E6F4',
        'light-primary': '#1E1B2E',
        'light-secondary': '#6B63A8',
        'light-body': '#4B5563',
        'light-muted': '#6B7280',
        'light-primary-btn': '#6D5DD3',
        'light-primary-btn-hover': '#5B4BC4',
        'light-secondary-btn': '#E5E7EB',
        'light-secondary-btn-hover': '#D1D5DB',
        'light-card': '#FFFFFF',
        'light-card-border': '#E5E7EB',
        'light-error-bg': '#FEE2E2',
        'light-error-text': '#991B1B',
        
        // Dark theme colors
        'dark-bg': '#0F172A',
        'dark-surface': '#1E293B',
        'dark-hero': '#1E1B3A',
        'dark-primary': '#F8FAFC',
        'dark-secondary': '#A5B4FC',
        'dark-body': '#CBD5E1',
        'dark-muted': '#94A3B8',
        'dark-primary-btn': '#7C6FF0',
        'dark-primary-btn-hover': '#6D5DD3',
        'dark-secondary-btn': '#334155',
        'dark-secondary-btn-hover': '#475569',
        'dark-card': '#1E293B',
        'dark-card-border': '#334155',
        'dark-error-bg': '#7F1D1D',
        'dark-error-text': '#FECACA',
      },
    },
  },
  plugins: [],
}
