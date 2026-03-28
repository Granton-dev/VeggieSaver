# 🥦 VeggieGuard — AI-Powered Vegetable Freshness Detection

> A household-focused real-time vegetable freshness detection system designed to reduce food wastage using computer vision and natural language processing.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Database Models](#database-models)
- [Design System](#design-system)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🌿 Overview

VeggieGuard is a web-based application that helps households detect vegetable spoilage before it happens. Using AI-powered computer vision, users can upload or take a photo of any vegetable and receive an instant freshness analysis — including condition assessment, days remaining, meal suggestions, and storage tips.

The system is designed specifically for **households**, not just farmers. Whether vegetables come from the market, supermarket, or home garden, VeggieGuard helps families reduce food waste and save money.

### The Problem
- 1/3 of all food produced globally is lost or wasted every year
- The average household loses ~$1,500 annually from discarded food
- 45% of fruits and vegetables are lost before they reach the table
- Most spoilage is gradual and preventable with early detection

### The Solution
VeggieGuard provides a **pure software solution** — no expensive IoT hardware required. Just a phone camera and an internet connection.

---

## ✨ Features

### 🔍 Core Features
- **Real-Time Freshness Detection** — Upload or capture a vegetable photo and get instant AI analysis
- **Freshness Scoring** — 0-100 freshness score with color-coded status (Fresh / Good / Caution / Spoiling / Spoiled)
- **Condition Detection** — Identifies issues like wilting, mould, bruising, discolouration, pest damage, disease
- **Days Remaining** — Estimates how many days the vegetable can still be used
- **Meal Suggestions** — AI-generated meal ideas based on current freshness level
- **Storage Tips** — Personalised storage advice to extend vegetable life
- **Warning Signs** — Lists visible spoilage indicators detected in the photo
- **Nutritional Impact** — Explains how freshness level affects nutritional value
- **Household Tips** — Practical advice tailored to household use

### 📊 Analytics & Tracking
- **Scan History** — Full history of all vegetable scans with filtering by freshness status
- **Waste Log** — Track discarded vegetables with reasons (disease, pest, overripe, spoiled, etc.)
- **Analytics Dashboard** — Charts showing waste over time, waste by reason, health distribution, freshness trends
- **Monitor Page** — Overview of all vegetables needing attention

### 🌱 Vegetable Management
- **Plant Catalogue** — 20 pre-loaded vegetables with real images, descriptions and growing tags
- **Add Vegetable** — Add vegetables via file upload, camera capture, or URL
- **Vegetable Detail** — View full vegetable info, AI analysis and scan history
- **Health Status Tracking** — Track plant health (Excellent / Good / Fair / Poor)

### 👤 User Experience
- **Authentication** — Secure registration and login system
- **Responsive Design** — Works on desktop, tablet, and mobile
- **Dark Mode** — Toggle between light and dark themes, persists across sessions
- **PWA Support** — Installable as a mobile app on Android and iOS
- **Smart Tips** — AI-generated household food waste reduction tips
- **Freshness Alerts** — Dashboard alerts for vegetables needing immediate attention
- **Auto-dismiss Messages** — Styled success/error notifications

### 🤖 AI Integration
- **Computer Vision** — Analyses vegetable photos for freshness and condition
- **Natural Language** — Generates human-readable recommendations and meal suggestions
- **Structured Output** — Returns JSON with all analysis fields for reliable display
- **Fallback Handling** — Graceful error handling if AI analysis fails

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **Django 6.0** | Web framework |
| **Python 3.13** | Programming language |
| **SQLite** | Database |
| **Groq API** | AI inference (LLaMA vision model) |
| **Pillow** | Image processing |
| **python-dotenv** | Environment variable management |
| **whitenoise** | Static file serving |
| **django-crispy-forms** | Form rendering |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **Bootstrap 5.3** | CSS framework |
| **Bootstrap Icons** | Icon library |
| **Chart.js** | Analytics charts |
| **Playfair Display** | Serif typography |
| **Outfit / DM Sans** | Body typography |
| **Vanilla JavaScript** | Interactivity |

### AI Models
| Model | Purpose |
|-------|---------|
| **llama-4-scout-17b-16e-instruct** | Vegetable image analysis (vision) |
| **llama-3.3-70b-versatile** | Smart tips generation (text) |

---

## 📁 Project Structure
```
garden_manager/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── db.sqlite3
├── garden_manager/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── garden/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils.py
│   ├── admin.py
│   └── templates/garden/
│       ├── about_veggieguard.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── scan.html
│       ├── scan_result.html
│       ├── scan_history.html
│       ├── add_vegetable.html
│       ├── vegetable_detail.html
│       ├── waste_log.html
│       ├── analytics.html
│       └── monitor.html
├── static/
│   ├── css/
│   │   └── darkmode.css
│   ├── js/
│   │   └── darkmode.js
│   ├── icons/
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   ├── manifest.json
│   └── sw.js
└── media/
    ├── vegetables/
    ├── scans/
    └── veggies/
        ├── tomato.jpeg
        ├── spinach.jpeg
        ├── kale.jpeg
        └── ...
```

---

## 🚀 Installation

### Prerequisites
- Python 3.13+
- pip
- Virtual environment
- Groq API key (free at https://console.groq.com)

### Step 1 — Download the Project
Download and extract the project folder then open a terminal inside the `garden_manager` folder.

### Step 2 — Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get a Free Groq API Key
1. Go to **https://console.groq.com**
2. Sign up with your Google account
3. Click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Copy the key — starts with `gsk_...`

### Step 5 — Create Environment File
```bash
nano .env
```

Add the following:
```
GROQ_API_KEY=gsk_your-key-here
DJANGO_SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
```

Save with `Ctrl+O` then `Ctrl+X`.

### Step 6 — Run Migrations
```bash
python manage.py makemigrations garden
python manage.py migrate
```

### Step 7 — Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 8 — Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 9 — Start the Server
```bash
python manage.py runserver
```

### Step 10 — Open in Browser
Visit **http://127.0.0.1:8000** in your browser.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI analysis | ✅ Yes |
| `DJANGO_SECRET_KEY` | Django secret key | ✅ Yes |
| `DEBUG` | Debug mode True/False | ✅ Yes |

---

## 📱 Usage

### User Flow
```
Landing Page (/)
      ↓
Login (/login/) or Register (/register/)
      ↓
Dashboard (/dashboard/)
      ↓
Scan Vegetable (/scan/) → Upload or Camera Photo
      ↓
AI Analyses Photo (Groq API — LLaMA Vision)
      ↓
Scan Result (/scan/<id>/) → Freshness Score + Recommendations
      ↓
View History (/scan/history/) → Filter by Freshness
      ↓
Log Waste (/waste/) → Track Discarded Vegetables
      ↓
Analytics (/analytics/) → Charts and Trends
```

### URL Reference

| URL | Page | Auth Required |
|-----|------|--------------|
| `/` | About/Landing | No |
| `/login/` | Login | No |
| `/register/` | Register | No |
| `/dashboard/` | Dashboard | Yes |
| `/scan/` | Scan vegetable | Yes |
| `/scan/<id>/` | Scan result | Yes |
| `/scan/history/` | Scan history | Yes |
| `/add/` | Add vegetable | Yes |
| `/vegetable/<id>/` | Vegetable detail | Yes |
| `/waste/` | Waste log | Yes |
| `/analytics/` | Analytics | Yes |
| `/monitor/` | Monitor | Yes |
| `/api/tips/` | AI tips AJAX | Yes |
| `/admin/` | Django admin | Superuser |

---

## 🤖 API Integration

### Vegetable Analysis
```python
from garden.utils import analyze_vegetable_photo

result = analyze_vegetable_photo('/path/to/image.jpeg')
# Returns:
{
    "identified_vegetable": "Spinach",
    "confidence_score": 0.95,
    "freshn

*VeggieGuard — Keeping households fresh, one vegetable at a time. 🥦*
