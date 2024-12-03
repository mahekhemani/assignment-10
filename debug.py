import pickle

# Load the embeddings file
with open('../data/image_embeddings.pickle', 'rb') as f:
    embeddings = pickle.load(f)

# Print the DataFrame info and column names
print("Type of embeddings:", type(embeddings))
print("Embeddings DataFrame columns:", embeddings.columns)
