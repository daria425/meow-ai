import { api } from "../lib/api";
import mockGenerationRun from "../data/mockGenerationRun.json";
import type { GenerationRun, GenerationConfig } from "../types/catGeneration";
class catCartoonizerService {
  async getCartoonizedCat(
    generationConfig: GenerationConfig
  ): Promise<GenerationRun> {
    if (process.env.NODE_ENV === "development") {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockGenerationRun as GenerationRun);
        }, 1000);
      });
    }
    try {
      const { iterations } = generationConfig;
      const response = await api.get("/api/cartoonize-cat/live", {
        params: {
          iterations: iterations,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching cartoonized cat:", error);
      return mockGenerationRun as GenerationRun;
    }
  }
  async getLiveCartoonizedCatGeneration(
    generationConfig: GenerationConfig,
    sessionId: string | number
  ) {
    try {
      const { iterations } = generationConfig;
      const response = await api.get(`/api/cartoonize-cat/live/${sessionId}`, {
        params: {
          iterations: iterations,
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching cartoonized cat:", error);
      return mockGenerationRun as GenerationRun;
    }
  }
}

const catCartoonizerServiceInstance = new catCartoonizerService();
export default catCartoonizerServiceInstance;
