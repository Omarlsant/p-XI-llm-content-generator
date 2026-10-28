import test from 'node:test';
import assert from 'node:assert';
import { SUPPORTED_LANGUAGES } from '../constants/languages.ts';

test('languages constant contains all 6 supported languages', () => {
  const expectedLanguages = [
    'English',
    'Spanish',
    'French',
    'German',
    'Japanese',
    'Italian',
  ];

  const actualKeys = Object.keys(SUPPORTED_LANGUAGES);
  assert.strictEqual(actualKeys.length, 6);

  for (const lang of expectedLanguages) {
    assert.strictEqual(
      SUPPORTED_LANGUAGES[lang as keyof typeof SUPPORTED_LANGUAGES],
      lang
    );
  }
});
