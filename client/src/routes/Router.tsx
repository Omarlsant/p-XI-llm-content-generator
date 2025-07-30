import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout";
import Home from "../pages/Home";
import ContentPage from "../pages/ContentPage";
import AboutPage from "../pages/AboutPage";
import ScientificPage from "../pages/ScientificPage";
import ContentFormPage from "../pages/ContentFormPage";
import ContentQueryPage from "../pages/ContentQueryPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        children: [
            {
                index: true,
                element: <Home />
            },
            {
                path: "/generate",
                element: <ContentPage />
            },
            {
                path: "/generate/content-agent",
                element: <ContentFormPage />
            },
            {
                path: "/generate/query-agent",
                element: <ContentQueryPage />
            },
            {
                path: "/scientific-rag",
                element: <ScientificPage />
            },
            {
                path: "/about",
                element: <AboutPage />
            }
        ]
    }
]);