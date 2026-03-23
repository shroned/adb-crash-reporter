# adb-crash-reporter
Real-time ADB log monitoring tool with UI that detects crashes instantly, supports multi-keyword tracking, and provides alerts with log recording for faster debugging.


# 🚀 Real-Time Crash Reporter with UI & Multi-Keyword Tracking

## 📌 Overview

This project is a **Python-based ADB Log Monitoring Tool** designed to detect crashes in real-time during testing. It notifies users instantly and provides a UI for better usability and control.

---

## ❗ Problem Statement

During test execution, crashes often go unnoticed until log analysis is performed later. This makes it difficult to identify the exact point of failure in the execution flow.

---

## 🎯 Solution

This tool monitors device logs in real-time and alerts the user immediately when a crash or specific keyword is detected.

---

## ✨ Features

* 🔍 Real-time log monitoring using `adb logcat`
* 🔔 Desktop notifications on keyword detection
* 🔊 Sound alert for immediate attention
* 🖥️ User-friendly UI using Tkinter
* 🧠 Supports **multiple keywords** (comma-separated input)
* 📄 Log recording functionality (save full logs to file)
* 🧵 Multi-threaded execution for monitoring & recording

---

## 🛠️ Tech Stack

* Python 3
* ADB (Android Debug Bridge)
* Tkinter (UI)
* Plyer (Notifications)
* Playsound (Audio alerts)
* Threading & Subprocess

---

## ⚙️ Prerequisites

Install required libraries:

```bash
pip install plyer
pip install playsound3
```

Ensure:

* ADB is installed and configured
* Only one device is connected

---

## ▶️ How to Run

```bash
python ui.py
```

---

## 🧑‍💻 Usage

1. Launch the application
2. Enter keywords (comma-separated for multiple tracking)
3. Click **Start Monitoring**
4. (Optional) Enter file name and start recording logs

---

## 📝 Example Keywords

```
crash, exception, fatal
```

---

## ⚠️ Notes

* Ensure only one ADB device is connected
* Keywords can be customized as per testing needs
* Sound file (`warning.mp3`) should be placed in the project directory

---

## 🚀 Future Enhancements

* Export filtered logs
* Regex-based advanced filtering
* UI improvements
* Cross-platform packaging

---

## 🤝 Contribution

Feel free to fork, improve, and raise PRs!

---

## 📣 Motivation

Built to simplify debugging and improve test efficiency by detecting issues *exactly when they occur*.

