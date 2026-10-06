# AI Study Planner

AI Study Planner is a complete Streamlit-based academic planning application designed for B.Tech students. It helps students manage subjects, tasks, assignments, study sessions, and upcoming exams with a personalized, AI-inspired study plan.

## Project description

This application helps students:

- plan daily and weekly study schedules
- prioritize difficult subjects and high-impact deadlines
- organize assignments and exam preparation
- track progress and study consistency
- receive personalized recommendations using a local fallback engine
- work even when no external AI API key is configured

## Features

- Student profile management
- Subject tracking with difficulty, preparation, target percentage, and exam dates
- Personalized AI study planner with priority scoring
- Study task and assignment manager
- Dashboard with progress metrics and score
- AI assistant for academic questions and planning advice
- Progress analytics and charts
- Local recommendation engine without API dependency
- SQLite database with SQLAlchemy
- Modern academic dashboard interface

## Technology stack

- Python 3.12
- Streamlit
- SQLAlchemy
- SQLite
- pandas
- plotly
- numpy
- python-dotenv
- sentence-transformers
- ChromaDB

## Project architecture

- app.py: main Streamlit entry point
- database/: models, database session, CRUD operations
- ai/: planning logic and recommendation engine
- services/: scheduler, progress, analytics logic
- utils/: validation and helper utilities
- pages/: modular Streamlit pages for app sections
- data/: SQLite database storage

## Installation steps

### 1. Python 3.12 setup

Install Python 3.12 and ensure it is available in PATH.

### 2. Create a virtual environment

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Environment variable setup

Create a .env file in the project root using the example file:

```powershell
Copy-Item .env.example .env
```

Then edit .env and set your API key if you want to use an external provider:

```env
AI_API_KEY=your_api_key_here
```

If no key is present, the application will automatically switch to the built-in local recommendation engine.

## How to run

In PowerShell:

```powershell
.venv\Scripts\activate
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## How to use

1. Launch the app.
2. Create your profile.
3. Add your subjects.
4. Add exam dates and assignment deadlines.
5. Generate an AI study plan.
6. Manage tasks and track progress.
7. Use the AI assistant for personalized advice.
8. Review analytics and update your plan as needed.

## Database information

The app uses SQLite with SQLAlchemy. All core tables are created automatically when the app starts.

Tables include:

- students
- subjects
- tasks
- assignments
- study_sessions
- study_plans

The database file is stored in the data folder.

## AI functionality

The application works without an API key. If no AI_API_KEY is configured, it falls back to local rule-based recommendations generated from:

- exam dates
- subject difficulty
- preparation gap
- target percentages
- pending tasks
- available study hours

This ensures the app remains fully functional for student use without external services.

## Screenshots

Add screenshots here later for a project demo.

## Future enhancements

- Add user authentication
- Add multi-user support
- Add calendar export
- Add more advanced AI provider support
- Add notification reminders
- Add CSV data export

## Troubleshooting

### Streamlit does not start

Check that your virtual environment is activated and dependencies are installed.

### Module import errors

Make sure you are running from the project root and the package structure is intact.

### SQLite database errors

Delete the existing database file in the data folder and restart the app if you want to reset data.

### AI features not working

No API key is required. The system falls back to local recommendation logic automatically.

## Windows VS Code setup

1. Open the project folder in VS Code.
2. Select the Python interpreter from the .venv environment.
3. Open a terminal in VS Code.
4. Run the commands shown in the installation section.
5. Start the app with `streamlit run app.py`.

## Project command summary

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```
