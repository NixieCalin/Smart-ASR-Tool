import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
import threading


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
root.title("Smart Speech-to-Text ASR Tool")
root.geometry("700x500")

tk.Label(
    root,
    text="Smart Speech-to-Text ASR Tool",
    font=("Arial", 20, "bold")
).pack(pady=20)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 11)
)
status_label.pack(pady=10)

text_box = tk.Text(
    root,
    height=15,
    width=75,
    font=("Arial", 12),
    wrap=tk.WORD
)
text_box.pack(padx=20, pady=10, fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)
record_button = tk.Button(
    button_frame,
    text="🎤 Start Recording",
    command=start_recording,
    width=18
)
record_button.grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="📁 Audio File",
    command=recognize_audio_file,
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Save Text",
    command=save_text,
    width=15
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_text,
    width=12
).grid(row=0, column=3, padx=5)
root.mainloop()