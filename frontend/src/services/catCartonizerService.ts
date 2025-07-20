import api from "../lib/api";
import mockGenerationRun from "../data/mockGenerationRun.json";
import type { GenerationRun } from "../types/catGeneration";
class catCartoonizerService {
  async getCartoonizedCat(): Promise<GenerationRun> {
    if (process.env.NODE_ENV === "development") {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockGenerationRun as GenerationRun);
        }, 1000);
      });
    }
    try {
      const response = await api.get("/api/cartoonize-cat");
      return response.data;
    } catch (error) {
      console.error("Error fetching cartoonized cat:", error);
      return mockGenerationRun as GenerationRun;
    }
  }
}

const catCartoonizerServiceInstance = new catCartoonizerService();
export default catCartoonizerServiceInstance;
