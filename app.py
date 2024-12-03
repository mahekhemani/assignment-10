from flask import Flask, render_template, request
import os
from flask import send_from_directory
from preprocess import get_top_k_similar_images, get_image_embedding, get_text_embedding

static_dir = os.path.abspath("../static")  # Adjusted to the correct folder
app = Flask(__name__, template_folder='../templates', static_folder=static_dir)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/debug-static-file/<path:filename>')
def debug_static_file(filename):
    file_path = os.path.join(app.static_folder, filename)
    return {"absolute_path": file_path, "exists": os.path.exists(file_path)}

# Route for serving static files explicitly
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        hybrid_weight = float(request.form.get('hybrid_weight', 0.5))
        
        if query_type == 'image' and 'query_image' in request.files:
            image_file = request.files['query_image']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(file_path)
            query_vector = get_image_embedding(file_path)
            results = get_top_k_similar_images(query_vector)
        
        elif query_type == 'text' and 'query_text' in request.form:
            query_text = request.form['query_text']
            query_vector = get_text_embedding(query_text)
            results = get_top_k_similar_images(query_vector)
        
        elif query_type == 'hybrid' and 'query_image' in request.files and 'query_text' in request.form:
            image_file = request.files['query_image']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(file_path)
            image_vector = get_image_embedding(file_path)
            text_vector = get_text_embedding(request.form['query_text'])
            
            query_vector = hybrid_weight * image_vector + (1 - hybrid_weight) * text_vector
            results = get_top_k_similar_images(query_vector)

        # Make sure paths are relative to /static/
        results = [(path, score) for path, score in results]  # Ensure correct paths for /static/
        print("Results (final paths):", results)  # Debugging

        # Debug: Print the paths being passed to the template
        print("Results being passed to the template:")
        for path, score in results:
            print(path)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
