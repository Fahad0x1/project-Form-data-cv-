from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash, session
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'a_very_secure_and_random_secret_key_123!@#'  # ضع هنا مفتاح سري قوي

UPLOAD_FOLDER = 'uploads'
EXCEL_FILE = 'data.xlsx'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# إنشاء مجلد الرفع إذا لم يكن موجودًا
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# إنشاء ملف الإكسل إذا لم يكن موجودًا مع الأعمدة المطلوبة
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['الاسم', 'المسمى الوظيفي', 'ملف السيرة الذاتية'])
    df.to_excel(EXCEL_FILE, index=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        job_title = request.form.get('job_title')
        file = request.files.get('cv')

        filename = ''
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # قراءة بيانات الملف وإضافة البيانات الجديدة
        df = pd.read_excel(EXCEL_FILE)
        new_entry = {'الاسم': name, 'المسمى الوظيفي': job_title, 'ملف السيرة الذاتية': filename}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        flash('تم تسجيل البيانات بنجاح.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "Fahad@123":
            session['logged_in'] = True
            return redirect(url_for('show_table'))
        else:
            flash("كلمة المرور خاطئة", "error")
    return render_template('login.html')


@app.route('/table')
def show_table():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    df = pd.read_excel(EXCEL_FILE)
    data = df.to_dict(orient='records')
    return render_template('table.html', data=data)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/logout')
def logout():
    session.clear()
    flash("تم تسجيل الخروج بنجاح.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
