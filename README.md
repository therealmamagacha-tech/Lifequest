# 🛡️ LIFEQUEST: Operations Agent
> **System CORE_OS v1.0.4** — Gamify your daily life in a Cyberpunk universe.[cite: 6]

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🌌 Project Overview
**LIFEQUEST** is a web application developed for the **Grizzly Hacks III** hackathon.[cite: 6]
The concept is to transform your daily chores and objectives into top-secret infiltration missions.[cite: 6, 8] By leveraging AI to analyze your successes and an ultra-stylized CSS interface, LIFEQUEST turns productivity into a true espionage RPG.[cite: 6, 9]

### ✨ Key Features
*   **Immersive Cyberpunk Interface**: A neon-themed design utilizing *Orbitron* and *Share Tech Mono* fonts for a high-tech terminal feel.[cite: 9]
*   **AI Contract System**: Integration with **Google Gemini** to analyze proof of completion via image scanning and validate mission integrity.[cite: 6]
*   **Agent Progression**: Earn XP, increase your rank (LVL_), and unlock exclusive achievement badges in your Hall of Fame.[cite: 6, 8]
*   **Multilingual Support**: The entire interface is available in both French and English.[cite: 4, 6]
*   **Security**: A robust authentication system using PBKDF2 hashing to protect operator data and access codes.[cite: 5]

## 🛠️ Technical Installation

### Prerequisites
*   Python 3.9 or higher.
*   A Google Gemini API Key (available via Google AI Studio).

### Local Setup
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/lifequest-grizzly.git](https://github.com/YOUR_USERNAME/lifequest-grizzly.git)
    cd lifequest-grizzly
    ```

2.  **Install dependencies**:
    *(Create a requirements.txt file with: streamlit, google-generativeai, python-dotenv)*
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    Create a `.env` file at the root of the project and add your API key:[cite: 2, 3]
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Launch the Application**:
    ```bash
    streamlit run app.py
    ```

## 🚀 Built With
*   **Frontend**: Streamlit (Python) with heavy custom CSS injection for the "HUD" atmosphere and animated backgrounds.[cite: 4, 9]
*   **Artificial Intelligence**: Google Generative AI (Gemini) for intelligent task verification and contract generation.[cite: 6]
*   **Icons**: Lucide Icons rendered dynamically via the Iconify API.[cite: 7]
*   **Storage**: A local JSON-based system for agent data persistence and session management.[cite: 5]

## 🎭 The Team
Developed for the **Grizzly Hacks III** competition.

---
*“Terminal locked. Awaiting operator input...”*[cite: 6]
