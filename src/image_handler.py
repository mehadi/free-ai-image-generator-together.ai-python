import os
from datetime import datetime
from PIL import Image

class ImageHandler:
    def __init__(self, save_dir="generated_images"):
        self.save_dir = save_dir
        self._ensure_save_directory()

    def _ensure_save_directory(self):
        """Create the save directory if it doesn't exist"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_image(self, image: Image.Image, prompt: str) -> str:
        """
        Save the generated image with a timestamp and return the file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a safe filename from the prompt
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{timestamp}_{safe_prompt}.png"
        filepath = os.path.join(self.save_dir, filename)
        
        image.save(filepath)
        return filepath

    def get_saved_images(self) -> list:
        """
        Get a list of all saved images
        """
        if not os.path.exists(self.save_dir):
            return []
        
        return [f for f in os.listdir(self.save_dir) if f.endswith(('.png', '.jpg', '.jpeg'))] 