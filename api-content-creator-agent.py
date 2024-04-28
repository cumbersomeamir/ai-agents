import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Attempt to read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_images(prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=5,
        size="1024x1024"
    )
    
    images = []
    # Collect all the urls from the response
    for image in response.data:
        images.append(image.url)
    
    return images

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    prompt = data['prompt']
    try:
        image_urls = generate_images(prompt)
        return jsonify({'images': image_urls})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
