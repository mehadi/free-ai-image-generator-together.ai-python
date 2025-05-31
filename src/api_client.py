import os
from dotenv import load_dotenv
import requests
from PIL import Image
import io
import base64
import logging
import json
from datetime import datetime, timedelta
from collections import deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'api_logs_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

class TogetherAIClient:
    def __init__(self):
        self.api_key = os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            logger.error("TOGETHER_API_KEY not found in environment variables")
            raise ValueError("TOGETHER_API_KEY not found in environment variables")
        self.api_url = "https://api.together.xyz/v1/images/generations"
        self.rate_limit = 6  # Maximum requests per minute
        self.request_times = deque(maxlen=self.rate_limit)  # Store timestamps of recent requests
        logger.info("TogetherAIClient initialized successfully")

    def _check_rate_limit(self):
        """Check if we've exceeded the rate limit"""
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        
        # Remove timestamps older than 1 minute
        while self.request_times and self.request_times[0] < one_minute_ago:
            self.request_times.popleft()
        
        if len(self.request_times) >= self.rate_limit:
            oldest_request = self.request_times[0]
            wait_time = (oldest_request + timedelta(minutes=1) - current_time).total_seconds()
            if wait_time > 0:
                raise Exception(f"Rate limit exceeded. Please wait {int(wait_time)} seconds before trying again.")

    def generate_image(self, prompt, model="black-forest-labs/FLUX.1-schnell-Free", width=576, height=1024, steps=4, seed=42, negative_prompt=None):
        """
        Generate an image using Together.ai's API
        
        Args:
            prompt (str): The text prompt for image generation
            model (str): The model to use for generation
            width (int): Image width
            height (int): Image height
            steps (int): Number of diffusion steps
            seed (int): Random seed for reproducibility
            negative_prompt (str, optional): What to avoid in the image
            
        Returns:
            PIL.Image: The generated image
        """
        try:
            # Check rate limit before making the request
            self._check_rate_limit()
            
            logger.info(f"Generating image with model: {model}")
            logger.info(f"Prompt: {prompt}")
            logger.info(f"Parameters: width={width}, height={height}, steps={steps}, seed={seed}")
            if negative_prompt:
                logger.info(f"Negative prompt: {negative_prompt}")
            
            # Prepare the request headers and data
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "prompt": prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "n": 1,
                "response_format": "b64_json"
            }
            
            if negative_prompt:
                data["negative_prompt"] = negative_prompt
            
            # Make the API request
            logger.info("Making API request to Together.ai")
            response = requests.post(self.api_url, headers=headers, json=data)
            
            # Add current request timestamp to the queue
            self.request_times.append(datetime.now())
            
            # Handle specific HTTP errors
            if response.status_code == 401:
                raise Exception("Invalid API key. Please check your TOGETHER_API_KEY")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again later")
            elif response.status_code == 400:
                error_msg = response.json().get('error', 'Unknown error')
                raise Exception(f"Invalid request: {error_msg}")
            
            response.raise_for_status()
            
            response_data = response.json()
            
            # Log the full response structure
            logger.info("API Response received:")
            logger.info(f"Response type: {type(response_data)}")
            logger.info(f"Response content: {json.dumps(response_data, indent=2) if isinstance(response_data, dict) else response_data}")
            
            # Check if response contains the image data
            if not response_data or 'data' not in response_data or not response_data['data']:
                logger.error("No image data found in response")
                raise Exception("No image data found in response")
            
            # Get the base64 image data
            image_data = response_data['data'][0]['b64_json']
            
            # Convert base64 to image
            logger.info("Converting base64 to image")
            try:
                image_data = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_data))
                logger.info("Image generated successfully")
                return image
            except Exception as e:
                logger.error(f"Error processing image data: {str(e)}")
                raise Exception("Failed to process image data")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}", exc_info=True)
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}", exc_info=True)
            raise Exception(f"Error generating image: {str(e)}") 