import test from 'node:test';
import assert from 'node:assert';

test('application navigation routes contract', () => {
  const routes = [
    { path: '/', name: 'Home' },
    { path: '/generate', name: 'Our Agents' },
    { path: '/generate/content-agent', name: 'Content Form' },
    { path: '/generate/query-agent', name: 'Query Agent' },
    { path: '/scientific-rag', name: 'Scientific RAG' },
    { path: '/about', name: 'About' },
    { path: '*', name: 'Not Found' }
  ];

  assert.strictEqual(routes.length, 7);
  const paths = routes.map(r => r.path);
  assert.ok(paths.includes('/'));
  assert.ok(paths.includes('/generate'));
  assert.ok(paths.includes('/generate/content-agent'));
  assert.ok(paths.includes('/generate/query-agent'));
  assert.ok(paths.includes('/scientific-rag'));
  assert.ok(paths.includes('/about'));
  assert.ok(paths.includes('*'));
});
