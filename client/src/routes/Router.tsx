import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout";
import Home from "../pages/Home";
import ContentPage from "../pages/ContentPage";
import AboutPage from "../pages/AboutPage";

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
                path: "/about",
                element: <AboutPage />
            }
        ]
    }
]);