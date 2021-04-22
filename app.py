import os, re
import zipfile
import shutil

import uuid as uuid
from flask import Flask, flash, render_template, request, make_response, redirect, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static/commons')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static/reports'

NOT_ALLOWED_EXTENSIONS = {'py'}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_unique_report_dir(directory, name):
    path = directory+'/reports'
    if os.path.exists(path):
        folders = 0
        for dirname in os.listdir(path):
            if name == dirname or re.match(name + "\([0-9]+\)", dirname):
                folders += 1
        if folders > 0:
            return f"reports/{name}({folders})/"
        else:
            return f"reports/{name}/"


def unzip_file(zip_src, dst_dir):
    """
    Unzip the zip file
         :param zip_src: full path of zip file
         :param dst_dir: the destination folder to extract to
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        with zipfile.ZipFile(zip_src, 'x') as report:
            report.extractall(app.config['UPLOAD_FOLDER'])
    else:
        return "Please upload zip file"


def save_report(name, report):
    if name == '':
        flash('No selected file')
        return redirect(request.url)
    if name:
        filename = secure_filename(name)
        directory = get_unique_report_dir('static', filename.rsplit('.', 1)[0])
        os.makedirs(str('static/'+directory))
        os.makedirs(str('templates/' + directory))

        file_path = os.path.join(BASE_DIR, 'static', str(uuid.uuid4()))
        report.save(file_path)
        target_path = os.path.join(BASE_DIR, str('static/'+directory))

        with zipfile.ZipFile(file_path, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(target_path)
        os.remove(file_path)  # delete file
        shutil.move(str(target_path+'/index.html'), str('templates/' + directory+'/index.html'))
        return filename


def get_all_report_name():
    return next(os.walk('templates/reports'))[1]


@app.route('/api/report', methods=['GET'])
def list_reports():
    """Endpoint to list report on the server."""
    return {
        'reports': next(os.walk('templates/reports'))[1]
    }


@app.route('/api/upload', methods=['POST'])
def save_html_report():
    response = make_response(
        jsonify(
            {"message": "Please upload zip file"}
        ),
        401,
    )

    resp = list()
    report_name = request.values['name']
    report = request.files.get("report")

    ret_list = report.filename.rsplit(".", maxsplit=1)
    if len(ret_list) != 2 or ret_list[1] != "zip":
        return make_response(jsonify({"message": "Please upload zip file"}), 400, )

    resp.append(save_report(report_name, report))
    if resp:
        return request.host_url + '/show/' + resp[-1]
    else:
        return render_template("commons/upload.html", message="No file selected")


@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template("commons/upload.html")


@app.route('/<path:path>')
def get_static_file(path):
    report_ref = request.cookies.get('report_ref')
    if report_ref:
        return app.send_static_file('reports/' + report_ref + '/' + path)
    else:
        return redirect('/home')


@app.route('/')
def render_report():
    if request.cookies.get('report_ref'):
        return render_template("commons/report.html", report_ref=request.cookies.get('report_ref'))
    else:
        return redirect('/home')


@app.route('/show/<report_ref>')
def show(report_ref):
    resp = make_response(redirect('/'))
    resp.set_cookie('report_ref', report_ref)
    return resp


@app.route('/home')
def home():
    return render_template("commons/home.html", report_list=get_all_report_name())


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
