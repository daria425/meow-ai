import { api } from "../lib/api";
import mockGenerationRun from "../data/mockGenerationRun.json";
import type {
  GenerationRunCompleteResponse,
  GenerationConfig,
} from "../types/catGeneration";
class catCartoonizerService {
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
      return mockGenerationRun as GenerationRunCompleteResponse;
    }
  }
}

const catCartoonizerServiceInstance = new catCartoonizerService();
export default catCartoonizerServiceInstance;
