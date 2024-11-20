import vlc
import yt_dlp as ytdlp
import tkinter as tk
import time

# Define your static list of YouTube video URLs
video_urls = [
    "https://youtu.be/oPmioNr4d48?si=LA3SJXG38FVykUSs",
    "https://youtu.be/VrYDBjHZy1g?si=Q3nqvO_ccnq9qqMA",
    "https://youtu.be/2ZM3VYMYWFE?si=-yVsXSI37FNeH-Gj"
]

class YouTubePlayer:
    def __init__(self, root):
        self.root = root
        self.current_index = 0  # Track the current video index
        self.player = vlc.MediaPlayer()

        # Initialize GUI
        self.setup_gui()
        self.play_video()

    def setup_gui(self):
        # Create a frame for the video and buttons
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for the video player
        self.video_canvas = tk.Canvas(self.main_frame, bg="black", width=640, height=360)
        self.video_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create a frame for navigation buttons
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(side=tk.RIGHT, padx=10)

        # Add Back and Next buttons
        self.back_button = tk.Button(self.controls_frame, text="Back", command=self.back_video)
        self.back_button.pack(side=tk.TOP, pady=10)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_video)
        self.next_button.pack(side=tk.TOP, pady=10)

        # Set up VLC player to render in the tkinter canvas
        self.player.set_hwnd(self.video_canvas.winfo_id())  # Windows; use set_xwindow for Linux, set_nsobject for macOS

    def get_video_stream_url(self, video_url):
        ydl_opts = {
            'format': 'best',  # Retrieve the best combined stream (audio + video)
            'quiet': True,
        }
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(video_url, download=False)
                return info_dict.get('url', None)
            except Exception as e:
                print(f"Error retrieving video URL for {video_url}: {e}")
                return None

    def play_video(self):
        # Get the current video URL
        url = video_urls[self.current_index]
        print(f"Now playing: {url}")

        # Stop current media before switching
        if self.player.is_playing():
            self.player.stop()

        # Get the video stream URL
        video_url = self.get_video_stream_url(url)
        if not video_url:
            print(f"Skipping {url} due to missing video URL.")
            return  # Skip this video if video URL is not available

        # Set media and play
        media = vlc.Media(video_url)
        self.player.set_media(media)
        self.player.play()
        print(f"Started playing: {url}")

    def next_video(self):
        # Move to the next video in the list, looping back if at the end
        self.current_index = (self.current_index + 1) % len(video_urls)
        self.play_video()

    def back_video(self):
        # Move to the previous video in the list, looping back if at the start
        self.current_index = (self.current_index - 1) % len(video_urls)
        self.play_video()

# Set up tkinter window to display VLC player
root = tk.Tk()
root.title("YouTube VLC Player")
root.geometry("800x450")  # Set the overall window size

# Run the YouTube player
app = YouTubePlayer(root)
root.mainloop()
