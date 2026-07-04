# YouTube Notifier

A simple, lightweight Python script that monitors specified YouTube channels for recent uploads (e.g., within the last few hours) and sends email notifications when new videos are found.

It parses the raw HTML of the YouTube channel's `/videos` page, extracts the latest video, and checks if it was uploaded recently. If a new video is detected, it emails a link to the video to you using Gmail's SMTP server.

---

## ⚡ Quick Start: Deploy with GitHub Actions (Recommended)

You can run this notifier **100% free** and without a local server using **GitHub Actions**. It will run automatically on GitHub's servers on an hourly schedule.

### Step 1: Create a Private GitHub Repository
1. Create a **private** repository on GitHub (to keep your configuration and logs private).
2. Push this project folder to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Configure Repository Secrets
To keep your email credentials secure, do **not** upload a `.env` file to GitHub. Instead, configure repository secrets:
1. In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
2. Click **New repository secret** and add the following three secrets:
   - `CHANNELS`: A comma-separated list of YouTube channels (e.g., `https://www.youtube.com/@StuffMadeHere/videos,https://www.youtube.com/@simonegiertz/videos`).
   - `EMAIL`: Your Gmail address.
   - `APP_PASSWORD`: Your 16-character Gmail App Password.
     > **How to get a Gmail App Password:**
     > 1. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
     > 2. Enable **2-Step Verification** if it isn't already.
     > 3. Go to **2-Step Verification** details, scroll to the bottom, and select **App passwords**.
     > 4. Generate a new password (e.g., name it "YouTube Notifier") and copy the 16-character password (without spaces).

### Step 3: Run & Schedule
- **Automated:** The workflow in [.github/workflows/check_youtube.yml](file:///.github/workflows/check_youtube.yml) is set to run automatically at the start of every hour.
- **Manual Trigger:** You can trigger the script manually at any time by going to the **Actions** tab in your repository, selecting **Check YouTube Uploads**, and clicking **Run workflow**.

---

## 💻 Alternative: Local Setup & Automation

If you prefer to run the script locally on your own computer or server:

### 1. Installation
1. Navigate to the project directory:
   ```bash
   cd YoutubeNotifier
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Configuration
1. Copy the example configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and enter your `channels`, `email`, and `app_password` details (see the Gmail App Password instructions above).

### 3. Execution
- **Run manually:**
  ```bash
  python main.py
  ```
- **Automate with Cron (Linux/macOS):**
  Open your crontab editor (`crontab -e`) and add an hourly rule:
  ```cron
  0 * * * * /path/to/YoutubeNotifier/venv/bin/python /path/to/YoutubeNotifier/main.py >> /path/to/YoutubeNotifier/cron.log 2>&1
  ```

---

## 🔍 How It Works

1. **Loads Settings:** The script reads configurations from the environment variables (either local `.env` or GitHub Secrets).
2. **Scrapes YouTube:** It fetches the public `/videos` page of each channel to download the raw HTML. **No YouTube API Key is needed.**
3. **Parses Upload Time:** It locates the latest video ID and parses the relative upload text.
4. **Checks Recency:** If it finds the keyword `"hour"` (e.g., "3 hours ago"), it identifies it as a recent upload.
5. **Emails Link:** It opens a secure connection to Gmail's SMTP server (`smtp.gmail.com` on port 465) and emails you a direct link.
