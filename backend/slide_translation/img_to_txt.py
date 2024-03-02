import requests
import os
from dotenv import load_dotenv


class ImageToText:

    api_url = "https://api.api-ninjas.com/v1/imagetotext"

    def __init__(self, img_path: str, api_key: str):
        self.img_path = img_path
        self.api_key = api_key
        with open(self.img_path, "rb") as image_file_descriptor:
            files = {"image": image_file_descriptor}
        headers = {"X-Api-Key": self.api_key}
        r = requests.post(self.api_url, files=files, headers=headers)
        self.api_output = r.json()

    def get_wordlist(self) -> list[str]:
        """Returns a list of all words in the image"""
        return [w["text"] for w in self.textual_data]

    def get_concat_string(self) -> str:
        """Returns a string containing all words separated by a space"""
        return " ".join(self.get_wordlist())

    def get_api_output(self) -> list[dict]:
        """
        >>> imgtxt = ImageToText(image_path, api_key)
        >>> imgtxt.get_api_output() 
        [{'text': str, 'bounding_box': {'x1': int, 'y1': int, 'x2': int, 'y2': int}}, ...]
        """
        return self.api_output()


def main():
    # load env variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '../../.env')
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv('API_NINJA_API_KEY')

    image_path = os.path.join(script_dir, '../../sample_images/sample_image1.png')

    imgtxt = ImageToText(image_path, api_key)
    plaintext = imgtxt.get_plaintext()
    print(plaintext)

if __name__ == "__main__":
    main()


# Example API output:
# [{'text': '<:::>', 'bounding_box': {'x1': 28, 'y1': 27, 'x2': 211, 'y2': 211}}, {'text': 'circle', 'bounding_box': {'x1': 262, 'y1': 126, 'x2': 465, 'y2': 172}}, {'text': 'Amazing', 'bounding_box': {'x1': 31, 'y1': 271, 'x2': 271, 'y2': 330}}, {'text': 'image', 'bounding_box': {'x1': 316, 'y1': 271, 'x2': 483, 'y2': 330}}, {'text': 'with', 'bounding_box': {'x1': 525, 'y1': 271, 'x2': 658, 'y2': 317}}, {'text': 'text', 'bounding_box': {'x1': 32, 'y1': 348, 'x2': 166, 'y2': 389}}, {'text': 'inside', 'bounding_box': {'x1': 211, 'y1': 343, 'x2': 413, 'y2': 389}}, {'text': 'square', 'bounding_box': {'x1': 47, 'y1': 535, 'x2': 249, 'y2': 580}}]