import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Ganzhi APIs
export const searchGanzhi = (keyword) =>
  api.get(`/ganzhi/search?q=${encodeURIComponent(keyword)}`);

export const getGanzhiDetail = (ganzhi) =>
  api.get(`/ganzhi/${encodeURIComponent(ganzhi)}`);

export const compareGanzhi = (list) =>
  api.get(`/ganzhi/compare?list=${list.join(',')}`);

// Nayin APIs
export const getNayinByGanzhi = (ganzhi) =>
  api.get(`/nayin/by-ganzhi/${encodeURIComponent(ganzhi)}`);

export const getGanzhiByNayin = (nayinName) =>
  api.get(`/nayin/${encodeURIComponent(nayinName)}/ganzhi`);

export const getNayinStatusList = () =>
  api.get('/nayin/status');

export const getNayinByStatus = (status) =>
  api.get(`/nayin/status/${encodeURIComponent(status)}`);

export const getNayinByCategory = (category) =>
  api.get(`/nayin/category/${encodeURIComponent(category)}`);

export const calcNayin = (ganzhi) =>
  api.get(`/nayin/calc/${encodeURIComponent(ganzhi)}`);

// Shensha APIs
export const getShenshaList = (params) =>
  api.get('/shensha', { params });

export const getShenshaDetail = (name) =>
  api.get(`/shensha/${encodeURIComponent(name)}`);

export const getGanzhiShensha = (ganzhi) =>
  api.get(`/ganzhi/${encodeURIComponent(ganzhi)}/shensha`);

export const getZixingRules = () =>
  api.get('/shensha/zixing');

// Guanxi APIs
export const getAllGuanxi = () =>
  api.get('/guanxi/all');

export const getGuanxiByGanzhi = (ganzhi) =>
  api.get(`/ganzhi/${encodeURIComponent(ganzhi)}/guanxi`);

export const getGuanxiTypes = () =>
  api.get('/guanxi/types');

// Admin APIs
export const adminLogin = (credentials) =>
  api.post('/admin/login', credentials);

export const adminExport = () =>
  api.get('/admin/export');

export default api;
