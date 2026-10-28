import test from 'node:test';
import assert from 'node:assert';
import { generateContent, queryVectorRAG, queryGraphRAG } from '../services/contentGeneratorAPI';

test('generateContent succeeds with generated_content and image', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => {
      return {
        ok: true,
        status: 200,
        json: async () => ({
          generated_content: { blog: 'Markdown content' },
          errors: {},
          image_url: 'https://images.unsplash.com/sample',
          image_alt: 'Sample AI image',
          success: true
        })
      } as unknown as Response;
    };

    const res = await generateContent({
      topic: 'Test Topic',
      platforms: ['blog'],
      model: 'llama3',
      language: 'English'
    });

    assert.strictEqual(res.generated_content.blog, 'Markdown content');
    assert.strictEqual(res.image_url, 'https://images.unsplash.com/sample');
    assert.strictEqual(res.success, true);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('generateContent handles partial failures and throws on 502 total failure', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => {
      return {
        ok: false,
        status: 502,
        statusText: 'Bad Gateway',
        json: async () => ({
          detail: {
            message: 'All requested platforms failed generation.',
            errors: { blog: 'Ollama timeout', X: 'Rate limit' }
          }
        })
      } as unknown as Response;
    };

    await assert.rejects(
      async () => {
        await generateContent({
          topic: 'Failing Topic',
          platforms: ['blog', 'X'],
          model: 'llama3',
          language: 'English'
        });
      },
      (err: Error) => {
        assert.match(err.message, /All requested platforms failed generation/);
        return true;
      }
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('queryVectorRAG and queryGraphRAG invoke endpoints properly', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async (url) => {
      const urlStr = String(url);
      if (urlStr.includes('/query-vector')) {
        return {
          ok: true,
          status: 200,
          json: async () => ({ answer: 'Vector RAG answer' })
        } as unknown as Response;
      }
      return {
        ok: true,
        status: 200,
        json: async () => ({ answer: 'Graph RAG answer' })
      } as unknown as Response;
    };

    const vectorRes = await queryVectorRAG({ question: 'What is RAG?' });
    assert.strictEqual(vectorRes.answer, 'Vector RAG answer');

    const graphRes = await queryGraphRAG({ question: 'Who is Lewis?' });
    assert.strictEqual(graphRes.answer, 'Graph RAG answer');
  } finally {
    globalThis.fetch = originalFetch;
  }
});
