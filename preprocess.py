import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
import clip
from PIL import Image
from sentence_transformers import SentenceTransformer

# Load the CLIP model and preprocessing pipeline
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

# Load a text embedding model
text_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load embeddings from the pickle file
with open('../data/image_embeddings.pickle', 'rb') as f:
    embeddings = pickle.load(f)

image_folder = "static/coco_images_resized"
image_paths = [os.path.join(image_folder, os.path.basename(path)) for path in embeddings['file_name']]

print("Generated image paths in preprocess.py:")
for path in image_paths[:5]:  # Print the first few paths for verification
    print(path)

image_features = np.stack(embeddings['embedding'])

# Normalize embeddings for similarity search
normalized_features = image_features / np.linalg.norm(image_features, axis=1, keepdims=True)

def get_image_embedding(image_path):
    """
    Convert an image into an embedding using the official OpenAI CLIP implementation.
    """
    image = clip_preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = clip_model.encode_image(image).cpu().numpy()
    return embedding

def get_text_embedding(query_text):
    """

    Convert a text query into an embedding using the CLIP model.
    """
    text = clip.tokenize([query_text]).to(device)
    with torch.no_grad():
        embedding = clip_model.encode_text(text).cpu().numpy()
    return embedding

def get_top_k_similar_images(query_vector, k=5):
    """
    Given a query vector, return the top k most similar images and their similarity scores.
    """
    similarities = cosine_similarity(query_vector.reshape(1, -1), normalized_features).flatten()
    top_k_indices = np.argsort(similarities)[::-1][:k]
    top_k_scores = similarities[top_k_indices]
    top_k_paths = [image_paths[i] for i in top_k_indices]

    # Debug: Print the paths being returned
    print("Top K Paths:", top_k_paths)

    return list(zip(top_k_paths, top_k_scores))
