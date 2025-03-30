/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,ts,jsx,tsx}", "./index.html"],
  theme: {
    extend: {
      fontFamily: {
        display: "SignPainter-HouseScript",
      },
      colors: {
        primary: "var(--color-primary)",
        secondary: "var(--color-secondary)",
        "almost-white": "var(--color-almost-white)",
        "enriched-black": "var(--color-enriched-black)",
        success: "var(--color-success)",
        error: "var(--color-error)",
      },
      zIndex: {
        1: 1,
      },
    },
  },
  plugins: [],
};
