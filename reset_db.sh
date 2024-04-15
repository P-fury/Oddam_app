rm -f charity-donation

python3 manage.py makemigrations
python3 manage.py migrate


#create super user
echo "from user.models import CustomUser; CustomUser.objects.create_superuser('pfury','pskate2@gmail.com', 'passdjango')" | python3 manage.py shell

python3 manage.py seed_data
