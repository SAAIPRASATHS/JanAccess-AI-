import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: `${API_BASE}/api`,
  timeout: 30000,
});

// ─── Assistant ─────────────────────────────────
export const assistantService = {
  chat: async (query, lowBandwidth = false, persona = null) => {
    let url = `/assistant/chat?query=${encodeURIComponent(query)}&low_bandwidth=${lowBandwidth}`;
    if (persona) {
      url += `&persona=${encodeURIComponent(persona)}`;
    }
    const { data } = await api.post(url);
    return data;
  },

  voiceChat: async (audioBlob, persona = null) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    let url = '/assistant/voice-chat';
    if (persona) {
      url += `?persona=${encodeURIComponent(persona)}`;
    }
    const { data } = await api.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },

  getPersonaOptions: async () => {
    const { data } = await api.get('/assistant/persona-options');
    return data;
  },
};

// ─── Eligibility ─────────────────────────────────
export const eligibilityService = {
  checkEligibility: async (criteria) => {
    const { data } = await api.post('/eligibility/check', criteria);
    return data;
  }
};

// ─── Document ─────────────────────────────────
export const documentService = {
  analyze: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.post('/document/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  }
};

// ─── Skills & Jobs ─────────────────────────────────
export const skillsService = {
  getRecommendations: async (input) => {
    const { data } = await api.post('/skills/recommend', input);
    return data;
  }
};

// ─── Analytics ─────────────────────────────────
export const analyticsService = {
  getSummary: async () => {
    const { data } = await api.get('/analytics/summary');
    return data;
  },
  getTopSchemes: async (limit = 10) => {
    const { data } = await api.get(`/analytics/top-schemes?limit=${limit}`);
    return data;
  },
  getHistory: async (limit = 20) => {
    const { data } = await api.get(`/analytics/history?limit=${limit}`);
    return data;
  },
  getPersonaUsage: async () => {
    const { data } = await api.get('/analytics/persona-usage');
    return data;
  },
};

export default api;
