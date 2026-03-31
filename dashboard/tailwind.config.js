module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#faf9f7',
        surface: '#f5f4f2',
        card: '#ffffff',
        border: '#e5e7eb',
        profit: '#16a34a',
        loss: '#dc2626',
        info: '#2563eb',
        bandA: '#ca8a04',
        bandB: '#6b7280',
        bandC: '#92400e',
        paper: '#ca8a04',
        live: '#16a34a',
      },
      fontFamily: {
        sans: ['Raleway', 'sans-serif'],
        serif: ['Georgia', 'serif'],
      }
    }
  },
  plugins: []
}
