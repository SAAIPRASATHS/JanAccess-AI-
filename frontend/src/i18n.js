import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import enTranslation from './locales/en/translation.json';
import hiTranslation from './locales/hi/translation.json';
import taTranslation from './locales/ta/translation.json';
import bnTranslation from './locales/bn/translation.json';

const resources = {
    en: {
        translation: enTranslation
    },
    hi: {
        translation: hiTranslation
    },
    ta: {
        translation: taTranslation
    },
    bn: {
        translation: bnTranslation
    }
};

i18n
    .use(LanguageDetector) // Detect user language
    .use(initReactI18next) // Pass i18n to react-i18next
    .init({
        resources,
        fallbackLng: 'en', // Default language
        supportedLngs: ['en', 'hi', 'ta', 'bn'],
        detection: {
            order: ['localStorage', 'navigator', 'htmlTag'],
            caches: ['localStorage'],
        },
        interpolation: {
            escapeValue: false // React already escapes values
        }
    });

export default i18n;
