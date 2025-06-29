# 🔐 Secure File Encryption System

A robust, web-based file encryption and decryption application built with Flask and modern cryptography standards. This application provides secure AES-256 encryption for files with password-based key derivation, featuring a beautiful and intuitive user interface.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Cryptography](https://img.shields.io/badge/Cryptography-41.0.3-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🔒 **Advanced Security**
- **AES-256 Encryption**: Industry-standard symmetric encryption
- **PBKDF2 Key Derivation**: Secure password-based key generation with 100,000 iterations
- **Salt Generation**: Unique salt for each file to prevent rainbow table attacks
- **Fernet Implementation**: Authenticated encryption with built-in integrity verification

### 📁 **File Management**
- **Single File Encryption/Decryption**: Process individual files securely
- **Batch Processing**: Encrypt/decrypt multiple files simultaneously
- **ZIP Archive Support**: Automatic ZIP creation for multiple files
- **File Type Agnostic**: Works with any file type (documents, images, videos, etc.)

### 🎨 **Modern User Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Bootstrap 5**: Modern, clean, and professional styling
- **Interactive Elements**: Smooth animations and hover effects
- **Real-time Feedback**: Success/error messages with flash notifications
- **Drag & Drop Support**: Intuitive file upload interface

### 🚀 **Performance & Reliability**
- **Memory Efficient**: Streams files without loading entire contents into memory
- **Error Handling**: Graceful handling of corrupted files and wrong passwords
- **Cross-platform**: Works on Windows, macOS, and Linux
- **No Database Required**: Lightweight and easy to deploy

## 📋 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [Security Details](#-security-details)
- [API Endpoints](#-api-endpoints)
- [File Structure](#-file-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/file_safety_using_AES_Password.git
   cd file_safety_using_AES_Password
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## 🎯 Usage

### Encryption Process

1. **Navigate to the application**
   - Open your browser and go to `http://localhost:5000`
   - Click "Get Started" or navigate to the encryption page

2. **Select files**
   - Choose single or multiple files to encrypt
   - Supported formats: Any file type (documents, images, videos, etc.)

3. **Set password**
   - Enter a strong password (minimum 8 characters recommended)
   - This password will be used to derive the encryption key

4. **Encrypt files**
   - Click "Encrypt Files" button
   - The application will process your files and provide download links
   - Encrypted files are saved with `.enc` extension

### Decryption Process

1. **Upload encrypted files**
   - Select the `.enc` files you want to decrypt
   - You can process multiple files simultaneously

2. **Enter password**
   - Use the same password that was used for encryption
   - The system will verify the password and decrypt the files

3. **Download decrypted files**
   - Decrypted files will be available for download
   - Original filenames are preserved (without `.enc` extension)

### Security Best Practices

- **Use strong passwords**: Combine uppercase, lowercase, numbers, and special characters
- **Keep passwords secure**: Store passwords in a password manager
- **Backup encrypted files**: Keep multiple copies of important encrypted files
- **Regular updates**: Keep the application and dependencies updated

## 🔐 Security Details

### Cryptographic Implementation

The application uses industry-standard cryptographic practices:

```python
# Key Derivation (PBKDF2)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,                    # 256-bit key
    salt=salt,                    # Random 16-byte salt
    iterations=100_000,           # High iteration count
    backend=default_backend()
)

# Encryption (Fernet/AES-256)
fernet = Fernet(key)
encrypted = fernet.encrypt(data)
```

### Security Features

- **AES-256**: Military-grade encryption algorithm
- **PBKDF2**: Password-based key derivation with 100,000 iterations
- **Random Salt**: 16-byte random salt per file prevents rainbow table attacks
- **Authenticated Encryption**: Fernet provides both confidentiality and integrity
- **Secure File Handling**: Files are processed securely without leaving traces

### File Format

Encrypted files follow this structure:
```
[16-byte salt][encrypted data]
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with application overview |
| `/encrypt-decrypt` | GET | File encryption/decryption interface |
| `/encrypt` | POST | Encrypt uploaded files |
| `/decrypt` | POST | Decrypt uploaded files |

### Request Parameters

**Encryption:**
- `file`: File(s) to encrypt (multipart/form-data)
- `password`: Encryption password (form data)

**Decryption:**
- `file`: Encrypted file(s) to decrypt (multipart/form-data)
- `password`: Decryption password (form data)

## 📁 File Structure

```
file_safety_using_AES_Password/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── crypto ppt.pdf        # Documentation (if any)
├── files_example/        # Directory for processed files
└── templates/
    ├── index.html        # Home page template
    └── encrypt_decrypt.html  # Encryption/decryption interface
```

## ⚙️ Configuration

### Environment Variables

You can customize the application behavior by setting environment variables:

```bash
# Flask configuration
export FLASK_ENV=production
export FLASK_DEBUG=False

# Application settings
export UPLOAD_FOLDER=./secure_files
export MAX_FILE_SIZE=100MB
```

### Application Settings

Key configuration options in `app.py`:

```python
# Secret key for session management
app.secret_key = 'your-secret-key-here'

# Upload folder for processed files
UPLOAD_FOLDER = 'files_example'

# PBKDF2 iterations (higher = more secure but slower)
iterations = 100_000
```

## 🔧 Troubleshooting

### Common Issues

**1. "No file selected" error**
- Ensure you've selected at least one file before submitting
- Check that the file size is within acceptable limits

**2. "Decryption failed" error**
- Verify you're using the correct password
- Ensure the file wasn't corrupted during transfer
- Check that the file has the `.enc` extension

**3. "Module not found" error**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python environment

**4. Port already in use**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using the current port

### Performance Optimization

- **Large files**: The application handles large files efficiently through streaming
- **Multiple files**: Batch processing is optimized for multiple files
- **Memory usage**: Files are processed in chunks to minimize memory consumption

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests if applicable
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask**: Web framework for Python
- **Cryptography**: Python cryptography library
- **Bootstrap**: Frontend framework for responsive design
- **Font Awesome**: Icon library

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the maintainers** for urgent security issues

---

**⚠️ Security Notice**: This application is designed for educational and personal use. For production environments, consider additional security measures such as HTTPS, rate limiting, and proper session management.

**🔒 Remember**: Always keep your encryption passwords secure and never share them. The security of your encrypted files depends entirely on the strength and secrecy of your passwords. 