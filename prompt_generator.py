from openai import OpenAI
import os
from dotenv import load_dotenv
from get_image import get_cat_image

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class PromptGenerator:
    def __init__(self, model: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.image_url = None
        self.model = model

    def generate_prompt(self) -> str:
        if not self.image_url:
            self.image_url = get_cat_image(save_image=True)
        user_input = f"""You are an expert prompt writer for the Stability AI API. Your task is to create a detailed description of the image to generate a cute cartoon cat
        image.Please provide a detailed description of the cat's appearance, colors, and any other relevant details that would help in generating a cute cartoon cat image. 
        Make sure to focus on the style and characteristics that would make the cat look adorable and cartoonish. Provide detailed style instructions, such as the type of cartoon style (e.g., anime, western cartoon, etc.), the mood of the image (e.g., playful, sleepy), and any specific features that should be highlighted (e.g., big eyes, fluffy fur).
        Respond in the format of a prompt for the Stability AI API. Do not include any additional text or explanations, just the prompt itself."""
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_input},
                        {"type": "input_image", "image_url": self.image_url},
                    ],
                }
            ],
        )
        generation_prompt=response.output_text
        return generation_prompt
