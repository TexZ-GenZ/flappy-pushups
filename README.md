# Flappy Pushups

A fun twist on the classic Flappy Bird game, controlled by your face movements! This game uses computer vision to track your face position and control the bird's movement.

## 🎮 Features

- Face-controlled gameplay using your webcam
- Classic Flappy Bird mechanics
- Real-time face detection using OpenCV
- Score tracking
- Smooth bird movement following face position

## 🛠️ Technologies Used

- Python 3.x
- Pygame - For game graphics and mechanics
- OpenCV (cv2) - For face detection and tracking
- NumPy - For numerical operations
- Caffe Model - For efficient face detection

## 📋 Prerequisites

- Python 3.7+
- Webcam
- Required Python packages:
  ```
  pygame
  opencv-python
  numpy
  ```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/flappy-pushups.git
   cd flappy-pushups
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install pygame opencv-python numpy
   ```

## 🎯 How to Play

1. Run the game:
   ```bash
   python src/main.py
   ```

2. Position yourself in front of your webcam
3. Move your head up and down to control the bird
4. Avoid the pipes and try to get the highest score!

## 🎛️ Controls

- Move your head up: Bird flies up
- Move your head down: Bird descends
- Press ESC: Exit game
- Press R: Reset game when over

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
