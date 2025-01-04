echo "Realizando makemigrations..."
python manage.py makemigrations

echo "Realizando migrações..."
python manage.py migrate

echo "Iniciando o servidor..."
python manage.py runserver
