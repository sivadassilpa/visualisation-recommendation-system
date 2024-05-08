import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // Update with your Flask server address

export const SApiService = {
  visualise: async (data: { username: String }): Promise<any> => {
    return axios.post(`${API_BASE_URL}/visualise`, data);
  },
};
