import os
from openai import OpenAI


# Attempt to read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")


#Initialising openai client
client = OpenAI()

def generate_images(prompt):
    response = client.images.generate(
      model="dall-e-2",
      prompt= prompt,
      n=1,
      size="1024x1024"
    )
    
    images = []
    
    #Collect all the urls from the response
    for image in response.data:
        images.append(image.url)
    
    print("All the images are: " , images)
    return images


all_images = generate_images("A kuala skydiving")

