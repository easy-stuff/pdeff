// tailwind.config.js
// -------------------
// Tailwind config for Flask app
// enables VSCode class IntelliSense
module.exports = {
    content: [
        // all html is here
        "./templates/**/*.{html,jinja,js}",
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}
