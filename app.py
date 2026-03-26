import os
import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from detector import TrafficAnalyzer


class CarColorDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Colour Detection and Traffic Analyzer")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f0f0")

        os.makedirs("output", exist_ok=True)

        # Model
        self.analyzer = TrafficAnalyzer("yolov8n.pt")

        # State
        self.cap = None
        self.running = False
        self.current_frame = None
        self.processed_frame = None
        self.video_thread = None

        # GUI
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(
            self.root,
            text="Car Colour Detection + Car Counting + People Counting",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a1a"
        )
        title.pack(pady=10)

        # Button frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Upload Image", font=("Arial", 12),
                  bg="#4CAF50", fg="white", width=15,
                  command=self.load_image).grid(row=0, column=0, padx=8)

        tk.Button(btn_frame, text="Upload Video", font=("Arial", 12),
                  bg="#2196F3", fg="white", width=15,
                  command=self.load_video).grid(row=0, column=1, padx=8)

        tk.Button(btn_frame, text="Start Webcam", font=("Arial", 12),
                  bg="#FF9800", fg="white", width=15,
                  command=self.start_webcam).grid(row=0, column=2, padx=8)

        tk.Button(btn_frame, text="Stop", font=("Arial", 12),
                  bg="#F44336", fg="white", width=15,
                  command=self.stop_video).grid(row=0, column=3, padx=8)

        tk.Button(btn_frame, text="Save Output", font=("Arial", 12),
                  bg="#9C27B0", fg="white", width=15,
                  command=self.save_output).grid(row=0, column=4, padx=8)

        # Preview frame
        preview_frame = tk.Frame(self.root, bg="#f0f0f0")
        preview_frame.pack(pady=10, fill="both", expand=True)

        # Original image panel
        left_frame = tk.Frame(preview_frame, bg="white", bd=2, relief="solid")
        left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        tk.Label(left_frame, text="Input Preview", font=("Arial", 16, "bold"),
                 bg="white").pack(pady=10)

        self.input_label = tk.Label(left_frame, bg="white")
        self.input_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Processed image panel
        right_frame = tk.Frame(preview_frame, bg="white", bd=2, relief="solid")
        right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        tk.Label(right_frame, text="Processed Output", font=("Arial", 16, "bold"),
                 bg="white").pack(pady=10)

        self.output_label = tk.Label(right_frame, bg="white")
        self.output_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=10)

        self.total_cars_var = tk.StringVar(value="Total Cars: 0")
        self.blue_cars_var = tk.StringVar(value="Blue Cars: 0")
        self.other_cars_var = tk.StringVar(value="Other Cars: 0")
        self.people_var = tk.StringVar(value="People Count: 0")

        stat_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#f0f0f0",
            "fg": "#222"
        }

        tk.Label(stats_frame, textvariable=self.total_cars_var, **stat_style).grid(row=0, column=0, padx=20)
        tk.Label(stats_frame, textvariable=self.blue_cars_var, **stat_style).grid(row=0, column=1, padx=20)
        tk.Label(stats_frame, textvariable=self.other_cars_var, **stat_style).grid(row=0, column=2, padx=20)
        tk.Label(stats_frame, textvariable=self.people_var, **stat_style).grid(row=0, column=3, padx=20)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(self.root, textvariable=self.status_var,
                                font=("Arial", 12), bg="#333", fg="white", anchor="w")
        status_label.pack(side="bottom", fill="x")

    def update_stats(self, stats):
        self.total_cars_var.set(f"Total Cars: {stats['total_cars']}")
        self.blue_cars_var.set(f"Blue Cars: {stats['blue_cars']}")
        self.other_cars_var.set(f"Other Cars: {stats['other_cars']}")
        self.people_var.set(f"People Count: {stats['people']}")

    def display_image(self, frame, label_widget, max_size=(600, 500)):
        if frame is None:
            return

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)

        # Resize to fit
        pil_img.thumbnail(max_size)

        tk_img = ImageTk.PhotoImage(pil_img)
        label_widget.configure(image=tk_img)
        label_widget.image = tk_img

    def load_image(self):
        self.stop_video()

        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if not file_path:
            return

        self.status_var.set(f"Loading image: {os.path.basename(file_path)}")

        frame = cv2.imread(file_path)
        if frame is None:
            messagebox.showerror("Error", "Could not read image.")
            return

        self.current_frame = frame.copy()

        processed, stats = self.analyzer.process_frame(frame)
        self.processed_frame = processed.copy()

        self.display_image(self.current_frame, self.input_label)
        self.display_image(self.processed_frame, self.output_label)
        self.update_stats(stats)

        self.status_var.set("Image processed successfully.")

    def load_video(self):
        self.stop_video()

        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )

        if not file_path:
            return

        self.cap = cv2.VideoCapture(file_path)

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open video.")
            return

        self.running = True
        self.status_var.set(f"Playing video: {os.path.basename(file_path)}")

        self.video_thread = threading.Thread(target=self.process_video_stream, daemon=True)
        self.video_thread.start()

    def start_webcam(self):
        self.stop_video()

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not access webcam.")
            return

        self.running = True
        self.status_var.set("Webcam started.")

        self.video_thread = threading.Thread(target=self.process_video_stream, daemon=True)
        self.video_thread.start()

    def process_video_stream(self):
        while self.running and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.current_frame = frame.copy()

            processed, stats = self.analyzer.process_frame(frame)
            self.processed_frame = processed.copy()

            # Update GUI in main thread
            self.root.after(0, self.display_image, self.current_frame, self.input_label)
            self.root.after(0, self.display_image, self.processed_frame, self.output_label)
            self.root.after(0, self.update_stats, stats)

            # Small delay for smooth playback
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

        self.stop_video()

    def stop_video(self):
        self.running = False

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.status_var.set("Stopped.")

    def save_output(self):
        if self.processed_frame is None:
            messagebox.showwarning("Warning", "No processed output available to save.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Output Image",
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")]
        )

        if not save_path:
            return

        cv2.imwrite(save_path, self.processed_frame)
        self.status_var.set(f"Saved output to: {save_path}")
        messagebox.showinfo("Success", f"Output saved successfully:\n{save_path}")

    def on_close(self):
        self.stop_video()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarColorDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()