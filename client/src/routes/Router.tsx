import { lazy, Suspense } from "react";
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout";
import RouteError from "../components/RouteError";
import PageLoader from "../components/PageLoader";

const Home = lazy(() => import("../pages/Home"));
const ContentPage = lazy(() => import("../pages/ContentPage"));
const AboutPage = lazy(() => import("../pages/AboutPage"));
const ScientificPage = lazy(() => import("../pages/ScientificPage"));
const ContentFormPage = lazy(() => import("../pages/ContentFormPage"));
const ContentQueryPage = lazy(() => import("../pages/ContentQueryPage"));
const NotFoundPage = lazy(() => import("../pages/NotFoundPage"));

const withSuspense = (Component: React.ComponentType) => (
  <Suspense fallback={<PageLoader />}>
    <Component />
  </Suspense>
);

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        errorElement: <RouteError />,
        children: [
            {
                index: true,
                element: withSuspense(Home)
            },
            {
                path: "/generate",
                element: withSuspense(ContentPage)
            },
            {
                path: "/generate/content-agent",
                element: withSuspense(ContentFormPage)
            },
            {
                path: "/generate/query-agent",
                element: withSuspense(ContentQueryPage)
            },
            {
                path: "/scientific-rag",
                element: withSuspense(ScientificPage)
            },
            {
                path: "/about",
                element: withSuspense(AboutPage)
            },
            {
                path: "*",
                element: withSuspense(NotFoundPage)
            }
        ]
    }
]);
