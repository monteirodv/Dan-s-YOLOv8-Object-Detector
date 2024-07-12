# 🖼️ YOLOv8 Object Detector

Welcome to the **YOLOv8 Object Detector** project! This application utilizes YOLOv8 for real-time object detection with a user-friendly GUI built using **Tkinter**.

## ✨ Features

- **Real-Time Object Detection**: Capture video feed from your webcam and detect objects in real time.
- **Customizable Settings**: Easily adjust model parameters, confidence thresholds, frame rate, and bounding box color.
- **Capture Still Images**: Take snapshots of the detected objects.

## 🛠️ Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/YOLOv8-Object-Detector.git
   cd YOLOv8-Object-Detector
   ```

2. **Install Dependencies**

   Ensure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLOv8 Models**

   Download the YOLOv8 models you wish to use (e.g., `yolov8n.pt`, `yolov8s.pt`, `yolov8m.pt`) from the official YOLOv8 GitHub repository.

## 🚀 Usage

1. **Run the Application**

   ```bash
   python object_detector.py
   ```

2. **Interact with the GUI**
   - **Capture Still Image**: Click the "Capture Still Image" button to take a snapshot.
   - **Configuration**: Click the "Configuration" button to open the settings window where you can adjust:
     - Model
     - Confidence Threshold
     - Frame Rate
     - Box Color
   - **Quit**: Click the "Quit" button to exit the application.

## ⚙️ Configuration

Configuration settings are stored in a `config.json` file. You can manually edit this file or use the in-app configuration window to adjust settings. Here is an example of the `config.json` file:

```json
{
  "model": "yolov8n.pt",
  "confidence_threshold": 0.5,
  "fps": 30,
  "box_color": "#00FF00"
}
```

## 📁 Code Structure

- `object_detector.py`: Main script that initializes the GUI and handles the detection logic.
- `config_window.py`: Contains the `ConfigWindow` class for the configuration GUI.
- `requirements.txt`: List of Python dependencies.

## 📦 Dependencies

- **OpenCV**: For video capture and image processing.
- **Torch**: Deep learning framework.
- **Ultralytics YOLO**: Pretrained YOLO models.
- **Tkinter**: GUI framework.
- **Pillow**: Image handling.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
