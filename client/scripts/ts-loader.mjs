import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export async function resolve(specifier, context, nextResolve) {
  try {
    return await nextResolve(specifier, context);
  } catch (err) {
    if (err && err.code === 'ERR_MODULE_NOT_FOUND' && (specifier.startsWith('.') || specifier.startsWith('/'))) {
      const base = new URL(specifier, context.parentURL);
      const basePath = fileURLToPath(base);
      for (const ext of ['.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js']) {
        if (existsSync(basePath + ext)) {
          return nextResolve(base.href + ext, context);
        }
      }
    }
    throw err;
  }
}
