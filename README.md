### Kirill Melanich test task for STARNAVI
# Social Network
This API allows an authorized user to create posts, like and dislike them. Also, it has bot_script that imitates users activity according to the rules defined in config.py file 

### Main rules

- Only authorized user can perform activity on this app 
- User can like or dislike any post multiple time
- User can delete or update only his own post
- User activity calculates automatically
- Bot generates posts and likes randomly according to config rules
- You can see the number of likes given for the period you are interested in by endpoint activity. Just enter the start and end date of the period into the form and click post

## Technologies used
- Django
- Django Rest Framework
- JWT authentication
- Faker
- Drf-spectacular
- Debug Toolbar

## Installation 
1. Clone the repository:
   ```shell
   git clone https://github.com/KirillMelanich/Social_Network
   
2. Navigate to the project directory and activate virtual environment:
   ```shell
   cd social_network
   python -m venv venv
   venv\Scripts\activate (on Windows)
   source venv/bin/activate (on macOS)

3. Install dependencies:
   ```shell
    pip install -r requirements.txt

4. Use `.env_sample` file as a template and create `.env` file with your settings
    . Don't forget to change your database settings for your local database

5. Run migrations
   ```shell
   python manage.py makemigrations
   python manage.py migrate

6. Create superuser
   ```shell
   python manage.py createsuperuser
 
7. Run server:
   ```shell
   python manage.py runserver
   
8. Run bot_script
    ```shell
   python bot_script.py
   
9. Enjoy Social Network! 
