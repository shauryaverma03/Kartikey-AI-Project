from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import tempfile
from PIL import Image
import mimetypes

# Load environment variables
load_dotenv()

# Configure Gemini API with the API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Set up the model - using the correct model name
model = genai.GenerativeModel('gemini-1.5-pro')

# Test the API connection
def test_api_connection():
    try:
        response = model.generate_content("Hello, are you working?")
        print("API Test Result:", response.text)
        return True
    except Exception as e:
        print("API Test Error:", str(e))
        return False

app = Flask(__name__)
CORS(app)

# Allowed image MIME types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

def validate_image(file):
    """Validate if the uploaded file is an allowed image type."""
    mime_type, _ = mimetypes.guess_type(file.filename)
    return mime_type in ALLOWED_IMAGE_TYPES

def get_gemini_response(prompt, image_path=None):
    try:
        # Check for greetings
        if prompt.lower().strip() in ["hii", "hi", "hello", "hey"] and not image_path:
            return "Hey there, history buff! I'm ChronicleAI, your snarky sidekick for digging up the past. Ready to unearth some old-school drama, roast a few dead kings, or figure out why everyone back then had such terrible haircuts? Let's hit the rewind button—what's your time-travel target?"
        
        # Add context for history-focused responses
        context = (
            "You are ChronicleAI, a snarky and witty history chatbot. Your responses should be informative, engaging, "
            "and include a touch of humor. Focus on historical accuracy while maintaining an entertaining tone. "
            "If an image is provided, analyze it for historical context, artifacts, or relevant details and incorporate "
            "that analysis into your response. If you're unsure about something, be honest about it."
        )
        
        # Prepare the content for the Gemini API
        content = [context, "\n\nUser prompt: ", prompt]
        
        # If an image is provided, include it in the content
        if image_path:
            try:
                img = Image.open(image_path)
                content.append(img)
                content.append("\n\nAdditional instruction: Analyze the provided image for historical context, artifacts, or relevant details.")
            except Exception as e:
                return f"Error processing image: {str(e)}"
        
        # Generate response
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        # Check for quota exceeded error
        if "429" in str(e):
            return (
                "Oops! Looks like we've hit our API quota limit. Don't worry though - you can either try again later "
                "(the quota should reset), or check out our documentation at https://ai.google.dev/docs/rate_limits "
                "for more info on upgrading your plan. In the meantime, why not explore some history books? "
                "They're like time machines that don't require API keys! 😉"
            )
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.form.get('message', '')
    image_file = request.files.get('image', None)
    
    if not user_message and not image_file:
        return jsonify({'error': 'No message or image provided'}), 400
    
    image_path = None
    if image_file:
        # Validate image
        if not validate_image(image_file):
            return jsonify({'error': 'Invalid image format. Only JPEG, PNG, and GIF are allowed.'}), 400
        
        # Save image to a temporary file
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.filename)[1]) as temp_file:
                image_file.save(temp_file.name)
                image_path = temp_file.name
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
    
    # Get response from Gemini
    response = get_gemini_response(user_message, image_path)
    
    # Clean up temporary image file
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception:
            pass
    
    return jsonify({'response': response})

@app.route('/api/test', methods=['GET'])
def test():
    success = test_api_connection()
    if success:
        return jsonify({'status': 'success', 'message': 'API connection successful'})
    else:
        return jsonify({'status': 'error', 'message': 'API connection failed'}), 500 

if __name__ == '__main__':
    # Test API connection on startup
    print("Testing API connection...")
    if test_api_connection():
        print("API connection successful!")
    else:
        print("API connection failed!")
    
    app.run(debug=True)