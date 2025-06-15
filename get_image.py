import requests
from dotenv import load_dotenv
import os

load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


def get_cat_image(save_image:bool=False)-> str:
    """
    Use The Cat API to get a random cat image URL.
    Returns:
        str: URL of the cat image.
    """
    url = "https://api.thecatapi.com/v1/images/search?mime_types=jpg,png"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]["url"]
        if save_image:
            image_data = requests.get(image_url).content
            if not os.path.exists("images"):
                os.makedirs("images")
            with open("images/cat_image.jpg", "wb") as file:
                file.write(image_data)
            print("Cat image saved as 'cat_image.jpg'")
        else:
            print(f"Cat image URL: {image_url}")
        return image_url
    else:
        print(f"Error: {response.status_code}")
        return None

def get_cartoonized_cat(prompt:str, output_image_path: str="images/cartoonized_cat.jpg"):
    """
    Use the Stability AI API to generate a cartoonized image of a cat based on a prompt.
    Args:
        prompt (str): The prompt for generating the cartoonized cat image.
        output_image_path (str): Path to save the generated image.
    """
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
"none":""
        },
        
        data={
            "prompt": prompt
        },
    )

    if response.status_code == 200:
        with open(output_image_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))