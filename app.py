import os
from main import ConnectFlask
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

UPLOAD_FOLDER = '/home/innovationchef/Desktop/resume-parser/data/flask/'
ALLOWED_EXTENSIONS = set(['docx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route("/", methods=['GET', 'POST'])
# def main():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('index', file=filename))
#     return """
#             <!doctype html>
#             <title>Upload new File</title>
#             <h1>Upload new File</h1>
#             <form action="" method=post enctype=multipart/form-data>
#               <p><input type=file name=file>
#                  <a href={{ url_for('index') }}> <input type=submit value=Upload> </a>
#             </form>
#             <p>%s</p>
#             """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

# @app.route("/index/<file>")
# def index(file):
#     app.logger.info(file)
#     Resume = ConnectFlask(file)
#     print(Resume.parse())
#     lnames = ['HTML', 'CSS', 'JS', 'GO', 'Python']
#     return render_template('index.html', lnames=lnames, lemails=lnames, lphones=lnames, laddresses=lnames)

@app.route("/")
def main():
    lnames = ['HTML', 'CSS', 'JS', 'GO', 'Python']
    return render_template('index.html', lnames=lnames, lemails=lnames, lphones=lnames, laddresses=lnames)



if __name__ == "__main__":
    app.debug = True
    app.run()






























# from flask import Flask, render_template, url_for


# app = Flask(__name__)

# @app.route("/")
# def main():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.debug = True
#     app.run()