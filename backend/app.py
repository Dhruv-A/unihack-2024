from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from slide_translation.find_and_replace import FindAndReplace


app = Flask(__name__)

# ensuring there is upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/translate_slide', methods=['POST'])
def translate_slide():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # no filename selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # send the request to the frontend
        find_text = request.form.get('find_text')
        replace_text = request.form.get('replace_text')

        # Process the file
        slide_translator = FindAndReplace()
        output_file_path = f'../sample_presentations/translated_{filename}'
        slide_translator.replace_text_in_presentation(file_path, find_text, replace_text, output_file_path)

        return jsonify({'message': 'File translated', 'output_file': output_file_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
