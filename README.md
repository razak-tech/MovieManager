# 🎬 ReelName

A simple CLI tool to **rename** and **organize** your movie files into folders using a clean format like:  
`Movie Title (Year)` ➜ `Movie Title (Year)/Movie Title (Year).mp4`

---

## 🛠️ Features

- Rename movie files with cleaner names (`Title (Year)`)
- Automatically organize videos and subtitles into folders
- Handles common formats like `.mp4`, `.mkv`, `.srt`, etc.
- Avoids re-renaming already-clean files
- Preview changes before applying

---

## 🚀 How to Use

```bash
# Run the script
python reelname.py
You’ll be asked to choose:

pgsql
Copy
Edit
1️⃣ Rename movies  
2️⃣ Organize into folders  
3️⃣ Rename and Organize  
4️⃣ Exit  
Then provide the full path to your movies folder.

📂 Example
Before:

Copy
Edit
My.Movie.2021.1080p.mkv
My.Movie.2021.srt
After:

java
Copy
Edit
My Movie (2021)/
├── My Movie (2021).mkv
└── My Movie (2021).srt
📦 Supported File Extensions
Video: .mp4, .mkv, .avi, .mov

Subtitles: .srt, .ass, .sub

✅ Requirements
Python 3.6+

pyfiglet module (for the ASCII banner)

Install it with:

bash
Copy
Edit
pip install pyfiglet
🔖 Version
v1.0 – Initial CLI-based version with renaming and organizing

💡 Future Plans
GUI version with drag & drop

Subtitle encoding fixer

Multilingual interface

Dark mode

🧑‍💻 Author
Made with ❤️ by razak-tech
Feel free to contribute, suggest features, or report bugs!
