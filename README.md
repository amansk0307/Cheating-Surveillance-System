# 🛡️ AI-Powered Online Proctoring & Surveillance System

An automated, machine learning-driven proctoring system designed to maintain integrity during online assessments. By leveraging real-time computer vision, the system continuously monitors candidate behavior via webcam to detect off-screen visual gaze and unauthorized devices (e.g., mobile phones), automatically capturing timestamped logs and visual evidence upon violation.

---

## 🌟 Key Features

* **Head Pose & Gaze Detection:** Tracks candidate head angles and off-screen visual drift to identify potential cheating.
* **Object & Phone Detection:** Detects physical visual infractions like mobile phone usage in real-time through the webcam feed.
* **Automated Violation Logging:** Generates real-time, precise timestamp logs whenever anomalous behavior is flagged.
* **Visual Evidence Capture:** Automatically captures screenshots upon detecting a policy breach for administrative review.
* **Lightweight & Efficient:** Designed for low latency to run smoothly alongside standard web browsers.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV
* **Machine Learning / Detection:** YOLO V12
* **Data Processing:** NumPy

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* A working webcam

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/amansk0307/Cheating-Surveillance-System.git](https://github.com/amansk0307/Cheating-Surveillance-System.git)
   cd Cheating-Surveillance-System
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the program:**
   ```bash
   python main.py
## 📂 Output & Logs
When a policy violation is triggered:
* **Screenshots:** Stored in logs/ labeled with date and time.
