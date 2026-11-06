# 🔴 Camera-Based Optical Stylus

A Python-based optical stylus system that uses a camera to detect the red light emitted from a pen tip and translates its position into real-time mouse cursor movement on a computer screen.

The project uses computer vision to track the pen tip, calculate its coordinates, and map them to the screen, allowing the pen to function as an input device.

## 🚀 Features

- **Real-Time Tracking:** Detects and tracks the red light emitted by the stylus.
- **Computer Vision:** Uses OpenCV for image processing and color detection.
- **Mouse Control:** Converts detected pen coordinates into mouse cursor movement.
- **Coordinate Mapping:** Maps camera coordinates to screen coordinates.
- **Low-Cost Implementation:** Uses a standard camera and a simple light-emitting stylus.

## ⚙️ How It Works

The system follows a simple computer vision pipeline:

1. **Video Capture:** Captures live video using a webcam.
2. **Color Detection:** Processes each frame to identify the red light using HSV color filtering.
3. **Position Detection:** Calculates the center coordinates of the detected red light.
4. **Coordinate Mapping:** Converts camera coordinates into corresponding screen coordinates.
5. **Mouse Movement:** Sends the mapped coordinates to the operating system to control the mouse cursor.

## 🛠️ Technologies Used

- Python
- OpenCV
- NumPy
- PyAutoGUI

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install Dependencies

```bash
pip install opencv-python numpy pyautogui
```

### 3. Run the Project

```bash
python main.py
```

*Make sure your camera is connected and the red-light stylus is visible to the camera.*

## 🔧 Hardware Requirements

- A webcam or compatible camera.
- A stylus or pen equipped with a red light source.
- A computer running Python.
- A monitor or display.

## 📸 Project Demonstration

Add screenshots, videos, or GIFs demonstrating the tracking system here.

## 🗺️ Future Improvements

- Perspective correction and four-point screen calibration.
- Improved tracking stability using Kalman filtering.
- Click and drag functionality.
- Gesture-based interaction.
- Reduced processing latency.
- Multi-display support.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!

Feel free to fork this repository, make changes, and submit a pull request.

**Developed with Python and OpenCV.**
