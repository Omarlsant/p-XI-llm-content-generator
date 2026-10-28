import { register } from 'node:module';
import { pathToFileURL } from 'node:url';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const loaderUrl = pathToFileURL(join(__dirname, 'ts-loader.mjs')).href;
register(loaderUrl, import.meta.url);
