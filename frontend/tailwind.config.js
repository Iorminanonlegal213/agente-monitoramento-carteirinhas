/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#e6f7f5',
          100: '#b3e8e1',
          200: '#80d9cd',
          300: '#4dcab9',
          400: '#1abba5',
          500: '#028090',
          600: '#026d7a',
          700: '#015a64',
          800: '#01474e',
          900: '#003438',
        },
      },
    },
  },
  plugins: [],
};
