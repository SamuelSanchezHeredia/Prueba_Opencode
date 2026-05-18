/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#101820",
        ember: "#d6452f",
        lemon: "#f7c548",
        sage: "#2f8f7f",
        parchment: "#f7f2e7",
      },
      fontFamily: {
        display: ["'Bespoke Serif'", "Georgia", "serif"],
        body: ["'Spline Sans'", "Arial", "sans-serif"],
      },
      boxShadow: {
        soft: "0 20px 60px rgba(16, 24, 32, 0.15)",
      },
    },
  },
  plugins: [],
};
