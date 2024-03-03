from flask import Flask, request, jsonify, session, redirect, abort
from werkzeug.utils import secure_filename
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.oauth2 import id_token, service_account
import google.auth.transport.requests
import os
import pathlib
import requests
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from pip._vendor import cachecontrol
from slide_translation.find_and_replace import FindAndReplace
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, "../.env")
load_dotenv(dotenv_path=env_path)
WEBAPP_CREDENTIALS_PATH = os.path.join(script_dir, "../webapp_credentials.json")
SERVICE_CREDENTIALS_PATH = os.path.join(script_dir, "../service_credentials.json")
app.secret_key = os.getenv("CLIENT_SECRET")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = os.getenv("CLIENT_ID")
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=WEBAPP_CREDENTIALS_PATH,
    scopes=SCOPES,
    redirect_uri="http://localhost:5173/callback"
)

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

        print("FIND", find_text, "REPLACE", replace_text);

        # Process the file
        slide_translator = FindAndReplace()
        output_file_path = f'../sample_presentations/translated_{filename}'
        slide_translator.replace_text_in_presentation(filename, "DE", file_path)

        return jsonify({'message': 'File translated', 'output_file': output_file_path}), 200

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    # if not session["state"] == request.args["state"]:
    #     abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/upload")

@app.route("/upload", methods=['GET'])
def upload_files():

    ppts_uploads_folder = os.path.join(script_dir, "uploads/")
    credentials_file = SERVICE_CREDENTIALS_PATH
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    links = []

    for ppt_name in os.listdir(ppts_uploads_folder):
        ppt_path = os.path.join(ppts_uploads_folder, ppt_name)
        mime_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        file_metadata = {"name": ppt_name}
        media = MediaFileUpload(ppt_path, mimetype=mime_type)
        uploadfile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploadfile.get('id')
        file_id = uploadfile.get("id")
        service.permissions().create(
                fileId=file_id,
                body={'role': 'writer', 'type': 'anyone', 'value': 'anyone'}
            ).execute()
        file_metadata = service.files().get(fileId=file_id, fields='webViewLink').execute()
        webViewLink = file_metadata['webViewLink']

        sharable_link = f"{webViewLink}&export=download"
        links.append({"id": file_id, "name": ppt_name, "link": sharable_link})

    return jsonify(links), 200


if __name__ == '__main__':
    app.run(host='localhost', port='5173', debug=True)