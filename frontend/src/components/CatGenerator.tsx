import catCartoonizerServiceInstance from "../services/catCartonizerService";
import { useQuery } from "@tanstack/react-query";
import type { GenerationRun } from "../types/catGeneration";

function CatCartoonizer() {
  const { data, loading, error } = useQuery({
    queryFn: async () => {
      const response = await catCartoonizerServiceInstance.getCartoonizedCat();
      return response;
    },
  });
  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    return <div>Error loading cartoonized cat: {error.message}</div>;
  }
  if (!data) {
    return <div>No cartoonized cat data available.</div>;
  }
  return (
    <div>
      <h1>Cartoonized Cat</h1>
      <img src={data.original_image_url} alt="Original Cat" />
      {data.runs.map((run) => (
        <div key={run.iteration_num}>
          <h2>Iteration {run.iteration_num}</h2>
          <p>Prompt: {run.prompt}</p>
          <img
            src={run.cartoonized_image}
            alt={`Cartoonized Cat ${run.iteration_num}`}
          />
          <h3>Evaluation</h3>
          <ul>
            <li>
              Similarity to Original:{" "}
              {run.evaluation.evaluation.similarity_to_original}
            </li>
            <li>
              Cuteness Factor: {run.evaluation.evaluation.cuteness_factor}
            </li>
            <li>Artistic Style: {run.evaluation.evaluation.artistic_style}</li>
            <li>
              Overall Impression: {run.evaluation.evaluation.overall_impression}
            </li>
          </ul>
          <p>Critique: {run.evaluation.critique}</p>
        </div>
      ))}
    </div>
  );
}
