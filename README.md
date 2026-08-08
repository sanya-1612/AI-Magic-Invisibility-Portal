<p align="center">
  <img src="screenshots/demo.png" width="850">
</p>

# ✨ AI Magic Invisibility Portal

A real-time AI-powered invisibility portal built using **Python**, **OpenCV**, and **MediaPipe**. The portal follows the user's index finger, dynamically changes size based on finger distance, and reveals the captured background inside the portal to create a magical invisibility effect.

---

## 🚀 Features

- 🪄 Real-time hand tracking using MediaPipe
- 🎯 Portal follows the index finger
- 📏 Dynamic portal size controlled by thumb-index distance
- ✨ Smooth portal movement
- 🌟 Glowing portal effect
- 👻 Real-time invisibility illusion
- ⚡ Fast performance using OpenCV
- 👋 Gesture-based controls

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 📂 Project Structure

```
AI-Magic-Invisibility-Portal/
│
├── main.py
├── portal.py
├── gesture_recognizer.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Magic-Invisibility-Portal.git
```

### 2. Open the project

```bash
cd AI-Magic-Invisibility-Portal
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate it

Windows

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run

```bash
python main.py
```

---

## 📸 Demo

### Magic Portal

> Add screenshots inside the **screenshots** folder.

Example:

```
screenshots/
    portal_demo1.png
    portal_demo2.png
```

---

## 🎯 Future Improvements

- Animated energy portal
- Particle effects
- Multiple portals
- Portal color customization
- Background stabilization

---

## 👩‍💻 Developer

**Sanya Rathore**

GitHub: https://github.com/sanya-1612

---

## 🎮 Controls

### Hand Controls

- **Index finger** — Move portal position
- **Thumb** (distance from index finger) — Adjust portal size

### Keyboard Shortcuts
| Key | Action |
| --- | --- |
| B | Capture/Refresh Background |
| C | Change Portal Shape |
| F | Toggle Fullscreen |
| Q | Quit Application |

### Gesture Controls

Hand gestures provide an additional way to control the portal without the keyboard.

| Gesture | Action |
|---------|--------|
| 👌 **OK Sign** | Capture / Refresh Background |
| ✌️ **Peace Sign** | Toggle Portal Visibility |
| ✊ **Closed Fist** | Pause / Resume Portal |
| 🖐️ **Open Palm** | Reset Portal to Default State |

Gesture recognition uses MediaPipe Hands. Hold each gesture steady for about 1 second for reliable detection. Keyboard shortcuts continue to work alongside gestures.

---

## 📖 Usage

1. **Launch** the application — a background frame is captured automatically.
2. **Move the portal** — point your index finger at the screen.
3. **Resize the portal** — adjust the distance between your index finger and thumb.
4. **Use gestures** — perform the supported gestures to control portal actions without the keyboard.

---

## 💡 Tips

- Good lighting improves gesture detection accuracy.
- Only one hand is tracked at a time.
- Hold gestures briefly for reliable detection.
- Keyboard shortcuts remain available as an alternative.

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
