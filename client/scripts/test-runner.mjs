#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const clientRoot = join(__dirname, '..');
const vitestBin = join(clientRoot, 'node_modules', '.bin', 'vitest');

const args = process.argv.slice(2);

if (existsSync(vitestBin)) {
  console.log('--- Running tests via Vitest ---');
  const child = spawn(vitestBin, ['run', ...args.filter(a => a !== '--run')], {
    cwd: clientRoot,
    stdio: 'inherit',
    env: process.env
  });
  child.on('close', code => process.exit(code ?? 0));
} else {
  console.log('--- Running tests via Node.js native test runner ---');
  const testsDir = join(clientRoot, 'src', 'tests');
  let testFiles = [];
  if (existsSync(testsDir)) {
    testFiles = readdirSync(testsDir)
      .filter(f => f.endsWith('.test.ts') || f.endsWith('.test.js'))
      .map(f => join(testsDir, f));
  }

  if (testFiles.length === 0) {
    console.log('No test files found in src/tests.');
    process.exit(0);
  }

  // Filter out vitest-specific flags like --run so node --test doesn't error
  const nodeArgs = ['--import', './scripts/register-ts-loader.mjs', '--test', ...testFiles];
  const child = spawn(process.execPath, nodeArgs, {
    cwd: clientRoot,
    stdio: 'inherit',
    env: process.env
  });
  child.on('close', code => process.exit(code ?? 0));
}
