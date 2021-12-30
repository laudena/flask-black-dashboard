# A Mechanical Clock with a Web Interface 
I used this web app generator as a backbone to run cog wheels of a mechanical clock, using a Raspberry-Pi and a stepper motor. 

<img src="https://github.com/laudena/flask-black-dashboard/blob/master/images/Clock.jpg" width="300">
<img src="https://github.com/laudena/flask-black-dashboard/blob/master/images/ClockMechanism.jpg" width="300">
<img src="https://github.com/laudena/flask-black-dashboard/blob/master/images/setup.png" width="300">

---

The working setup Video [Is here](https://youtu.be/lBk1q_Q5vkI)

To set the right time, use the clock web interface and enter the time shown by the clock (current clock's hands position). It will then quickly move the hands to the right position. 

See the setup steps at the end of this file.

---

# [Flask Dashboard Black](https://appseed.us/admin-dashboards/flask-dashboard-black)

**[Flask Dashboard Black](https://appseed.us/admin-dashboards/flask-dashboard-black)** is an open-source seed project generated by AppSeed on top of a modern dark-themed UI. **Black Dashboard** is a beautiful Bootstrap 4 Admin Dashboard with a huge number of components built to fit together and look amazing. It combines colors that are easy on the eye, spacious cards, beautiful typography, and graphics. For newcomers, **Flask** is a lightweight web application framework written in Python that provides a lightweight codebase and libraries that can be easily extended to complex projects. 

<br />

> Features

- Up-to-date [dependencies](./requirements.txt): **Flask 2.0.1**
- [SCSS compilation](#recompile-css) via **Gulp**
- UI: **[Black Dashboard](https://bit.ly/2L0W6Z7)** v1.0.1 provided by *Creative-Tim*
- DBMS: SQLite, PostgreSQL (production) 
- DB Tools: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Modular design with **Blueprints**, simple codebase
- Session-Based authentication (via **flask_login**), Forms validation
- Deployment scripts: Docker, Gunicorn / Nginx, Heroku 
- Support via **Github** and [Discord](https://discord.gg/fZC6hup).

<br />

> Links

- [Flask Dashboard Black](https://appseed.us/admin-dashboards/flask-dashboard-black) - product page
- [Flask Dashboard Black](https://flask-black-dashboard.appseed-srv1.com) - LIVE deployment
- [Flask Dashboard Black](https://docs.appseed.us/products/flask-dashboards/black-dashboard) - product documentation

<br />

## Quick Start in [Docker](https://www.docker.com/)

> Get the code

```bash
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
```

> Start the app in Docker

```bash
$ docker-compose pull   # download dependencies 
$ docker-compose build  # local set up
$ docker-compose up -d  # start the app 
```

Visit `http://localhost:85` in your browser. The app should be up & running.

<br />

![Flask Dashboard - Black Design, dashboard screen.](https://user-images.githubusercontent.com/51070104/140599334-00bd0b9a-b2aa-4163-893a-fedd8c5f1afc.gif)

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
$ # OR with PostgreSQL connector
$ # pip install -r requirements-pgsql.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Code-base structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- routes.py                 # Define app routes
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- routes.py                 # Define authentication routes  
   |    |    |-- models.py                 # Defines models  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |    |    |-- includes/                 # HTML chunks and components
   |    |    |    |-- navigation.html      # Top menu component
   |    |    |    |-- sidebar.html         # Sidebar component
   |    |    |    |-- footer.html          # App Footer
   |    |    |    |-- scripts.html         # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |-- requirements-mysql.txt               # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt               # Production modules  - PostgreSql DMBS
   |
   |-- Dockerfile                           # Deployment
   |-- docker-compose.yml                   # Deployment
   |-- gunicorn-cfg.py                      # Deployment   
   |-- nginx                                # Deployment
   |    |-- appseed-app.conf                # Deployment 
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

> The bootstrap flow

- `run.py` loads the `.env` file
- Initialize the app using the specified profile: *Debug* or *Production*
  - If env.DEBUG is set to *True* the SQLite storage is used
  - If env.DEBUG is set to *False* the specified DB driver is used (MySql, PostgreSQL)
- Call the app factory method `create_app` defined in app/__init__.py
- Redirect the guest users to Login page
- Unlock the pages served by *home* blueprint for authenticated users

<br />

## Recompile CSS

To recompile SCSS files, follow this setup:

<br />

**Step #1** - Install tools

- [NodeJS](https://nodejs.org/en/) 12.x or higher
- [Gulp](https://gulpjs.com/) - globally 
    - `npm install -g gulp-cli`
- [Yarn](https://yarnpkg.com/) (optional) 

<br />

**Step #2** - Change the working directory to `assets` folder

```bash
$ cd apps/static/assets
```

<br />

**Step #3** - Install modules (this will create a classic `node_modules` directory)

```bash
$ npm install
// OR
$ yarn
```

<br />

**Step #4** - Edit & Recompile SCSS files 

```bash
$ gulp scss
```

The generated file is saved in `static/assets/css` directory.

<br />

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/), [Heroku](https://www.heroku.com/), [Gunicorn](https://gunicorn.org/), and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

<br />

### [Heroku](https://www.heroku.com/)
---

Steps to deploy on **Heroku**

- [Create a FREE account](https://signup.heroku.com/) on Heroku platform
- [Install the Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) that match your OS: Mac, Unix or Windows
- Open a terminal window and authenticate via `heroku login` command
- Clone the sources and push the project for LIVE deployment

```bash
$ # Clone the source code:
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
$
$ # Check Heroku CLI is installed
$ heroku -v
heroku/7.25.0 win32-x64 node-v12.13.0 # <-- All good
$
$ # Check Heroku CLI is installed
$ heroku login
$ # this commaond will open a browser window - click the login button (in browser)
$
$ # Create the Heroku project
$ heroku create
$
$ # Trigger the LIVE deploy
$ git push heroku master
$
$ # Open the LIVE app in browser
$ heroku open
```

<br />

### [Gunicorn](https://gunicorn.org/)
---

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

> Install using pip

```bash
$ pip install gunicorn
```
> Start the app using gunicorn binary

```bash
$ gunicorn --bind 0.0.0.0:8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

<br />

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)
---

Waitress (Gunicorn equivalent for Windows) is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones that live in the Python standard library.

> Install using pip

```bash
$ pip install waitress
```
> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

<br />

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The offcial website
- [Boilerplate Code](https://appseed.us/boilerplate-code) - Index provided by **AppSeed**
- [Flask Dashboard Black](https://blog.appseed.us/flask-black-dashboard-update/) - related blog article

<br />

---
**[Flask Dashboard Black](https://appseed.us/admin-dashboards/flask-dashboard-black)** - Provided by **AppSeed** [Web App Generator](https://appseed.us/app-generator).
---


# Mecahnical Clock Raspberry Pi installation ( To do inside the Pi )
To simplify the process (which is another way of saying "let's quickly hack this solution"), I would build the image inside the Rapsberry Pi, where the environment is right and the libraries are available
## Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi
docker version
docker info
```
## Docker-compose
```bash
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
sudo apt-get remove python-configparser
sudo pip3 -v install docker-compose
```
## Craeting the image
```
docker create --privileged --device /dev/gpiomem -v /sys:/sys --restart unless-stopped -p 5005:5005 app_appseed-app:latest
```


TIPS:

### Deploy a desktop version of pi, and config it using a screen and a keyboard
```apt-get update
apt-get upgrade
```
### Copy to remote Pi
```tar -cvf app.tar .
scp app.tar pi@raspberryclock:/home/pi/app
ssh pi@raspberryclock
cd /home/pi
tar -xvf app.tar
```
### docker-compose inside the RPi (to fit the ARM-linux)
```cd app
docker-compose build
```
### setup docker and docker compose
see above

### raspi-config 
enable SPi, ssh, GPIO, etc...
