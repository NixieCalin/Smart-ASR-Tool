import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
import threading

# UI Theme
BG_COLOR = "#F3F0FA"
PANEL_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#7656C9"
PRIMARY_HOVER = "#6344B5"
ACCENT_COLOR = "#E6E0F2"
ACCENT_HOVER = "#D8CEEA"
TEXT_COLOR = "#332D45"
MUTED_TEXT = "#77708A"
SUCCESS_COLOR = "#4F9878"
ERROR_COLOR = "#C45D7A"

def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:
        status_label.config(text="Listening...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)

        status_label.config(text="Recognizing...")

        text = recognizer.recognize_google(audio)

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, text)

        status_label.config(text="Speech recognized successfully.")

    except sr.UnknownValueError:
        status_label.config(text="Could not understand speech.")
        messagebox.showwarning(
            "Recognition Error",
            "Could not understand the speech."
        )

    except sr.WaitTimeoutError:
        status_label.config(text="No speech detected.")

    except sr.RequestError:
        status_label.config(text="Speech service unavailable.")
        messagebox.showerror(
            "Connection Error",
            "Could not connect to the speech recognition service."
        )

    except Exception as e:
        status_label.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))

    finally:
        record_button.config(state=tk.NORMAL)


def start_recording():
    record_button.config(state=tk.DISABLED)

    threading.Thread(
        target=recognize_speech,
        daemon=True
    ).start()
def recognize_audio_file():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("WAV Audio", "*.wav")]
    )

    if not file_path:
        return

    recognizer = sr.Recognizer()

    try:
        status_label.config(text="Processing audio file...")

        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, text)

        status_label.config(
            text="Audio file converted successfully."
        )

    except sr.UnknownValueError:
        status_label.config(text="Could not understand audio.")
        messagebox.showwarning(
            "Recognition Error",
            "Could not understand the audio."
        )

    except sr.RequestError:
        status_label.config(text="Speech service unavailable.")
        messagebox.showerror(
            "Connection Error",
            "Could not connect to the speech recognition service."
        )

    except Exception as e:
        status_label.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))


def save_text():
    text = text_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Empty Text", "There is no text to save.")
        return

    with open("recognized_text.txt", "w", encoding="utf-8") as file:
        file.write(text)

    messagebox.showinfo("Saved", "Text saved successfully.")


def clear_text():
    text_box.delete("1.0", tk.END)
    status_label.config(text="Ready")

# Main window
root = tk.Tk()
root.title("Smart Speech-to-Text Transcription App")
root.geometry("760x640")
root.minsize(680, 560)
root.configure(bg=BG_COLOR)

tk.Label(
    root,
    text="Smart Speech Transcription ASR Tool",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(pady=(28, 4))

tk.Label(
    root,
    text="Turn your speech and audio into text",
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg=MUTED_TEXT
).pack(pady=(0, 14))

status_label = tk.Label(
    root,
    text="Ready",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=MUTED_TEXT
)
status_label.pack(pady=(0, 12))

text_box = tk.Text(
    root,
    height=10,
    font=("Segoe UI", 13),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR,
    insertbackground=PRIMARY_COLOR,
    selectbackground=ACCENT_COLOR,
    selectforeground=TEXT_COLOR,
    relief="flat",
    borderwidth=0,
    wrap=tk.WORD,
    padx=18,
    pady=16,
    highlightthickness=1,
    highlightbackground="#E1E4ED",
    highlightcolor=PRIMARY_COLOR
)
text_box.pack(
    padx=32,
    pady=(0, 18),
    fill="both",
    expand=True
)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=(0, 28))

def style_button(button, *, primary=False, width=15):
    button.configure(
        width=width,
        font=("Segoe UI", 10, "bold" if primary else "normal"),
        bg=PRIMARY_COLOR if primary else ACCENT_COLOR,
        fg="#FFFFFF" if primary else TEXT_COLOR,
        activebackground=PRIMARY_HOVER if primary else ACCENT_HOVER,
        activeforeground="#FFFFFF" if primary else TEXT_COLOR,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=8,
        pady=10
    )

record_button = tk.Button(
    button_frame,
    text="🎤  Start Recording",
    command=start_recording
)
style_button(record_button, primary=True, width=19)
record_button.grid(row=0, column=0, padx=6)

audio_button = tk.Button(
    button_frame,
    text="📁  Audio File",
    command=recognize_audio_file
)
style_button(audio_button, width=15)
audio_button.grid(row=0, column=1, padx=6)

save_button = tk.Button(
    button_frame,
    text="Save Text",
    command=save_text
)
style_button(save_button, width=13)
save_button.grid(row=0, column=2, padx=6)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_text
)
style_button(clear_button, width=10)
clear_button.grid(row=0, column=3, padx=6)

root.mainloop()