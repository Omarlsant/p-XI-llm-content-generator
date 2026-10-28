export const SUPPORTED_LANGUAGES = {
  English: 'English',
  Spanish: 'Spanish',
  French: 'French',
  German: 'German',
  Japanese: 'Japanese',
  Italian: 'Italian',
} as const;

export type SupportedLanguage = keyof typeof SUPPORTED_LANGUAGES;
