import axios from "axios";

const backendApi = axios.create({
  baseURL: "http://0.0.0.0:8080",
});

export default backendApi;
