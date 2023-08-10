import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
import threading

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")

        self.label = tk.Label(root, text="Enter YouTube URL:")
        self.label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.quality_label = tk.Label(root, text="Select Quality:")
        self.quality_label.pack()

        self.quality_combobox = ttk.Combobox(root, values=["Highest", "720p", "480p", "360p", "Audio"])
        self.quality_combobox.set("Highest")
        self.quality_combobox.pack()

        self.destination_label = tk.Label(root, text="Select Destination:")
        self.destination_label.pack()

        self.destination_button = tk.Button(root, text="Browse", command=self.select_destination)
        self.destination_button.pack()

        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.pack()

        self.destination_path = ""

    def select_destination(self):
        self.destination_path = filedialog.askdirectory()
        if self.destination_path:
            messagebox.showinfo("Success", f"Destination selected: {self.destination_path}")
        else:
            messagebox.showerror("Error", "No destination selected.")

    def start_download(self):
        url = self.url_entry.get()
        quality = self.quality_combobox.get()

        try:
            yt = YouTube(url)

            if quality == "Highest":
                video = yt.streams.get_highest_resolution()
            elif quality == "720p":
                video = yt.streams.get_by_resolution("720p")
            elif quality == "480p":
                video = yt.streams.get_by_resolution("480p")
            elif quality == "360p":
                video = yt.streams.get_by_resolution("360p")
            elif quality == "Audio":
                video = yt.streams.filter(only_audio=True).first()
            else:
                messagebox.showerror("Error", "Invalid quality selection.")
                return

            t = threading.Thread(target=self.download_video, args=(video,))
            t.start()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def download_video(self, video):
        try:
            file_extension = video.mime_type.split("/")[-1]
            filename = f"{video.title}.{file_extension}"
            video.download(output_path=self.destination_path, filename=filename)
            messagebox.showinfo("Success", "Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
