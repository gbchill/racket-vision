# RacketVision

RacketVision is an AI-powered tennis coaching and analysis platform designed to help players improve their forehand shot. By leveraging advanced computer vision and pose estimation, the system extracts key body landmarks from user-uploaded videos and compares them to those from professionally executed forehands. This comparison produces actionable feedback, enabling players to understand and correct flaws in their technique.

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

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd racket-vision
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv #mac0s/Linux



#Activate
source venv/bin/activate  # macOS/Linux

.\venv\Scripts\Activate.ps1 #Windows


```

(For Windows, use `venv\Scripts\activate` instead.)

### 3. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3.1. Generate or Update the requirements.txt File

After installing or updating your project dependencies, generate an updated requirements.txt file with the following command:

```bash
pip freeze > requirements.txt
```

This command captures all installed packages and their versions, ensuring your dependency list remains current. Remember to commit any changes to this file.

### 5. Run the Backend Server

Navigate to the backend folder and start the server:

```bash
cd backend
cd app
fastapi dev main.py
```

### 6. Run the Frontend

Navigate to the frontend folder and start the application:

```bash
cd ../frontend
npm install  # Install dependencies
npm run dev
```

Visit http://localhost:3000 to view your application.

Random stuff:
rafce
