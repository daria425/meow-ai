from get_image import get_cat_image, get_cartoonized_cat
from openai import OpenAI
from dotenv import load_dotenv
import os
from logger import logger
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client= OpenAI(api_key=OPENAI_API_KEY)
original_image_url = get_cat_image(save_image=True)
logger.info(f"Original cat image URL: {original_image_url}")
generation_chat_history=[
    {
        "role":"developer", 
        "content":f"""You are an expert prompt writer for the Stability AI API. The user will provide you with a photo of their cat.
        The user wants an adorable cartoon image as close to their cat photo as possible generated from Stability AI. 
        Your task is to create a detailed description of the image to generate a cute cartoon cat.
        image.
        Please provide a detailed description of the cat's appearance, colors, and any other relevant details that would help in generating a cute cartoon cat image. 
        Important details to include:
        - The cat's fur color and pattern (e.g., tabby, calico, solid)
        - The cat's eye color and shape
        - The cat's size and build (e.g., small, fluffy, slender)
        - Any distinctive features (e.g., unique markings, collar, toys)
        - The overall mood or expression of the cat (e.g., playful, sleepy, curious)
        - The setting or background (e.g., indoors, outdoors, with toys)
        - Emphasis on cuteness and cartoonish style
        - Use descriptive adjectives to enhance the prompt
        KEY GUIDELINES:
        Respond in the format of a prompt for the Stability AI API. Do not include any additional text or explanations, just the prompt itself.
        Do not say 'create an image' or 'generate an image', just provide the description directly."""
    },
]
generation_chat_history.append(
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": f"Here is a photo of my cat, please create a detailed description for a cute cartoon cat image based on this photo."
            },
            {
                "type": "input_image",
                "image_url": original_image_url
            }
        ]
    }
)

generation_prompt=client.responses.create(
    model="gpt-4o", 
    input=generation_chat_history,
    temperature=0.5
).output_text
logger.info(f"Generated prompt for cartoon image: {generation_prompt}")
cartoon_image=get_cartoonized_cat(
    prompt=generation_prompt, 
    output_image_path="images/cartoonized_cat.jpg"
)
logger.info(f"Cartoonized cat image saved as 'images/cartoonized_cat.jpg'")