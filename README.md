#Universal Grade Monitoring System
##Overview
An automated web-scraping agent designed to monitor Student Information Systems (OBS) for academic updates. It utilizes a headless browser architecture to detect changes in records and dispatches instant alerts via Discord or Telegram. The modular design allows for easy adaptation across different university platforms.

##Technical Architecture
Automation: Powered by Playwright for high-performance interaction with dynamic web interfaces.

Process Management: Orchestrated by PM2 to ensure 24/7 uptime and automated recovery.

Cloud Infrastructure: Optimized for Linux-based Virtual Machines (GCP/AWS) with minimal resource footprints.

Security Layer: Implements a decoupled configuration model via environment variables to ensure credential isolation.

##Installation and Configuration
Prerequisites
Python 3.8+

Linux Environment (Ubuntu 22.04 recommended)

Playwright & Dependencies

##Setup
1. Clone and Install:
git clone https://github.com/UKT-glitch/grade-notifier.git
cd grade-notifier
pip install -r requirements.txt
python3 -m playwright install chromium
sudo python3 -m playwright install-deps
2. Environment Setup:
Create a .env file from the provided .env.example:
OBS_USER=your_id
OBS_PASS=your_password
DISCORD_WEBHOOK=your_url
3. Deployment
pm2 start monitor.py --name "grade-monitor" --interpreter python3

##Security & Adaptation
Data Privacy: Credential management is strictly isolated through .gitignore to prevent PII leakage.

Rate Limiting: Execution cycles are optimized to ensure compliance with server request policies.

Modularity: Target URLs and CSS selectors can be updated within monitor.py to support various SIS architectures.
