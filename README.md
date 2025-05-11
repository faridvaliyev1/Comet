# Comet 🚀

A data-centric application for processing and managing analytics pipelines.

## 📋 Prerequisites

1. **Python 3.8+**  
2. **PostgreSQL**  
   - Install on your local machine:  
     - **macOS (Homebrew)**  
       brew install postgresql  
       brew services start postgresql  
     - **Ubuntu / Debian**  
       sudo apt update  
       sudo apt install postgresql postgresql-contrib  
       sudo systemctl start postgresql  
     - **Windows**  
       Download and install from https://www.postgresql.org/download/windows/  

3. **Git** (to clone the repo)

## 🔧 Installation

1. **Clone the repository**  
   git clone https://github.com/faridvaliyev1/Comet.git  
   cd Comet

2. **Create and activate a virtual environment**  
   python -m venv venv  
   source venv/bin/activate    # macOS/Linux  
   venv\Scripts\activate       # Windows

3. **Install Python dependencies**  
   pip install --upgrade pip  
   pip install -r requirements.txt

## 🗄️ PostgreSQL Setup

1. **Create a database user & database**  
   sudo -u postgres psql  
   -- inside psql shell:  
   CREATE USER comet_user WITH PASSWORD 'your_password';  
   CREATE DATABASE comet_db OWNER comet_user;  
   \q

2. **Configure connection**  
   Copy `Datacentric/config.example.yaml` → `Datacentric/config.yaml` and update:

   db:  
     host: "localhost"  
     port: 5432  
     name: "comet_db"  
     user: "comet_user"  
     password: "your_password"  

   input_path: "data/input/"  
   output_path: "data/output/"  
   log_level: "INFO"

## ▶️ Running the Application

From the project root:

   cd Datacentric  
   python main.py

This will:  
1. Read `config.yaml`.  
2. Connect to your local Postgres instance.  
3. Execute the data pipeline.

## 🛠️ Common Commands

- Reinstall dependencies:  
  pip install --force-reinstall -r requirements.txt

- Run in detached Python session (e.g. screen/tmux):  
  screen -S comet-session  
  python main.py

- Create a new branch:  
  git checkout -b feature/your-feature

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Contact

Maintained by [Farid Valiyev](https://github.com/faridvaliyev1).  
Feel free to open an issue or submit a pull request!
