from prompt_generator import PromptGenerator
from get_image import get_cartoonized_cat

generator= PromptGenerator(model="gpt-4o-mini")
prompt = generator.generate_prompt()
print(f"Generated Prompt: {prompt}")
get_cartoonized_cat(prompt=prompt, output_image_path="cartoonized_cat.png")