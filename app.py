from flask import Flask, render_template, request
import para_summarizer
import nltk
import os
from werkzeug.utils import secure_filename
import img_ocr_copy
import search_results

# Ensure NLTK resources are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    input_text = ''
    extracted_text = None
    web_results = None
    youtube_results = None
    uploaded_image_url = None

    if request.method == 'POST':
        # Text input or image upload?
        file = request.files.get('image')
        input_text = request.form.get('input_text', '').strip()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_image_url = '/' + filepath
            try:
                # OCR
                file.seek(0)
                extracted_text = img_ocr_copy.ocr_from_imagefile(file)
                if not extracted_text.strip():
                    error = 'No text detected in image.'
                else:
                    input_text = extracted_text
            except Exception as e:
                error = f'OCR error: {str(e)}'
        if input_text:
            try:
                # Summarize
                summary_list = para_summarizer.generate_summary(input_text, top_n=2)
                summary = ' '.join(summary_list)
                # Web search
                try:
                    web_results = list(search_results.gsearch(summary))
                    youtube_results = list(search_results.gsearch('youtube : ' + summary))
                except Exception as e:
                    web_results = None
                    youtube_results = None
            except Exception as e:
                error = f'Error during summarization or search: {str(e)}'
        elif not error:
            error = 'Please upload an image or enter/paste some text.'

    return render_template('index.html', summary=summary, error=error, input_text=input_text, extracted_text=extracted_text, web_results=web_results, youtube_results=youtube_results, uploaded_image_url=uploaded_image_url)

if __name__ == '__main__':
    app.run(debug=True)
