/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
         'main': "'Montserrat', sans-serif"
      },
      animation: {
         'flash-mess': 'show_flash_mess 7s linear',
         'appear': 'appear 0.7s linear'
      },
      keyframes: {
         show_flash_mess: {
            '0%, 100%': { transform: 'translateY(200px)' },
            '10%, 90%': { transform: 'translateY(0)' }
         },
         appear: {
            '0%': { opacity: '0', transform: 'translateY(25px)' },
            '100%': { opacity: '1', transform: 'translateY(0)' }
         }
      },
      boxShadow: {
         'box-hover': '0 0 30px 0px #083344'
      }
    },
  },
  plugins: [],
}

