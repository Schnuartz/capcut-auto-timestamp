# 🎬 CapCut Auto Timestamp
This script automates a key video editing step in CapCut by converting blue time markers into ready-to-use timestamps for your YouTube video description.
**CapCut Auto Timestamp** is a Python utility that extracts custom time markers (color `#00c1cd`) from your CapCut projects and formats them as **YouTube-ready chapters**.

It automatically locates your `draft_content.json` project file, converts the internal timestamps to full project timecodes, and generates a ready-to-paste list for your YouTube video description.

---

## 🚀 Features

- 🧠 **Automatic project detection** *(optional)* — detects your currently open CapCut project if [`psutil`](https://pypi.org/project/psutil/) is installed.  
- 💬 **Command line only** — no pop-up windows, everything happens directly in the CMD window.  
- 🕒 **Accurate YouTube chapters** — generates timestamps in `HH:MM:SS - Marker Name` format.  
- 🎞 **Intro marker added automatically** — always includes `00:00:00 - Einleitung` at the top.  
- 🧩 **Portable** — works on any Windows PC with CapCut installed.  
- 💾 **Simple output** — creates a `YouTube_Chapters.txt` file next to the script.

---

## 📦 Installation

### 1️⃣ Clone or download this repository
```bash
git clone https://github.com/<your-username>/capcut-auto-timestamp.git
cd capcut-auto-timestamp
```
### 2️⃣ Install Python (if not installed)
Download from python.org/downloads.

During installation, check “Add Python to PATH”.

### 3️⃣ (Optional) Install psutil for automatic CapCut detection
```bash
pip install psutil
```
If you don’t install it, the script will still run — it will just ask you to type the project name manually.

### 🧰 Usage
▶ Option 1: Run via .bat (recommended)
Double-click the provided file:

```bash
run-capcut-auto-timestamp.bat
```
The CMD window will open:

```bash
🟢 CapCut Auto Timestamp
------------------------
⚠️ psutil not installed → skipping auto-detect.
   To enable this feature later, run:
   pip install psutil
Enter CapCut project name [None]:
```
Type your project name (e.g., HodlHodl Lending) and press ENTER.

▶ Option 2: Run manually in terminal
```bash
python capcut-auto-timestamp.py
```
### 📁 Output
After running, the script creates a file:

```bash
YouTube_Chapters.txt
```
Example content:

```bash
Timecodes:
00:00:00 - Einleitung
00:01:10 - Marker 01
00:02:25 - Marker 02
00:05:09 - Marker 04
...
```
You can now paste this directly into your YouTube video description to create clickable chapter segments.

### 🧠 How It Works
The script:

Finds your CapCut project folder under

```bash
C:\Users\<USERNAME>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\
```
Loads your draft_content.json

Extracts all markers with color #00c1cd

Converts each marker’s internal time into the project’s real timeline time

Outputs the formatted list


### ⚙️ File Structure
```bash
capcut-auto-timestamp/
│
├── capcut-auto-timestamp.py        # Main script
├── run-capcut-auto-timestamp.bat   # Windows launcher
└── README.md                       # Documentation
```
### 🧩 Dependencies
Python ≥ 3.8

(Optional) psutil – for detecting the currently open CapCut project

Install dependencies with:
```bash
pip install psutil
```
