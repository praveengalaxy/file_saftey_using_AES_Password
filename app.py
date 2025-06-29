from flask import Flask, request, send_file, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64, os, io
from zipfile import ZipFile

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for flashing messages

UPLOAD_FOLDER = 'files_example'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_key(password: str, salt: bytes) -> bytes:
    """Derive a secret key from the password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt-decrypt')
def encrypt_decrypt():
    return render_template('encrypt_decrypt.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    files = request.files.getlist('file')
    password = request.form.get('password')
    if not files or files[0].filename == '':
        flash("No file selected for encryption!", "error")
        return redirect(url_for('encrypt_decrypt'))
    if not password:
        flash("Password is required!", "error")
        return redirect(url_for('encrypt_decrypt'))

    if len(files) == 1:
        file = files[0]
        filename = secure_filename(file.filename)
        data = file.read()
        salt = os.urandom(16)
        key = generate_key(password, salt)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        encrypted_filename = os.path.join(UPLOAD_FOLDER, filename + ".enc")
        with open(encrypted_filename, 'wb') as f:
            f.write(salt + encrypted)
        encrypted_file = io.BytesIO()
        encrypted_file.write(salt + encrypted)
        encrypted_file.seek(0)
        flash(f"File encrypted successfully! Saved as {filename}.enc in files_example folder", "success")
        return send_file(encrypted_file, as_attachment=True, download_name=filename + ".enc")
    else:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zipf:
            for file in files:
                filename = secure_filename(file.filename)
                data = file.read()
                salt = os.urandom(16)
                key = generate_key(password, salt)
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)
                enc_data = salt + encrypted
                zipf.writestr(filename + ".enc", enc_data)
        zip_buffer.seek(0)
        flash(f"{len(files)} files encrypted successfully! Download the zip archive.", "success")
        return send_file(zip_buffer, as_attachment=True, download_name="encrypted_files.zip", mimetype='application/zip')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    files = request.files.getlist('file')
    password = request.form.get('password')
    if not files or files[0].filename == '':
        flash("No file selected for decryption!", "error")
        return redirect(url_for('encrypt_decrypt'))
    if not password:
        flash("Password is required!", "error")
        return redirect(url_for('encrypt_decrypt'))

    if len(files) == 1:
        file = files[0]
        filename = secure_filename(file.filename)
        data = file.read()
        salt = data[:16]
        encrypted_data = data[16:]
        try:
            key = generate_key(password, salt)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted_data)
        except Exception as e:
            flash("Decryption failed! Incorrect password or corrupted file.", "error")
            return redirect(url_for('encrypt_decrypt'))
        original_filename = filename[:-4] if filename.endswith('.enc') else filename
        decrypted_filename = os.path.join(UPLOAD_FOLDER, original_filename)
        with open(decrypted_filename, 'wb') as f:
            f.write(decrypted)
        decrypted_file = io.BytesIO()
        decrypted_file.write(decrypted)
        decrypted_file.seek(0)
        flash(f"File decrypted successfully! Saved as {original_filename} in files_example folder", "success")
        return send_file(decrypted_file, as_attachment=True, download_name=original_filename)
    else:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zipf:
            for file in files:
                filename = secure_filename(file.filename)
                data = file.read()
                salt = data[:16]
                encrypted_data = data[16:]
                try:
                    key = generate_key(password, salt)
                    fernet = Fernet(key)
                    decrypted = fernet.decrypt(encrypted_data)
                    original_filename = filename[:-4] if filename.endswith('.enc') else filename
                    zipf.writestr(original_filename, decrypted)
                except Exception as e:
                    continue  # skip files that fail to decrypt
        zip_buffer.seek(0)
        flash(f"{len(files)} files decrypted (some may have failed). Download the zip archive.", "success")
        return send_file(zip_buffer, as_attachment=True, download_name="decrypted_files.zip", mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True)
