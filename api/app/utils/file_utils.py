import mimetypes
import base64
def load_txt_instuctions(file_path: str) -> str:
    """
    Load instructions from a text file.
    
    :param file_path: Path to the text file containing instructions.
    :return: Content of the text file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            instructions = file.read()
        return instructions
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    

def get_image_data_url(image_path: str) -> str:
    """
    Convert an image file to a data URL.
    
    :param image_path: Path to the image file.
    :return: Data URL of the image.
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image/'):
        mime_type = 'image/jpeg'  # fallback

    # Create a data URL for client-side rendering
    data_url = f"data:{mime_type};base64,{encoded_image}"
    return data_url
