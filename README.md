# djangoLogin

# In this Application User will register him/herself and give the range of IP address
# On the login time It will check if the IP address is in range or not. If yes, Then the user can login
# If Success full Login count for each day reached the limit 100, then next time user can't login
# The checking ip method (checkApiLimit in 'coomon/views.py') can be used as api also as it is sending json response


# For starting the project please check if python is installed or not, Here it's using 3.11.0
# Check the requirements.txt file for used packages

# create virtual environment by running the command: python -m venv env
# activating the env: .\env\Scripts\Activate
# Executing the migration (Needed if any changes to models.py file): python manage.py makemigrations
# Migrating the migrations: python manage.py migrate
# Installing the required packages: pip install -r requirements.txt
# running the server: python manage.py runserver