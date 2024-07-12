import cv2
import torch
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import Image, ImageTk
import json
import os

class ConfigWindow:
    def __init__(self, parent, config, save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuration")
        self.window.geometry("400x500")
        self.config = config
        self.save_callback = save_callback

        style = ttk.Style(self.window)
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Model selection
        ttk.Label(frame, text="Model:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=self.config['model'])
        model_combo = ttk.Combobox(frame, textvariable=self.model_var, values=['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt'])
        model_combo.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        # Confidence threshold
        ttk.Label(frame, text="Confidence Threshold:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.conf_var = tk.DoubleVar(value=self.config['confidence_threshold'])
        conf_slider = ttk.Scale(frame, from_=0, to=1, orient='horizontal', variable=self.conf_var)
        conf_slider.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        # Frame rate
        ttk.Label(frame, text="Frame Rate:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.fps_var = tk.IntVar(value=self.config['fps'])
        fps_spinbox = ttk.Spinbox(frame, from_=1, to=60, textvariable=self.fps_var)
        fps_spinbox.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        # Box color
        ttk.Label(frame, text="Box Color:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar(value=self.config['box_color'])
        color_button = ttk.Button(frame, text="Choose Color", command=self.choose_color)
        color_button.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

        # Save button
        save_button = ttk.Button(frame, text="Save Configuration", command=self.save_config)
        save_button.grid(column=0, row=4, columnspan=2, pady=20)

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_var.get())[1]
        if color:
            self.color_var.set(color)

    def save_config(self):
        new_config = {
            'model': self.model_var.get(),
            'confidence_threshold': self.conf_var.get(),
            'fps': self.fps_var.get(),
            'box_color': self.color_var.get()
        }
        self.save_callback(new_config)
        self.window.destroy()

class ObjectDetector:
    def __init__(self, window_title):
        self.window = tk.Tk()
        self.window.title(window_title)
        self.window.geometry("800x600")

        self.style = ttk.Style(self.window)
        self.style.theme_use('clam')

        self.load_config()
        self.create_widgets()

        self.model = YOLO(self.config['model'])
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.is_still_image = False

        self.update()
        self.window.mainloop()

    def load_config(self):
        default_config = {
            'model': 'yolov8n.pt',
            'confidence_threshold': 0.5,
            'fps': 30,
            'box_color': '#00FF00'
        }
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config

    def save_config(self, new_config):
        self.config = new_config
        with open('config.json', 'w') as f:
            json.dump(self.config, f)
        self.model = YOLO(self.config['model'])

    def create_widgets(self):
        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(self.frame, width=640, height=480, bg='black')
        self.canvas.grid(column=0, row=0, columnspan=3)

        self.label = ttk.Label(self.frame, text="Detected: Nothing")
        self.label.grid(column=0, row=1, columnspan=3, pady=10)

        self.capture_button = ttk.Button(self.frame, text="Capture Still Image", command=self.capture_still)
        self.capture_button.grid(column=0, row=2, pady=10)

        self.config_button = ttk.Button(self.frame, text="Configuration", command=self.open_config)
        self.config_button.grid(column=1, row=2, pady=10)

        self.quit_button = ttk.Button(self.frame, text="Quit", command=self.window.quit)
        self.quit_button.grid(column=2, row=2, pady=10)

    def open_config(self):
        ConfigWindow(self.window, self.config, self.save_config)

    def capture_still(self):
        self.is_still_image = True

    def update(self):
        if not self.is_still_image:
            ret, frame = self.cap.read()
        else:
            ret = True

        if ret:
            results = self.model(frame, conf=self.config['confidence_threshold'])

            filtered_detections = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = self.model.names[cls]
                    filtered_detections.append((label, float(conf), (int(x1), int(y1), int(x2), int(y2))))

            for label, conf, (x1, y1, x2, y2) in filtered_detections:
                cv2.rectangle(frame, (x1, y1), (x2, y2), tuple(int(self.config['box_color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), 2)
                cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, tuple(int(self.config['box_color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), 2)

            if filtered_detections:
                detected_text = ", ".join([f"{label} ({conf:.2f})" for label, conf, _ in filtered_detections[:3]])
                self.label.config(text=f"Detected: {detected_text}")
            else:
                self.label.config(text="Detected: Nothing")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo

        self.is_still_image = False
        self.window.after(int(1000 / self.config['fps']), self.update)

if __name__ == "__main__":
    ObjectDetector("YOLOv8 Object Detector")
