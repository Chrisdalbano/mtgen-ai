module.exports = {
  purge: ['./src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        'beleren': ['"Cinzel"', 'serif'],
        'matrix': ['"Bad Script"', 'cursive'],
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}