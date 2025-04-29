# History Expert Chatbot

This is a specialized chatbot that answers questions about historical events, figures, and periods using the Gemini API. Built with Flask and modern web technologies.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

You can get a Gemini API key from: https://makersuite.google.com/app/apikey

## Running the Chatbot

To start the chatbot, run:
```bash
python app.py
```

The chatbot will be available at `http://localhost:5000`. Open this URL in your web browser to start chatting.

## Features

- Specialized in historical information
- Modern, responsive web interface
- Real-time chat experience
- Powered by Google's Gemini AI
- Built with Flask for robust backend handling

## Project Structure

- `app.py` - Main Flask application
- `templates/index.html` - Frontend interface
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file) 
