# 💬 Sakhi – Mental Health Support Chatbot

**Sakhi** is an AI-powered mental health support chatbot that provides a safe space for users to share feelings, chat with an intelligent AI companion, and log their emotional state daily through a mood tracker. Built using **Flask, JavaScript, and MongoDB**, it integrates a **RAG (Retrieval-Augmented Generation)** pipeline to deliver personalized responses.

---

## 📚 Table of Contents

1. [📌 Introduction](#-introduction)
2. [🛠️ Technology Stack & Tools Used](#️-technology-stack--tools-used)
3. [🧪 Methodology](#-methodology)
4. [📅 Weekly Progress Summary](#-weekly-progress-summary)
5. [📊 Results and Analysis](#-results-and-analysis)
6. [🔚 Conclusion](#-conclusion)
7. [🚀 Future Scope](#-future-scope)
8. [⚙️ Local Setup Instructions](#️-local-setup-instructions)
9. [🔗 RAG Model Download](#-rag-model-download)

---

## 📌 Introduction

### Problem Statement
Mental health is often neglected or stigmatized. Many people hesitate to express their feelings or seek professional help. Sakhi bridges this gap by offering an accessible, anonymous AI companion that listens and helps users reflect on their emotional well-being.

### Scope
- Provide users with an AI-powered conversational companion.
- Enable mood tracking with historical logging.
- Offer a user-friendly interface accessible on the web.
- Use MongoDB to store user mood logs.

---

## 🛠️ Technology Stack & Tools Used

| Category      | Technologies |
|---------------|--------------|
| Frontend      | HTML, CSS, JavaScript |
| Backend       | Python (Flask) |
| AI/NLP        | HuggingFace Transformers, SentenceTransformers |
| Database      | MongoDB |
| Auth & Routing| Flask Routes |
| Deployment    | GitHub, Localhost |
| Model Type    | RAG (Retrieval-Augmented Generation) |

---

## 🧪 Methodology

### 👋 Landing Page
- Introduces "Sakhi" and emphasizes the importance of mental health.
- Mentions helpline numbers for real emergencies.
- Prompts users to log in or sign up.

### 🔐 Login/Signup Page
- Basic form for account creation and login.

### 🎯 Choose Page
- User can select between:
  - 🤖 AI Chat with Sakhi
  - 📘 Log Mood

### 💬 Chat Page
- A conversational interface powered by a RAG pipeline.
- Displays a **default welcome message**:  
  _"Hi [User Name]! I am your AI companion Sakhi. I wonder what brought you here today, I’m here to listen to you."_  
- Fetches relevant context using the retriever and generates human-like responses using the language model.

### 😊 Mood Tracker Page
- Users can select a mood (happy, neutral, sad, angry, anxious).
- Upon submission, the mood is saved to MongoDB with a timestamp.
- A table displays all submitted moods.

---

## 📅 Weekly Progress Summary

| Week | Milestones |
|------|------------|
| 1    | Created landing page and login/signup flow |
| 2    | Designed choose/chat/mood pages |
| 3    | Integrated mood tracker UI with backend |
| 4    | Set up MongoDB and stored mood data |
| 5    | Integrated RAG pipeline for AI responses |
| 6    | Styling, testing, and documentation |

---

## 📊 Results and Analysis

- AI responses are contextual and sensitive using RAG.
- Mood logs successfully stored and retrieved from MongoDB.
- Frontend is responsive and user-friendly.
- Functional separation between login, chat, and mood features.

---

## 🔚 Conclusion

The Sakhi chatbot offers a reliable, anonymous, and empathetic platform for users to share their feelings or track moods. It combines artificial intelligence with mental health awareness in a meaningful and impactful way.

---

## 🚀 Future Scope

- Integrate user authentication with hashed passwords.
- Voice input and sentiment detection from speech.
- Graphical dashboard to analyze mood trends over time.
- Escalation to human therapists for serious cases.

---

## ⚙️ Local Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Ayushiisengar/chatbot-for-mental-health-support.git
cd chatbot-for-mental-health-support

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Download and place RAG model folder
#    (See link below and place inside: backend/RAG_Model)

# 5. Run the Flask backend
cd backend
python app.py

# 6. Visit the app in your browser
http://localhost:5000

```


## 🔗 RAG Model Download

📁 **Google Drive Link to RAG_Model Folder**  
👉 [Insert your RAG Model Google Drive link here]  

📂 **After downloading**, place the extracted folder at the following path inside the project: backend/RAG_Model/


---

## 🙋‍♀️ Developed By

**Ayushi Sengar**  
_Marksman Internship Project, 2025_

👨‍🏫 **Mentored by:** [Your Mentor’s Name]

---


