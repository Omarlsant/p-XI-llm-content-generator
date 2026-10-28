import test from 'node:test';
import assert from 'node:assert';
import { invokeQueryAgent } from '../services/queryAgentAPI';

test('invokeQueryAgent returns response answer on 200 OK', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => {
      return {
        ok: true,
        status: 200,
        json: async () => ({ answer: 'Query agent response in markdown' })
      } as unknown as Response;
    };

    const res = await invokeQueryAgent({
      question: 'Explain RAG vs Fine-tuning',
      language: 'English',
      use_search: false,
      company_info: ''
    });

    assert.strictEqual(res.answer, 'Query agent response in markdown');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('invokeQueryAgent throws informative error on 404 endpoint not found', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => {
      return {
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({})
      } as unknown as Response;
    };

    await assert.rejects(
      async () => {
        await invokeQueryAgent({
          question: 'Hello',
          language: 'English',
          use_search: false,
          company_info: ''
        });
      },
      (err: Error) => {
        assert.match(err.message, /Not Found/);
        return true;
      }
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});
