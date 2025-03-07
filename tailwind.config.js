/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}

//npx tailwindcss -i ./webapp/static/input.css -o ./webapp/static/output.css --watch
