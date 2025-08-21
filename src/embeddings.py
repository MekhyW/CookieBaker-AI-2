import os
from typing import List, Optional
from openai import OpenAI
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.text_model = "text-embedding-3-small"
        self.image_model = "text-embedding-3-small"  # For image descriptions
    
    def generate_text_embedding(self, text: str) -> List[float]:
        """Generate embedding for text content"""
        try:
            response = self.client.embeddings.create(model=self.text_model, input=text)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating text embedding: {e}")
            return [0.0] * 1536 # Return zero vector as fallback
    
    def describe_image(self, image_data: str) -> str:
        """Generate description of image using OpenAI Vision API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this image in detail, focusing on key visual elements, objects, people, actions, and context that would be relevant for conversation memory."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error describing image: {e}")
            return "Image content could not be analyzed"
    
    def generate_image_embedding(self, image_data: str) -> List[float]:
        """Generate embedding for image by first describing it, then embedding the description"""
        try:
            description = self.describe_image(image_data)
            return self.generate_text_embedding(description)
        except Exception as e:
            print(f"Error generating image embedding: {e}")
            return [0.0] * 1536 # Return zero vector as fallback
    
    def generate_combined_embedding(self, text: Optional[str] = None, image_data: Optional[str] = None) -> List[float]:
        """Generate combined embedding for text and/or image content"""
        embeddings = []
        if text:
            text_embedding = self.generate_text_embedding(text)
            embeddings.append(np.array(text_embedding))
        if image_data:
            image_embedding = self.generate_image_embedding(image_data)
            embeddings.append(np.array(image_embedding))
        if not embeddings:
            return [0.0] * 1536 # Return zero vector if no content
        if len(embeddings) > 1: # Average the embeddings if we have both text and image
            combined = np.mean(embeddings, axis=0)
            norm = np.linalg.norm(combined) # Normalize the combined embedding
            if norm > 0:
                combined = combined / norm
            return combined.tolist()
        else:
            return embeddings[0].tolist()
    
    def prepare_search_query_embedding(self, query_text: str, context: Optional[str] = None) -> List[float]:
        """Prepare embedding for search queries, optionally including context"""
        search_text = query_text
        if context:
            search_text = f"Context: {context}\nQuery: {query_text}"
        return self.generate_text_embedding(search_text)

embedding_generator = EmbeddingGenerator()