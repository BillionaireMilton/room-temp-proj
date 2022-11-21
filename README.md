comprehensive blog is here ->> https://blog.teclado.com/first-rest-api-flask-postgresql-python/
first create a  folder for your project
open the project in the text editor or your ide
create a virtual environment on thesame directory of your project i used "python3 -m venv venv"
activate the environment:: source /Users/mintel/StudioProjects/ml_pf/m_cl_learnings/alx_nanodegree_prog/alx-fsd-prog/room-temp-proj/venv/bin/activate 
the above is the rirectory to my project on a mac 
create requirements.txt and add required dependencies, i will update as we continue
first one on the requirements file is "flask"
run "pip install -r requirements.txt" to install the dependency stated on the requirements file
create app.py file (code here)
update requirements with "flask-dotenv" and install 
create .flaskenv file and add required codes (FLASK_APP=app this informs that the app runs from app.py) and (FLASK_DEBUG=True [or 1] this can either be True or 1 and it informs the state of the project either development[debug] or production)
flask-dotenv helps keep your app in debud mode or production mode as suits your mode.
you will be making use of insomnia or postman for all you endpoint testing
also use the elephantsql.com (signUp and create an instance) copy the url 
create .env file and add DATABASE_URL=[paste the url you copied above]
update requirements with "psycopg2-binary" and install [this helps you interract with the database] 
now connect to the database on the app.py
