/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./public/**/*.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'cass': {
          primary: '#6366f1',    // Indigo
          secondary: '#8b5cf6',  // Violet
          dark: '#1e1e2e',       // Dark background
          darker: '#181825',     // Darker background
          light: '#f8fafc',      // Light background
          accent: '#22d3ee',     // Cyan accent
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'typing': 'typing 1.5s ease-in-out infinite',
      },
      keyframes: {
        typing: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        }
      }
    },
  },
  plugins: [],
}
