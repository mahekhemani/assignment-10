from preprocess import get_image_embedding

# Test with an example image
image_path = "../data/house.jpg"
embedding = get_image_embedding(image_path)
print("Embedding shape:", embedding.shape)
