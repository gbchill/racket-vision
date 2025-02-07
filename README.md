# Tennis Shot Analysis Project

This project is an AI-powered tool designed to analyze tennis shots, particularly focusing on the forehand stroke. It utilizes computer vision techniques, including MediaPipe, to process video footage and extract key insights about player performance.

## Features

- **Forehand Analysis:** Uses AI to analyze forehand shots, detecting speed, angle, and form.
- **Backend Processing:** A Flask-based backend processes video input and extracts shot data.
- **User Interface:** Displays analysis results in an easy-to-understand format.
- **Data Insights:** Provides feedback on shot consistency and improvement areas.

---

## Prerequisites

### 1. Install Python 3.10.12

MediaPipe does not support Python 3.11 or later, so ensure you have Python 3.10 installed.

#### Check Python Version

```bash
python3 --version
```

Expected output:

```
Python 3.10.12
```

If you have a different version, install Python 3.10.12 using one of the following methods:

#### Using `pyenv` (Recommended)

```bash
brew install pyenv  # Install pyenv
pyenv install 3.10.12
pyenv global 3.10.12
```

Then restart your shell:

```bash
exec zsh  # For macOS/Linux using Zsh
```

#### Using Homebrew (Alternative)

```bash
brew install python@3.10
```

Then update your `PATH`:

```bash
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd tennis-shot-analysis
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

(For Windows, use `venv\Scripts\activate` instead.)

### 3. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Install MediaPipe

```bash
pip install mediapipe --no-cache-dir
```

If the above fails, try:

```bash
pip install git+https://github.com/google/mediapipe.git
```

### 5. Run the Backend Server

Navigate to the backend folder and start the server:

```bash
cd backend
flask run
```

By default, the server runs on `http://127.0.0.1:5000/`.

To run on a specific port:

```bash
flask run --host=0.0.0.0 --port=5001
```

### 6. Run the Frontend

Navigate to the frontend folder and start the application:

```bash
cd ../frontend
npm install  # Install dependencies
npm start  # Start the frontend development server
```

By default, the frontend runs on `http://localhost:3000/`.

---

### Frontend Not Running

If the frontend does not start, try:

```bash
cd frontend
npm install  # Ensure all dependencies are installed
npm start  # Start the frontend again
```

---

This README provides full instructions to set up and run the Tennis Shot Analysis project, covering backend processing, AI-powered forehand shot analysis, and frontend deployment.
