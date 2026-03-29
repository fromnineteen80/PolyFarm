module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0a',
        surface: '#141414',
        card: '#1a1a1a',
        border: '#2a2a2a',
        profit: '#00c853',
        loss: '#ff1744',
        info: '#2979ff',
        bandA: '#ffd700',
        bandB: '#c0c0c0',
        bandC: '#cd7f32',
        paper: '#ff9800',
        live: '#00c853',
      },
      fontFamily: {
        mono: ['Menlo', 'Monaco', 'Consolas', 'monospace'],
      }
    }
  },
  plugins: []
}
