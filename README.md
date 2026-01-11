# 🚀 GraspIQ AI Assistant

**GraspIQ AI Assistant** is a full-stack, AI-powered placement and career guidance chatbot built using **Flask**, **SambaNova (DeepSeek / LLaMA models)**, and a **modern responsive UI**.
It provides **company-specific placement guidance**, **career counseling**, **technical interview preparation**, and **real-time AI chat** for students.

---
## Website Preview
<img width="679" height="473" alt="image" src="https://github.com/user-attachments/assets/588b4347-3af2-4bd4-a359-cb039d1c3096" />

---
## 🌟 Features

### 🤖 AI-Powered Chatbot

* Real-time conversational AI using **SambaNova Cloud**
* Supports **DeepSeek-V3.1-Terminus**, **LLaMA 3.1 / 3.2**
* Automatic **fallback to local knowledge base** if API is unavailable

### 🎯 Placement & Career Guidance

* Company-specific preparation (FAANG, Indian IT, startups, consulting)
* Resume & LinkedIn optimization advice
* Technical interview strategies (DSA, System Design)
* Soft skills & HR interview guidance

### 📚 GraspIQ Platform Support

* Login & registration help
* Course & program details
* Support and contact information
* About GraspIQ platform

### ⚡ Performance & UX

* Instant responses (<1s)
* Typing indicators & animations
* Responsive UI (Mobile, Tablet, Desktop)
* Dark mode support
* Streaming responses (SSE supported)

---

## 🛠 Tech Stack

### Backend

* **Flask 2.3**
* **Flask-CORS**
* **Python-dotenv**
* **OpenAI SDK (SambaNova compatible)**
* **Gunicorn (Production Server)**

### AI Models

* **DeepSeek-V3.1-Terminus** (Primary)
* **LLaMA 3.1 / 3.2 Instruct**
* Local enhanced knowledge base fallback

### Frontend

* HTML5 + CSS3 (Custom UI)
* Vanilla JavaScript
* Font Awesome Icons
* Google Fonts (Inter, Poppins)
* Animate.css

---

## 📂 Project Structure

```
GraspIQ-AI-Assistant/
│
├── app.py                  # Main Flask backend
├── generate_secret.py      # Generates secure Flask secret keys
├── requirements.txt        # Python dependencies
│
├── templates/
│   └── index.html          # Frontend UI
│
├── static/
│   ├── style.css           # UI & responsive styling
│   └── favicon.ico
│
├── .env.example            # Environment variable template
└── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/graspiq-ai-assistant.git
cd graspiq-ai-assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
FLASK_SECRET_KEY=your_secure_key_here
SAMBA_API_KEY=your_sambanova_api_key
DEBUG=True
PORT=5000
```

Generate a secure secret key:

```bash
python generate_secret.py
```

---

## ▶️ Running the Application

### Development Mode

```bash
python app.py
```

### Production Mode (Recommended)

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

Visit:

```
https://graspiq-chatbot-1.onrender.com/
```

---

## 🔌 API Endpoints

| Endpoint          | Method | Description            |
| ----------------- | ------ | ---------------------- |
| `/`               | GET    | Main UI                |
| `/chat`           | POST   | Chat response          |
| `/stream`         | POST   | Streaming AI responses |
| `/suggestions`    | GET    | Quick questions        |
| `/health`         | GET    | System health          |
| `/api-status`     | GET    | AI provider status     |
| `/models`         | GET    | Available AI models    |
| `/test-sambanova` | GET    | Test AI connectivity   |

---

## 🧠 Intelligent Fallback System

* ✅ Uses **SambaNova AI** when API is available
* ⚠️ Automatically switches to **local enhanced knowledge base** if API fails
* No downtime for users

---

## 🔐 Security & Best Practices

* Environment-based secrets
* Secure Flask session handling
* CORS enabled safely
* API health monitoring
* Production-ready logging

---

## 🌐 Deployment Ready

* Works perfectly on **Render**, **Railway**, **AWS**, **GCP**, **Azure**
* Gunicorn-based production setup
* Stateless & scalable

---

## 📸 UI Preview

> Modern, professional dashboard with:

* AI status indicators
* Quick access links
* Animated chat interface
* Placement-focused UX

---

## 📬 Support

* **Website:** [https://graspiq.in](https://graspiq.in)
* **Email:** [support@graspiq.in](mailto:support@graspiq.in)
* **Instagram:** [https://www.instagram.com/_graspiq](https://www.instagram.com/_graspiq)_

---

## 📄 License

This project is licensed under the **MIT License**.
Feel free to use, modify, and distribute with attribution.

---

## ⭐ Acknowledgements

* **SambaNova Systems**
* **DeepSeek AI**
* **Meta LLaMA**
* **Flask Community**

---
