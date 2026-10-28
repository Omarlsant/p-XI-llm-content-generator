/**
 * Centralized API configuration.
 *
 * Uses VITE_API_BASE_URL if explicitly defined.
 * Defaults to an empty string '' so relative requests (/api/...)
 * work consistently through Vite proxy in development and Nginx reverse proxy in Docker/production.
 */
export const API_BASE_URL: string = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) ? import.meta.env.VITE_API_BASE_URL : '';
