import axios from "axios";

export const openHands = axios.create();

export const setAuthTokenHeader = (token: string) => {
  openHands.defaults.headers.common.Authorization = `Bearer ${token}`;
};

export const setGitHubTokenHeader = (token: string) => {
  openHands.defaults.headers.common["X-GitHub-Token"] = token;
};

export const removeAuthTokenHeader = () => {
  if (openHands.defaults.headers.common.Authorization) {
    delete openHands.defaults.headers.common.Authorization;
  }
};

export const removeGitHubTokenHeader = () => {
  if (openHands.defaults.headers.common["X-GitHub-Token"]) {
    delete openHands.defaults.headers.common["X-GitHub-Token"];
  }
};

const CLIENT_AUTH = import.meta.env.VITE_CLIENT_AUTH === "True";
if (CLIENT_AUTH) {
  const CLIENT_JWT = import.meta.env.VITE_CLIENT_JWT;
  setAuthTokenHeader(CLIENT_JWT);
}
