# Voice and Audio File Based Speech Transcription System

A Python-based Automatic Speech Recognition (ASR) application that converts spoken audio into text. The system supports both microphone input and WAV audio file transcription through a simple graphical user interface.

## Features
- Speech recognition using a microphone
- Transcription of WAV audio files
- Live display of recognized speech
- Export options to save transcriptions as a text file
- Clear utility to reset the current transcription
- Responsive interface built with multi-threading to prevent UI freezing

## Technologies Used
- **Python 3.x**
- **Tkinter** – Graphical User Interface (GUI)
- **SpeechRecognition** – Core speech recognition functionality
- **Threading** – Background execution for asynchronous microphone capturing

## How to Run

### Step 1: Clone the Repository
Clone the repository using Git and navigate to the project directory.
### Step 2: Install Dependencies
Install the required Python packages using:
```bash
pip install -r requirements.txt
```
Alternatively, you can install the core dependencies individually:
```bash
pip install SpeechRecognition 
pip install PyAudio
```
### Step 3: Run the Application
Execute the main script to launch the interface:
```bash
python app.py
```
---

## Usage

### 1. Microphone Recording
1. Click **Start Recording** and speak clearly into your microphone.
2. The application captures the audio streams in a separate thread.
3. Once you stop or processing completes, the text is sent to the API, and the transcription populates the text workspace.
### 2. Audio File Transcription
1. Click **Audio File** to select an existing `*.wav` file from your local computer storage.
2. Choose your file using the file browser dialog window.
3. The application will instantly read, process, and display the extracted speech text inside the application window.
### 3. Saving the Transcription
- Click **Save Text** to write the current transcription into a permanent record.
- The default layout saves the file as: `recognized_text.txt`
### 4. Clearing the Transcription
- Click **Clear** to instantly wipe all text from the display pane and reset the application status bar back to default.

---

## Project Structure
```text
ASR-Tool/
│
├── app.py
├── requirements.txt
├── README.md
└── screenshots/
```

## System Requirements
- Python 3.x environment
- A functional hardware microphone for live voice input
- Installed Speech Recognition library
- Active internet connection required for the Speech Recognition
- PyAudio library extensions bound to your local audio driver