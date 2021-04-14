import os

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import utils

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files['file']
#
#         if file.filename == '':
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file', filename=filename))
#     return redirect(request.url)
#     # return '''
#     # <!doctype html>
#     # <title>Upload new File</title>
#     # <h1>Upload new File</h1>
#     # <form method=post enctype=multipart/form-data>
#     #   <input type=file name=file>
#     #   <input type=submit value=Upload>
#     # </form>
#     # '''

# @app.route("/upload", methods=["POST"])
# def upload():
#     uploaded_files = request.files.getlist("file[]")
#     print uploaded_files
#     return ""

@app.route('/', methods=['GET'])
def index():
    return render_template("temp_index.html")


@app.route('/facer', methods=['POST'])
def new_face_request():
    if request.method == 'POST':
        print(request.files)
        print(request.form)

        # files = request.files
        uploaded_files = request.files.getlist("face_file")
        album_link = request.form.get("album_link")

        if len(uploaded_files) == 0 or album_link is None:
            print("Not all data sent")
            return redirect(url_for(index))

        # print("files", files)

        for file in uploaded_files:
            print("file", file)

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                required_face_dir = app.config['UPLOAD_FOLDER']+"/required_face"
                utils.make_dir(required_face_dir)
                file.save(os.path.join(required_face_dir, filename))

        utils.find_face_in_album(album_link, app.config['UPLOAD_FOLDER'])

        return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
