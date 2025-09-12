# Beauty Salon - Wagtail CMS

A modern beauty salon website built with Wagtail CMS and Bootstrap Pulse theme.

## 🚀 First-Time Setup

```bash
# 1. Clone and enter project
git clone <repository-url>
cd beauty_salon

# 2. Create and activate virtual environment
python -m venv beauty_venv
beauty_venv\Scripts\activate          # Windows (Command Prompt/PowerShell)
source beauty_venv/bin/activate       # macOS/Linux/WSL

# 3. Install dependencies and setup database
pip install -r requirements.txt
python manage.py migrate

# 4. Create admin user (follow prompts)
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

**Visit:**
- Website: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`

## 📁 What's Included vs Excluded

### ✅ **Committed to Git:**
- Python source code (`.py` files)
- Templates (`.html` files)  
- Static assets (CSS, JS, images in `static/` folders)
- Configuration files (`settings.py`, `urls.py`, etc.)
- Requirements file (`requirements.txt`)
- Documentation (`README.md`)

### ❌ **NOT Committed to Git:**
- **Database file** (`db.sqlite3`) - Each developer gets a fresh database
- **Media uploads** (`media/` folder) - User-uploaded images
- **Virtual environment** (`beauty_venv/` folder) - Created locally
- **Cache/compiled files** (`__pycache__/`, `*.pyc`)
- **IDE settings** (`.vscode/`, `.idea/`)
- **Environment variables** (`.env` files)

## 🖼️ About Media Files (Images)

- Images are stored in `media/` folder and **included in Git** 
- Upload images through admin panel at `http://localhost:8000/admin`
- All team members automatically get the same images when pulling changes

## 🔄 Daily Workflow

### **Getting Latest Changes:**
```bash
git pull origin main
pip install -r requirements.txt    # Update dependencies
python manage.py migrate           # Apply database changes
python manage.py runserver         # Start working
```

### **Making Changes:**
```bash
# After modifying models
python manage.py makemigrations
python manage.py migrate

# After uploading images through admin
git add media/
git commit -m "Added new beauty salon images"
```

## 📦 Project Structure
```
beauty_salon/
├── beauty_salon/          # Main project settings
│   ├── settings/         # Environment-specific settings
│   ├── templates/        # Base templates
│   └── static/          # Global static files
├── home/                 # Homepage app
│   ├── models.py        # Page models and blocks
│   ├── templates/       # App-specific templates
│   └── static/         # App-specific static files
├── media/              # User uploads (not in Git)
├── beauty_venv/        # Virtual environment (not in Git)
├── db.sqlite3          # Database (not in Git)
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 🎯 Key Features
- **Wagtail CMS** for content management
- **Bootstrap Pulse theme** for styling
- **StreamField blocks** for flexible content
- **Image handling** with automatic resizing
- **Responsive design** for all devices

## 🛠️ Common Commands
```bash
python manage.py runserver          # Start development server
python manage.py makemigrations     # After changing models
python manage.py migrate            # Apply database changes
python manage.py createsuperuser    # Create new admin user
```
