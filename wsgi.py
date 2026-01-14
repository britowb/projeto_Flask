#########################################################
#### Web Server Gateway Interface configuration file ####
#### Used to run the Flask application               ####
#### with a WSGI server like Gunicorn or uWSGI       ####
#########################################################
from app import create_app

app = create_app('development')

if __name__ == "__main__":
    app.run(debug=True)