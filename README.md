# Applicant Tracking System (ATS)

A robust, full-featured Applicant Tracking System built with Django 6.0, designed to streamline recruitment processes for HR teams and Recruiters.

## 🚀 Features

### For Recruiters
- **Dashboard:** At-a-glance view of active jobs and recent applicants.
- **Job Management:** Create, edit, and delete job postings with rich details (salary in LKR, requirements, etc.).
- **Applicant Management:**
    - View all applicants filtered by job and status.
    - Detailed profile view with resume preview (PDF text extraction).
    - **🤖 AI Analysis:** Integrated **Gemini AI** to analyze CVs against job descriptions automatically.
    - **Duplicate Prevention:** System prevents the same candidate from applying multiple times to the same job.
    - Status tracking (Screening, Interview, Hired, Rejected).
    - Add private notes to candidate profiles.

### For Candidates
- **Simple Application:** Streamlined process to apply for open positions.
- **Validation:** Real-time feedback if applying to the same job twice.
- **Security:** Recruiters cannot apply to their own job postings.

---

## 🛠 Tech Stack

- **Backend:** Python 3.14, Django 6.0
- **Database:** SQLite (Development), PostgreSQL-ready (Production using `dj-database-url`)
- **Frontend:** Django Templates, Bootstrap 5.3.2 (CDN), Bootstrap Icons
- **AI Integration:** Google Gemini 1.5 Flash (via `google-generativeai`)
- **Utilities:** `PyPDF2` (Resume parsing), `Pillow` (Image handling)

---

## 🏗 Design Decisions

### 1. Robust Duplicate Prevention
We implemented a multi-layered approach to prevent duplicate applications:
- **Frontend/View Layer:** Checks for existing email or phone numbers for the specific job before processing.
- **Database Layer:** Enforced `unique_together = [['applied_job', 'email'], ['applied_job', 'phone']]` constraints in the `Applicant` model. This ensures database-level integrity.
- **Recruiter Exclusion:** explicit check prevents job owners from applying to their own postings to maintain data validity.

### 2. AI-Powered Insights
Instead of generic keyword matching, we integrated **Gemini AI**.
- **On-Demand Analysis:** To respect API limits and quotas, analysis is triggered manually by the recruiter ("Analyze with AI" button) rather than running automatically.
- **Privacy:** Resume text is extracted locally using `PyPDF2` and sent to the API ephemerally; files are not stored on Google servers.

### 3. Session-Based Rate Limiting
To prevent spam, we implemented a session-based rate limit:
- A user can only submit one application every **5 minutes**.
- This is tracked via `request.session` timestamps, providing a lightweight but effective barrier against automated spam without needing heavy Redis infrastructure for this scale.

### 4. UI/UX Choices
- **Bootstrap 5:** Chosen for rapid, responsive UI development.
- **Single Page Filter Persistence:** Applicant filtering uses JavaScript to maintain state without complex URL parameter parsing in Django templates, simplifying the backend logic.

---

## 📝 Assumptions

1.  **Resume Format:** The system currently assumes resumes are primarily in **PDF format** for text extraction features. Other formats are accepted but won't trigger the text preview or AI analysis.
2.  **Single Recruiter:** The current permission model assumes that the user creating the job is the primary "owner". While others can view, the owner has specific rights (like not being able to apply).
3.  **Currency:** Salary defaults to **LKR (Sri Lankan Rupee)** based on regional requirements.
4.  **Timezone:** Configured for **Asia/Colombo** for accurate timestamping of activities.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.14+
- Google Gemini API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ATS
    ```

2.  **Install dependencies:**
    ```bash
    uv sync  # or pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    GEMINI_API_KEY=your-gemini-api-key
    ```

4.  **Run Migrations:**
    ```bash
    uv run manage.py migrate
    ```

5.  **Start Server:**
    ```bash
    uv run manage.py runserver
    ```

6.  Access the app at `http://127.0.0.1:8000`

---

## 📄 License
[MIT License](LICENSE)
