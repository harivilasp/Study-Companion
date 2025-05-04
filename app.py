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

import logging

# ... (rest of your imports)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    extracted_text = None
    web_results = None
    youtube_results = None
    uploaded_image_url = None

    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_image_url = '/' + filepath
            logger.info(f'Image uploaded: {filename}')
            try:
                file.seek(0)
                extracted_text = img_ocr_copy.ocr_from_imagefile(file)
                logger.info(f'OCR extracted text: {extracted_text[:100]}...')
                if not extracted_text.strip():
                    error = 'No text detected in image.'
                    logger.warning('No text detected in image.')
                else:
                    # If extracted text is short, skip summarization
                    num_sentences = extracted_text.count('.') + extracted_text.count('!') + extracted_text.count('?')
                    if len(extracted_text) < 200 or num_sentences < 2:
                        summary = extracted_text.strip()
                        logger.info('Extracted text is short, skipping summarization.')
                    else:
                        summary_list = para_summarizer.generate_summary(extracted_text, top_n=2)
                        summary = ' '.join(summary_list)
                        logger.info(f'Summary: {summary}')
                    # Web search
                    try:
                        web_results = list(search_results.gsearch(summary))
                        youtube_results = list(search_results.gsearch('youtube : ' + summary))
                        logger.info(f'Web results: {web_results[:2]}...')
                        logger.info(f'YouTube results: {youtube_results[:2]}...')
                    except Exception as e:
                        logger.error(f'Web search error: {e}')
                        web_results = None
                        youtube_results = None
            except Exception as e:
                error = f'OCR or summarization error: {str(e)}'
                logger.error(error)
        else:
            error = 'Please upload or paste an image.'
            logger.warning('No image uploaded.')

    return render_template('index.html', summary=summary, error=error, input_text='', extracted_text=extracted_text, web_results=web_results, youtube_results=youtube_results, uploaded_image_url=uploaded_image_url)

if __name__ == '__main__':
    app.run(debug=True)
