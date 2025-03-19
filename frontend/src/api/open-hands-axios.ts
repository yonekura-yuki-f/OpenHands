import axios from "axios";

export const openHands = axios.create({
  baseURL: `${window.location.protocol}//${import.meta.env.VITE_BACKEND_BASE_URL || window?.location.host}`,
});

const CLIENT_JWT = import.meta.env.VITE_CLIENT_JWT;
if (CLIENT_JWT) {
  openHands.defaults.headers.common.Authorization = `Bearer ${CLIENT_JWT}`;
}
