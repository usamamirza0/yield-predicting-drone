from flask import Flask, render_template, request
import werkzeug
from functions import initialize, my_yield, request_data

app = Flask(__name__, template_folder='template', static_folder='C:\\Users\\usama\\Documents\\Server\\static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

model, device = initialize()   

@app.route('/')
def upload_file():
    print(request.method)
    return render_template('upload.html')
	
@app.route('/result', methods = ['GET', 'POST'])
def uploaded_file():
    print(request.method)
    if request.method == 'POST':
        f = request.files['file']
        f.save(werkzeug.utils.secure_filename(f.filename))
        yield_value = my_yield(f.filename, model, device)
        request_data()
        return render_template('result.html', value=yield_value)
    return 'file uploaded successfully'

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0')