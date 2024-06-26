import axios from "axios";
import { IQuestionaireResponse } from "../pages/questionnaires/userLevelQuestionnaires";

const API_BASE_URL = "http://127.0.0.1:5000"; // Update with your Flask server address

export const SApiService = {
  login: async (data: { username: string; password: string }): Promise<any> => {
    return axios.post(`${API_BASE_URL}/login`, data);
  },

  uploadFile: async (data: {
    userId: number;
    dataProfile: {};
    selectedFile: File;
    selectedColumns: string[];
  }) => {
    try {
      const formData = new FormData();
      formData.append("file", data.selectedFile);
      formData.append("columns", data.selectedColumns.join(","));
      const dataProfile = {
        userId: data.userId,
        dataProfile: data.dataProfile,
      };
      formData.append("dataProfile", JSON.stringify(dataProfile));
      const response = await axios.post(
        `${API_BASE_URL}/uploadFile`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error("Error uploading file:", error);
      throw error;
    }
  },

  updateUserProfile: async (data: {
    userId: number;
    userProfile: IQuestionaireResponse[];
  }): Promise<any> => {
    return axios.post(`${API_BASE_URL}/update-user-profile`, data);
  },

  updateDataContext: async (data: {
    userId: number;
    userProfile: IQuestionaireResponse[];
  }): Promise<any> => {
    return axios.post(`${API_BASE_URL}/update-data-context`, data);
  },
  insertRule: async (data: {
    ruleName: string;
    description: string;
    condition: string | null;
    informationType: string | null;
    action: string;
  }): Promise<any> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/insert-rules`, data);
      return response.data;
    } catch (error) {
      console.error("Error inserting rule:", error);
      throw error;
    }
  },
  insertFeedback: async (data: {
    ruleId: number;
    userProfileId: number;
    dataProfileId: number;
    preference: boolean;
  }): Promise<any> => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/insert-feedback`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error inserting rule:", error);
      throw error;
    }
  },
};
