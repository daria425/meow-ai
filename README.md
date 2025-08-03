# Meow AI

<img src="./cat cartoonizer.png" style="width: 500px; height:auto">

This project explores reflection-driven generative loops through a lightweight visual system. Given a random cat image, an LLM generates a prompt, which is used to create a new image via Stability AI. The result is then critiqued by another LLM acting as a reflection agent. Based on feedback, the prompt is revised and the cycle continues for three iterations.

Each iteration is logged and displayed, showing:

- the generated prompt

- the resulting image

- the LLM’s feedback

This project is an implementation of reflective generation, a fundamental pattern used in generative AI applications, inspired by this [Agentic Patterns Repository](https://github.com/neural-maze/agentic-patterns-course) by [Neural Maze](https://github.com/neural-maze).

## Tech Stack

### Backend

- **FastAPI**
- **Python 3.11**
- **WebSockets**

### Frontend

- **React 18**
- **TypeScript**
- **Vite**
- **TailwindCSS**
