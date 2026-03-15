python -m venv venv
.\venv\scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

$env:flask_app="run.py"
$env:flask_env="development"

flask db init
flask db migrate -m "crear tablas iniciales"
flask db upgrade
flask run