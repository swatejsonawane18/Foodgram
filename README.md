# Follow the below instructions to execute the app

env_site contains the virtual environment.
foodgram folder contains the backend setup.
frontend folder contains the frontend setup.
requirements.txt contains all the dependencies that need to be used.

Execute the code - 

Backend setup - 
1. Activate the virtual environment.
2. Go to the backend folder -> cd foodgram
3. Run this command to populate the data -> python manage.py populate_data
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver

Frontend Setup - 
1. Activate the virtual environment.
2. Go to the frontend folder -> cd frontend
3. Run this command to install dependencies -> npm install
4. Start the react app -> npm start
