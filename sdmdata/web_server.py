#!/usr/bin/env python
# -*-coding:utf-8-*-

# import build-in library
import os
import json
import shutil
import hashlib
import subprocess
import logging
import tempfile
import tarfile
from logging.handlers import RotatingFileHandler

# import third party library
import tablib
import chardet

# import flask
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import make_response
from flask import url_for

# import extension library of flask
from flask.ext.login import LoginManager
from flask.ext.login import UserMixin
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user

# import self build library
from sdmdata.db import Occurrence
from sdmdata.db import Species
from sdmdata.db import User
from sdmdata.db import State
from sdmdata.db import create_session

# import database library
from sqlalchemy.orm.exc import NoResultFound

import app_config

# create our little application :)
app = Flask(__name__)
app.config.from_object(app_config)
app.debug = True
# TODO: log file
handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
if app.debug:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
# app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# TODO: count_limit need be in app.config
count_limit = 50


class UserManager(UserMixin):
    def __init__(self, user_name, user_id):
        self.user_name = user_name
        self.id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    db_session = create_session()
    try:
        user_obj = db_session.query(User).filter(User.id == user_id).one()
        user_name = user_obj.login_name
        user = UserManager(user_name, user_id)
        return user
    except NoResultFound:
        return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = bool(remember)
        db_session = create_session()
        hash_obj = hashlib.md5()
        hash_obj.update(password)
        hashed_password = hash_obj.hexdigest()

        check_result = db_session.query(User).filter(User.login_name == user_name,
                                                     User.password == hashed_password).count()

        if check_result:
            user_obj = db_session.query(User).filter(User.login_name == user_name,
                                                     User.password == hashed_password).one()
            user_id = user_obj.id
            user = UserManager(user_name, user_id)
            login_result = login_user(user, remember=remember)
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('user/login.html')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("/user/change-password.html")
    else:
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        db_session = create_session()
        hash_obj = hashlib.md5()
        hash_obj.update(old_password)
        hashed_password = hash_obj.hexdigest()

        check_result = db_session.query(User).filter(User.login_name == current_user.user_name,
                                                     User.password == hashed_password).count()

        if check_result:
            user_obj = db_session.query(User).filter(User.login_name == current_user.user_name,
                                                     User.password == hashed_password).one()
            hash_obj = hashlib.md5()
            hash_obj.update(new_password)
            hashed_password = hash_obj.hexdigest()
            user_obj.password = hashed_password
            db_session.commit()
            return render_template("message.html", result=True)
        else:
            return render_template("message.html", result=False, url="/change-password")


@app.route("/manage-user")
@login_required
def manage_user():
    if current_user.user_name == "admin":
        db_session = create_session()
        user_list = db_session.query(User).all()
        return render_template("user/manage-user.html", user_list=user_list)


@app.route("/add-user", methods=["POST"])
@login_required
def add_user():
    if current_user.user_name == "admin":
        username = request.form["username"]
        password = request.form["password"]
        hash_obj = hashlib.md5()
        hash_obj.update(password)
        hashed_password = hash_obj.hexdigest()
        db_session = create_session()
        user = User(login_name=username, password=hashed_password)
        db_session.add(user)
        db_session.commit()
        return render_template("message.html", result=True, url="/manage-user")


@app.route("/delete-user")
@login_required
def delete_user():
    if current_user.user_name == "admin":
        user_id = request.args["user_id"]
        db_session = create_session()
        try:
            user_obj = db_session.query(User).filter(User.id == user_id).one()
        except NoResultFound:
            return "user not exists"
        db_session.delete(user_obj)
        db_session.commit()
        return render_template("message.html", result=True, url="/manage-user")


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route("/upload-species-csv", methods=["GET", "POST"])
@login_required
def upload_species_csv():
    if request.method == "GET":
        return render_template("upload-species-csv/upload.html")
    if request.method == 'POST':
        work_dir = os.path.join(".", "workspace")
        csv_file = os.path.join(work_dir, "data.csv")
        f = request.files['species_file']
        f.save(csv_file)
        upload_result = True

        fd = open(csv_file, "rb")
        buf = fd.read()
        fd.close()
        encode_result = chardet.detect(buf)
        if encode_result["encoding"] == "ascii":
            encode_ascii = True
        else:
            encode_ascii = False
            upload_result = False
            os.remove(csv_file)
        return render_template("upload-species-csv/result.html", upload_result=upload_result, encode_ascii=encode_ascii)


@app.route("/import-species-csv")
@login_required
def import_species_csv():
    work_dir = os.path.join(".", "workspace")
    csv_file = os.path.join(work_dir, "data.csv")
    csv_file_flag = os.path.exists(csv_file)
    return render_template('import-species-csv/import.html', csv_file=csv_file_flag)


@app.route("/import-species-csv-result")
@login_required
def import_species_csv_result():
    from sdmdata.import_species_csv import import_species_csv

    work_dir = os.path.join(".", "workspace")
    csv_file = os.path.join(work_dir, "data.csv")
    unique_list, duplicate_list = import_species_csv(csv_file, col_index=0)
    imported_species_count = len(unique_list)
    duplicate_species_count = len(duplicate_list)
    os.remove(csv_file)
    return render_template('import-species-csv/result.html',
                           duplicate_count=duplicate_species_count,
                           imported_count=imported_species_count)


@app.route("/view-species-list")
@login_required
def edit_species_list():
    db_session = create_session()
    species_count = db_session.query(Species.species_name).count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("view-species-list.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("download_species_list"),
                           data_url=url_for("species_list_data"))


@app.route("/species-list-data")
@login_required
def species_list_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).all()
    json_string = json.dumps(species_list)
    return json_string


@app.route("/download-species-list")
@login_required
def download_species_list():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).all()
    headers = ["Species name"]

    raw_data = list(species_list)

    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=species-name-list.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/empty-species-list")
@login_required
def empty_species_list():
    return render_template("empty-species-list.html")


@app.route("/do-empty-species-list")
@login_required
def do_empty_species_list():
    db_session = create_session()
    db_session.query(Species).delete()
    db_session.commit()
    return render_template("message.html", result=True)


@app.route("/check-species-name")
@login_required
def check_species_name():
    import subprocess

    subprocess.Popen(["./check_species_name_daemon.py", "start"])
    return render_template('check-species-name/result.html')


@app.route("/control-species-check")
@login_required
def control_species_check():
    command = request.args["command"]

    subprocess.Popen(["./check_species_name_daemon.py", command])
    return json.dumps(True)


@app.route("/species-check-status")
@login_required
def species_check_status():
    import subprocess

    daemon_process = subprocess.Popen(["./check_species_name_daemon.py", "status"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_output, err_output = daemon_process.communicate()
    std_output = std_output.strip(" \n")
    json_string = json.dumps([std_output, err_output])
    return json_string


@app.route("/check-species-name-progress")
@login_required
def check_species_name_progress():
    db_session = create_session()
    species_count = db_session.query(Species).count()
    species_fetch_done = db_session.query(Species).filter(Species.name_correct != None).count()
    json_string = json.dumps([species_fetch_done, species_count])
    return json_string


@app.route("/checked-species-name")
@login_required
def checked_species_name():
    db_session = create_session()
    species_count = db_session.query(Species).filter(Species.name_correct == True).count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("checked-species-name.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("export_checked_species_name_data"),
                           data_url=url_for("checked_species_name_data"))


@app.route("/checked-species-name-data")
@login_required
def checked_species_name_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name,
                                    Species.kingdom,
                                    Species.phylum,
                                    Species.clazz,
                                    Species.order,
                                    Species.superfamily,
                                    Species.family,
                                    Species.genus,
                                    Species.species,
                                    Species.infraspecific).filter(Species.name_correct == True).all()
    json_string = json.dumps(species_list)
    return json_string


@app.route("/export-checked-species-name-data")
@login_required
def export_checked_species_name_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name,
                                    Species.kingdom,
                                    Species.phylum,
                                    Species.clazz,
                                    Species.order,
                                    Species.superfamily,
                                    Species.family,
                                    Species.genus,
                                    Species.species,
                                    Species.infraspecific).filter(Species.name_correct == True).all()

    headers = ["Species name", "Kingdom", "Phylum", "Class", "Order", "Superfamily", "Family", "Genus",
               "Scientific Name", "Infraspecific Taxon"]

    raw_data = list(species_list)

    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=checked-species-name.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/error-species-name")
@login_required
def error_species_name():
    db_session = create_session()
    species_count = db_session.query(Species).filter(Species.name_correct == False).count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("error-species-name.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("export_error_species_name_data"),
                           data_url=url_for("error_species_name_data"))


@app.route("/error-species-name-data")
@login_required
def error_species_name_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.name_correct == False).all()
    json_string = json.dumps(species_list)
    return json_string


@app.route("/export-error-species-name-data")
@login_required
def export_error_species_name_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.name_correct == False).all()

    raw_data = list(species_list)

    headers = ["Species name"]
    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=error-species-name.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/fetch-occurrence")
@login_required
def fetch_occurrence():
    import subprocess
    subprocess.Popen(["./fetch_data_daemon.py", "start"])
    return render_template('fetch-occurrence/result.html')


@app.route("/control-fetch-occurrence")
@login_required
def control_fetch_occurrence():
    command = request.args["command"]
    import subprocess

    subprocess.Popen(["./fetch_data_daemon.py", command])
    return json.dumps(True)


@app.route("/fetch-occurrence-status")
@login_required
def fetch_occurrence_status():
    import subprocess

    daemon_process = subprocess.Popen(["./fetch_data_daemon.py", "status"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    std_output, err_output = daemon_process.communicate()
    std_output = std_output.strip(" \n")
    json_string = json.dumps([std_output, err_output])
    return json_string


@app.route("/species-no-occurrence")
@login_required
def species_no_occurrence():
    db_session = create_session()
    species_count = db_session.query(Species.species_name).filter(Species.no_data == True).count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("species-no-occurrence.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("export_species_no_occurrence_data"),
                           data_url=url_for("species_no_occurrence_data"))


@app.route("/species-no-occurrence-data")
@login_required
def species_no_occurrence_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.no_data == True).all()
    json_string = json.dumps(species_list)
    return json_string


@app.route("/export-species-no-occurrence-data")
@login_required
def export_species_no_occurrence_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.no_data == True).all()
    raw_data = list(species_list)

    headers = ["Species name"]
    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=species-no-occurrence-data.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/species-non-occurrence")
@login_required
def species_non_occurrence():
    db_session = create_session()
    species_count = db_session.query(Species).filter(Species.have_un_coordinate_data == True).count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("species-non-occurrence.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("export_species_non_occurrence_json"),
                           data_url=url_for("species_non_occurrence_data"))


@app.route("/species-non-occurrence-data")
@login_required
def species_non_occurrence_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.have_un_coordinate_data == True).all()
    json_string = json.dumps(species_list)
    return json_string


@app.route("/export-species-non-occurrence-json")
@login_required
def export_species_non_occurrence_json():
    db_session = create_session()

    temp_dir = tempfile.mkdtemp()
    _, temp_file = tempfile.mkstemp()

    tar = tarfile.open(temp_file, "w")

    data_obj = db_session.query(Species.un_coordinate_data, Species.species_name).filter(Species.have_un_coordinate_data == True).all()
    for data_item in data_obj:
        json_string = data_item.un_coordinate_data
        file_name = data_item.species_name + ".csv"
        full_file_path = os.path.join(temp_dir, file_name)
        fd = open(full_file_path, "w")
        fd.write(json_string)
        fd.close()

    file_list = os.listdir(temp_dir)
    file_list = [os.path.join(temp_dir, file_item) for file_item in file_list]
    for name in file_list:
        tar.add(name)
    tar.close()

    static_file = "static/download/un-occurrence-data.tar"
    static_file_url_path = os.path.join("/", static_file)

    shutil.move(temp_file, static_file)

    return render_template('download/link.html', file_url=static_file_url_path)


@app.route("/export-species-non-occurrence-data")
@login_required
def export_species_non_occurrence_data():
    db_session = create_session()
    species_list = db_session.query(Species.species_name).filter(Species.have_un_coordinate_data == True).all()
    raw_data = list(species_list)

    headers = ["Species name"]
    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=species-un-occurrence-data.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/empty-occurrence")
@login_required
def empty_occurrence():
    return render_template('fetch-occurrence/empty.html')


@app.route("/do-empty-occurrence")
@login_required
def do_empty_occurrence():
    db_session = create_session()
    db_session.query(Occurrence).delete()
    db_session.commit()
    db_session.query(Species).filter(Species.in_process == True).update({"in_process": 0}, synchronize_session=False)
    db_session.commit()

    # TODO: directory
    # remove json file
    shutil.rmtree("un-occurrence-data")
    os.mkdir("un-occurrence-data")
    return render_template("message.html", result=True)


@app.route("/fetch-occurrence-progress")
@login_required
def fetch_occurrence_progress():
    db_session = create_session()
    species_count = db_session.query(Species).filter(Species.name_correct == True).count()
    species_fetch_done = db_session.query(Species).filter(Species.in_process == True).count()
    json_string = json.dumps([species_fetch_done, species_count])
    return json_string


@app.route("/cross-check")
@login_required
def cross_check():
    import subprocess

    subprocess.Popen(["./cross_check_daemon.py", "start"])
    return render_template('cross-check/result.html')


@app.route("/cross-check-progress")
@login_required
def cross_check_progress():
    db_session = create_session()
    occurrence_count = db_session.query(Occurrence).count()
    occurrence_check_done = db_session.query(Occurrence).filter(Occurrence.cross_check != None).count()
    json_string = json.dumps([occurrence_check_done, occurrence_count])
    return json_string


@app.route("/control-cross-check")
@login_required
def control_cross_check():
    command = request.args["command"]
    import subprocess

    subprocess.Popen(["./cross_check_daemon.py", command])
    return json.dumps(True)


@app.route("/cross-check-status")
@login_required
def cross_check_status():
    import subprocess

    daemon_process = subprocess.Popen(["./cross_check_daemon.py", "status"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_output, err_output = daemon_process.communicate()
    std_output = std_output.strip(" \n")
    json_string = json.dumps([std_output, err_output])
    return json_string


@app.route("/view-cross-check")
@login_required
def view_cross_check():
    db_session = create_session()
    species_count = db_session.query(Occurrence.species_name).distinct().count()
    if species_count >= count_limit:
        ajax_display = False
    else:
        ajax_display = True
    return render_template("/view-cross-check.html", species_count=species_count, ajax_display=ajax_display,
                           count_limit=count_limit, download_link=url_for("download_cross_check_result"),
                           data_url=url_for("cross_check_result"))


@app.route("/cross-check-result")
@login_required
def cross_check_result():
    db_session = create_session()
    state_obj = db_session.query(State).delete()
    species_list = db_session.query(Occurrence.species_name).distinct()

    for species_obj in species_list:
        species_name = species_obj.species_name
        correct = db_session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                      Occurrence.cross_check == 1).count()
        incorrect = db_session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                        Occurrence.cross_check == 0).count()
        unknown_country = db_session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                              Occurrence.cross_check == -1).count()
        species_info = State(species_name=species_name, correct=correct, incorrect=incorrect,
                             unknown_country=unknown_country)
        db_session.add(species_info)
    db_session.commit()

    state_list = db_session.query(State.species_name, State.correct, State.incorrect, State.unknown_country).all()
    state_list = list(state_list)
    json_string = json.dumps(state_list)
    return json_string


@app.route("/download-cross-check-result")
@login_required
def download_cross_check_result():
    db_session = create_session()
    state_list = db_session.query(State.species_name, State.correct, State.incorrect, State.unknown_country).all()

    raw_data = list(state_list)

    headers = ["Species name", "Correct", "Incorrect", "Country unknown"]
    data = tablib.Dataset(*raw_data, headers=headers)

    csv_string = data.csv

    resp = make_response(csv_string)
    resp.headers['Content-Disposition'] = 'attachment;filename=download-cross-check-result.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route("/marked-as-checked")
@login_required
def marked_as_checked():
    db_session = create_session()
    db_session.query(Occurrence).update({'cross_check': 1})
    db_session.commit()
    return render_template("message.html", result=True)


@app.route("/empty-check-result")
@login_required
def empty_check_result():
    db_session = create_session()
    db_session.query(Occurrence).update({'cross_check': None})
    db_session.commit()
    return render_template("message.html", result=True)


@app.route("/get-cross-check-result")
@login_required
def get_cross_check_result():
    db_session = create_session()
    state_obj = db_session.query(State.species_name, State.correct, State.incorrect, State.unknown_country).all()
    state_list = list(state_obj)
    json_string = json.dumps(state_list)
    return json_string


@app.route("/export")
@login_required
def export():
    db_session = create_session()
    country_obj_list = db_session.query(Occurrence.country_code).distinct()

    country_list = []
    for country_obj in country_obj_list:
        country_code = country_obj.country_code
        country_list.append(country_code)

    return render_template("export/index.html", country_list=country_list)


@app.route("/download")
@login_required
def download():
    area_country_all = int(request.args.get("country_all"))
    if not area_country_all:
        country_list = request.args.getlist("country")
    else:
        country_list = None

    output_all = int(request.args.get("output_all"))

    if not output_all:
        output_type = request.args.getlist("output_type")
    else:
        output_type = None

    # TODO: check format
    output_format = request.args.get("format")

    # TODO: this part need to a daemon not to block user interface
    temp_dir = tempfile.mkdtemp()

    from sdmdata.export_data_main import export_data

    print(temp_dir, output_format, country_list, output_type)

    export_data(temp_dir, output_format, country_list, output_type)

    _, temp_file = tempfile.mkstemp()
    tar = tarfile.open(temp_file, "w")
    file_list = os.listdir(temp_dir)
    file_list = [os.path.join(temp_dir, file_item) for file_item in file_list]
    for name in file_list:
        tar.add(name)
    tar.close()

    # # TODO: multiply project will be a problem
    # static_file = "static/download/output_" + output_format + ".tar"
    # static_file_url_path = os.path.join("/", static_file)
    # shutil.move(temp_file, static_file)
    #
    # return render_template('export/download.html', file_url=static_file_url_path)

    fd = open(temp_file, "rb")
    tar_string = fd.read()
    fd.close()

    resp = make_response(tar_string)
    resp.headers['Content-Disposition'] = 'attachment;sdmdata-data.tar'
    resp.headers['Content-type'] = 'application/x-tar'
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)