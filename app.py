# app.py
from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO, emit, join_room
import os
import io
import zipfile
from werkzeug.utils import secure_filename
import logging
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from collections import defaultdict
from threading import Lock

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'srt'}
socketio = SocketIO(app)

# Ensure upload and processed folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

logging.basicConfig(level=logging.DEBUG)

# Use defaultdict for user-specific data
uploaded_files = defaultdict(list)
file_timestamps = defaultdict(dict)
processing_status = defaultdict(lambda: {'status': 'idle', 'progress': 0})
lock = Lock()

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        user_id = request.remote_addr
        files = request.files.getlist('file')
        with lock:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    uploaded_files[user_id].append(filename)
                    file_timestamps[user_id][filename] = datetime.now()
                else:
                    return jsonify({'error': 'Only .srt files are allowed!'}), 400
        return jsonify({'files': uploaded_files[user_id]}), 200
    except Exception as e:
        logging.error(f"Error during upload: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process():
    try:
        user_id = request.remote_addr
        seconds_to_add = int(request.form.get('seconds'))

        def process_files(user_id):
            try:
                with lock:
                    processing_status[user_id]['status'] = 'processing'
                total_files = len(uploaded_files[user_id])
                zip_filename = f'output_{user_id}.zip'
                output = io.BytesIO()

                with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for index, filename in enumerate(uploaded_files[user_id]):
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                        modified_content = modify_srt(lines, seconds_to_add)
                        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                        with open(processed_file_path, 'w', encoding='utf-8') as file:
                            file.write(modified_content)
                        logging.info(f"Processed file created at: {processed_file_path}")
                        with open(processed_file_path, 'r', encoding='utf-8') as file:
                            zf.writestr(filename, file.read())
                        # Delete the processed file after adding to zip
                        os.remove(processed_file_path)
                        logging.info(f"Processed file deleted: {processed_file_path}")
                        with lock:
                            processing_status[user_id]['progress'] = int((index + 1) / total_files * 100)

                output.seek(0)
                zip_file_path = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)
                with open(zip_file_path, 'wb') as f:
                    f.write(output.read())

                # Delete original uploaded files
                for filename in uploaded_files[user_id]:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.info(f"Uploaded file deleted: {file_path}")
                
                with lock:
                    processing_status[user_id]['status'] = 'done'
                    socketio.emit('processing_done', {'user_id': user_id}, room=user_id)
                # Schedule deletion of the zip file after 5 minutes
                scheduler.add_job(delete_files, 'date', run_date=datetime.now() + timedelta(minutes=5), args=[user_id, [zip_file_path]])
            except Exception as e:
                logging.error(f"Error during processing: {e}")
                with lock:
                    processing_status[user_id]['status'] = 'error'

        threading.Thread(target=process_files, args=(user_id,)).start()
        return jsonify({'status': 'processing'}), 200
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    user_id = request.remote_addr
    return jsonify(processing_status[user_id])

@app.route('/download', methods=['GET'])
def download():
    user_id = request.remote_addr
    try:
        zip_file_path = os.path.join(app.config['PROCESSED_FOLDER'], f'output_{user_id}.zip')
        return send_file(zip_file_path, mimetype='application/zip', as_attachment=True, download_name='modified_srt_files.zip')
    except Exception as e:
        logging.error(f"Error during download: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    user_id = request.remote_addr
    join_room(user_id)
    emit('connected', {'message': 'Connected to server'}, room=user_id)

def delete_files(user_id, filenames):
    try:
        with lock:
            for filename in filenames:
                if os.path.exists(filename):
                    os.remove(filename)
                if filename in file_timestamps[user_id]:
                    del file_timestamps[user_id][filename]
            del uploaded_files[user_id]
            del processing_status[user_id]
        logging.info(f"Deleted files for user {user_id}: {filenames}")
    except Exception as e:
        logging.error(f"Error during file deletion: {e}")

def delete_idle_files():
    try:
        now = datetime.now()
        idle_users = []
        with lock:
            for user_id in list(file_timestamps.keys()):
                idle_files = [filename for filename, timestamp in file_timestamps[user_id].items() if now - timestamp > timedelta(hours=1)]
                if idle_files:
                    delete_files(user_id, idle_files)
                    idle_users.append(user_id)
        logging.info(f"Deleted idle files for users: {idle_users}")
    except Exception as e:
        logging.error(f"Error during idle file deletion: {e}")

def modify_srt(lines, seconds_to_add):
    import re
    pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})')
    modified_lines = []
    for line in lines:
        match = pattern.match(line)
        if match:
            start_hour, start_minute, start_second, start_millisecond, end_hour, end_minute, end_second, end_millisecond = map(int, match.groups())
            end_second += seconds_to_add
            if end_second >= 60:
                end_minute += end_second // 60
                end_second = end_second % 60
            if end_minute >= 60:
                end_hour += end_minute // 60
                end_minute = end_minute % 60
            modified_line = f'{start_hour:02}:{start_minute:02}:{start_second:02},{start_millisecond:03} --> {end_hour:02}:{end_minute:02}:{end_second:02},{end_millisecond:03}\n'
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)
    return ''.join(modified_lines)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(delete_idle_files, 'interval', hours=1)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)