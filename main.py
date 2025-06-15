from cat_cartoonizer import CatCartoonizerAgent

models={
    "generation_model": "gpt-4o", 
    "evaluation_model": "gpt-4o"

}

agent= CatCartoonizerAgent(
    models=models, 
)
agent.run_generation_loop(iterations=3)  # Run the generation loop for 3 iterations