# 🎨 AI Image Generator

A modern web application that generates stunning images using Together.ai's Stable Diffusion model. Built with Streamlit, this application provides an intuitive interface for creating AI-generated artwork.

![AI Image Generator](https://img.shields.io/badge/AI-Image%20Generator-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)

## ✨ Features

- 🖼️ Generate high-quality images using Stable Diffusion
- ⚙️ Customizable image parameters (width, height, steps, seed)
- 🎯 Advanced settings with negative prompts
- 💾 Automatic image saving and gallery view
- 📥 Easy image download functionality
- 🎨 Modern and intuitive user interface
- 🔄 Real-time image generation feedback

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mehadi/free-ai-image-generator-together.ai-python
cd free-ai-image-generator-together.ai-python
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your Together.ai API key:
   - Sign up at [Together.ai](https://www.together.ai)
   - Get your API key from the dashboard
   - Create a `.env` file in the project root and add:
   ```
   TOGETHER_API_KEY=your_api_key_here
   ```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## 🎯 Usage

1. **Basic Image Generation**:
   - Enter your prompt in the text area
   - Click "Generate Image"
   - Wait for the image to be generated

2. **Advanced Settings**:
   - Adjust image dimensions (width/height)
   - Modify generation steps
   - Set a specific seed for reproducibility
   - Add negative prompts to exclude unwanted elements

3. **Image Gallery**:
   - View all generated images
   - Download images directly from the gallery
   - Images are automatically saved locally

## 🔧 Configuration

The application can be configured through the following:

- **Image Parameters**:
  - Width: 512-1024 pixels
  - Height: 512-1024 pixels
  - Steps: 1-50
  - Seed: -1 to 2147483647

- **Model Selection**:
  - Currently supports: black-forest-labs/FLUX.1-schnell-Free

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Together.ai](https://www.together.ai) for providing the AI model
- [Streamlit](https://streamlit.io) for the web framework
- [Stable Diffusion](https://stability.ai) for the image generation model

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/ImageGeneratorTogatherAI](https://github.com/yourusername/ImageGeneratorTogatherAI) 