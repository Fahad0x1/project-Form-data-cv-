from flask import Flask, render_template, request, redirect, send_from_directory
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXCEL_FILE = 'data.xlsx'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['الاسم', 'المسمى الوظيفي', 'ملف السيرة الذاتية'])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        job_title = request.form['job_title']
        file = request.files['cv']

        filename = ''
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        df = pd.read_excel(EXCEL_FILE)
        new_entry = {'الاسم': name, 'المسمى الوظيفي': job_title, 'ملف السيرة الذاتية': filename}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return redirect('/')

    return render_template('form.html')

@app.route('/table')
def show_table():
    df = pd.read_excel(EXCEL_FILE)
    return render_template('table.html', data=df.to_dict(orient='records'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
