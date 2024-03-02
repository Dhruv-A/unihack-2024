from flask import Flask, request, jsonify, session, redirect, abort
from werkzeug.utils import secure_filename
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import os
import pathlib
from slide_translation.find_and_replace import FindAndReplace
from slide_translation.pptx_to_gslides import GDriveUploader
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = "<Add your own unique Google Client Id from the client_secret.json here>"
client_secrets_file = os.path.join(pathlib.Path(os.getcwd()), "creds.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost/callback"
)

# ensuring there is upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/translate_slide', methods=['POST'])
def translate_slide():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    target_language = request.form['language']

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
        slide_translator.replace_text_in_presentation(filename, target_language, file_path)

        # 
        # Upload to GDrive
        gdrive_uploader = GDriveUploader()
        gdrive_uploader.upload_ppt(f"translated_presentations/{filename}_translated.pptx")

        return jsonify(gdrive_uploader.get_sharable_link())

@app.route('/login')
def login():
    pass




if __name__ == '__main__':
    app.run(host='localhost', port='5173', debug=True)
