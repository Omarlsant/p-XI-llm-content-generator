# Content GenerAItor — Frontend SPA

Interactive Single Page Application (SPA) for **Content GenerAItor**, designed for multi-platform AI content generation and scientific research retrieval.

---

## 🛠️ Tech Stack

* **Framework:** React 19 + TypeScript 5.8
* **Build Tool:** Vite 7 (powered by `@vitejs/plugin-react-swc` for fast refresh)
* **Styling:** Tailwind CSS v4 + `@tailwindcss/typography` (`.prose` rendering)
* **Routing:** React Router 7 (code-split with `React.lazy` and `Suspense`)
* **Components:** Custom accessible UI components, Material UI Icons (`@mui/icons-material`), Embla Carousel
* **Testing:** Node.js native test runner & Vitest compatibility harness

---

## 📁 Project Structure

```
client/
├── nginx.conf              # Production Nginx reverse proxy, gzip & caching headers
├── Dockerfile              # Multi-stage production container build (Node 22 -> Nginx)
├── package.json            # Scripts and dependencies
├── vite.config.ts          # SWC React plugin, Tailwind CSS v4 and backend API proxy
├── src/
│   ├── components/         # Reusable UI controls (Navbar, Footer, RouteError, Marquee)
│   ├── constants/          # Shared constants (SUPPORTED_LANGUAGES)
│   ├── layout/             # Global layout wrapper
│   ├── pages/              # Lazy-loaded views (Home, ContentForm, ContentQuery, Scientific, About, NotFound)
│   ├── routes/             # Router configuration with code-splitting
│   ├── services/           # Backend API integration clients (FastAPI endpoints)
│   └── tests/              # Unit test suites (languages, API mocks, routing)
```

---

## 🚀 Available Scripts

In the `client/` directory, you can run:

* `npm run dev`: Starts the local development server at `http://localhost:5173` with Fast Refresh and backend reverse proxy configured on `/api`.
* `npm run build`: Typechecks with `tsc -b` and builds production-optimized, code-split assets into `dist/`.
* `npm run lint`: Runs ESLint across all TypeScript and React files with zero warnings tolerance.
* `npm test`: Runs the automated unit test suite.
* `npm run preview`: Locally previews the production build.

---

## ⚙️ Environment Variables

The frontend is designed to work with relative paths by default, proxying `/api` requests to the FastAPI backend without requiring manual configuration.

If pointing to an external backend URL directly, configure `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```
