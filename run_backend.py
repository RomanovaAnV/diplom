import json
import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename

import utils
from hashlib import sha256
from model.main_search import search_child_photos

import threading

from config import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder="templates", static_folder="templates/static")

app.secret_key = sha256().digest()
app.request_thread_storage = {
    'statuses': {},
    'log_files': {}
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    # return render_template("request_page.html")
    return render_template("request_page.html")


@app.route('/api/new_request', methods=['POST'])
def new_face_request():
    if request.method == 'POST':
        print(request.files)
        print(request.form)
        print(request.json)

        # files = request.files
        uploaded_files = request.files.getlist("face_file")
        album_link = request.form.get("album_link")
        request_id = utils.generate_request_id()
        print("REQUEST ID", request_id)

        session['request_id'] = request_id

        if len(uploaded_files) == 0 or album_link is None:
            print("Not all data sent")
            return redirect(url_for('index'))

        # print("files", files)

        for file in uploaded_files:
            print("file", file)

        request_dir = utils.define_request_dir(request_id)  # директория в которой будут файлы заявки
        utils.make_dir(request_dir)  # создать если нету

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  # имя файла
                required_face_dir = request_dir+searching_faces_subdir  # директория с фото искомого человека
                utils.make_dir(required_face_dir)
                file.save(os.path.join(required_face_dir, filename))

        # archive_link = utils.find_face_in_album(album_link, request_dir)

        request_thread = threading.Thread(target=utils.find_face_and_make_archive,
                                          args=(album_link, request_id, app.request_thread_storage, ), daemon=True)
        request_thread.start()
        # print("THREAD STATUSES", app.request_thread_storage["statuses"])

        # album_dir = utils.download_album_photos(album_link, request_dir)
        # archive_link = search_child_photos(upload_dir+"/" +
        #                                    str(request_id)+searching_faces_subdir, album_dir)

        download_url = url_for('download_result', request_id=request_id)
        # print(download_url)

        # response = app.response_class(
        #     response=json.dumps({"request_id": request_id}),
        #     status=200,
        #     mimetype='application/json'
        # )

        # return redirect(download_url)
        return jsonify(request_id=request_id)


@app.route('/downloads/<request_id>/result', methods=['GET', 'POST'])
def download_result(request_id: int):
    session_request_id = session.get('request_id')
    print("session request_id", session_request_id)
    print("request id", request_id)
    if (session_request_id is None) or int(session_request_id) != int(request_id):
        return url_for('new_face_request')

    archive_dir = upload_dir+"/"+str(request_id)
    return send_from_directory(archive_dir,
                               result_archive_name+".zip", as_attachment=True, attachment_filename="result.zip")


@app.route('/api/get_status', methods=['POST'])
def get_status():
    session_request_id = session.get('request_id')
    # print("asdf")
    # print(session.get('request_id'))
    # print(request.data)
    # print(request.json)
    request_id = request.json.get("request_id")
    if (session_request_id is None) or int(session_request_id) != int(request_id):
        return url_for('new_face_request')

    request_status = None
    if request_id is None:
        request_status = "none"
    else:
        thread_status = app.request_thread_storage["statuses"].get(int(request_id))
        print("CURRENT THREAD STATUS", thread_status)

        # request_status = "done" if utils.check_file_exists(upload_dir+"/"+result_archive_name+".zip") \
        #     else "processing"
        request_status = thread_status
    return jsonify(request_status=request_status)


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5011)
    app.run()