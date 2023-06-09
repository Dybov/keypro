# Initial task
## Applicant code test assignment
### Task
Make a (Geo)Django application for creating and moving point objects on map. For DB you might want to use PostGIS (PostgreSQL) or SQLite. For frontend you might want to use Leaflet or OpenLayers (they are supported by majority of frontend frameworks – ReactJS, Vue, Angular – though framework usage is not mandated, you can do it even in javascript or using jQuery). You are not limited in the tools or components you are using.

### Implementation
Backend: The Django application has been built with minimal additional requirements, without using Django REST Framework (DRF) as it would be too heavy for this size project.
Frontend: Leaflet and JavaScript are used for the frontend. ReactJS, Vue, and Angular are not mandatory and considered too heavy for building this app.

## Application basic functionality
### Task
Application user main screen is map. User should be able to scroll the map (extent of the map is not important), to create point on a map by clicking on map pane, update positions of points he created by dragging them.

### Implementation
The main screen ('/') features a scrollable map. Users have the ability to create a point on the map by clicking on the desired location and then clicking the "create" button in a popup. When a point is dragged, its position is updated, and a popup appears at the end of the drag operation, prompting the user to choose whether to save or cancel the changes. Clicking on a point brings up a popup with a delete button for removing the point.

## Application advanced (optional) functionality
### Task
User should be able to see points other users created in one style (in example color or shape) and 
points he created in other style.

User should not be able to move points created by other users. When user closes the browser window and then opens it again, he should be able to continue creating and moving his points application (if no specific measure to delete data about user in browser is done).

Admin site should exist where admins see all the points, delete any of it or change its owner and coordinates. Points in admin should be able to be filtered by its creator. Also admins should be able to see user info with number of points they created and edit it. Admins should be able to assign other users admin rights. Admins should be able to delete users, in such case points should stay.

### Implementation
In the application, the user's points are displayed in green, while points created by other users are shown in gray. Users are only able to move or delete points that they own, and cannot modify points owned by other users.

All changes made by the user persist even after reopening the browser, allowing them to continue editing from where they left off.

The admin site is built using Django's admin site, which provides access for managing users (utilizing Django's built-in user management features) as well as managing points. In the admin site, administrators have the ability to create, delete, change the position, and update the owner of points. Deleting a user does not remove their associated points, which remain in the system.

## Project basic functionality
### Task
Project should be supplied in some code repository. Project should have instructions on installing and running it.

### Implementation
The project is hosted in a GitHub repository. Below are instructions for installing and running the project in development mode. Please note that configuring the project for production is not within the scope of the task.

## Project advanced (optional) functionality
### Task
Project should have some tests, preferably in frontend and backend. Project should have docstrings for code used in it. 
Application should be packaged in Docker to be able to run on windows or linux hosts. You might want to run nginx or some other web server to serve static content and some application server like gunicorn or uwsgi (or some other wsgi or asgi server) to run Django though it is not mandatory.

### Implementation
The project does not include any tests as it was not developed using a Test-Driven Development (TDD) approach, and time constraints prevented their implementation.

The project documentation is written using reStructuredText docstrings, both in Python and JavaScript files. These docstrings provide information about the code's functionality, usage, and any important considerations.

To enhance portability, the application is packaged in a Docker container, allowing it to be run on both Windows and Linux hosts. The use of Nginx and ASGI/WSGI is not necessary for running the application in a development environment. The production configuration has not been implemented.

Please ensure that you have Docker installed on your machine and follow the provided instructions to run the project locally.


# Installation and running

By default app would be running on 8000 port of localhost, so ensure it's open or change port in the commands

## Using docker
* in project directory run `docker compose up`
    first time it takes a lot of time to download images and build, then it
    takes time to initialize DB, so app won't start, but it gives base for
    next steps. (implementation of starting app only when DB will be ready is
    not necessary because much time it takes only once)
* After previous command build and run apps (django shows error, while DB will
    be configuring, so the orientir would be message that database system is
    ready to accept connections), do not close it, and in another
    terminal/command line run command in the project folder run next commands:
* `docker compose exec backend python geodjango/manage.py migrate`
* `docker compose exec backend python geodjango/manage.py createsuperuser`
    and answer prompts
* Then kill docker compose (Ctrl/command + C)
* And start it again `docker compose up`

Other times just run `docker compose up` (or with `-d` flag to detach)

## Manually
* Install Python3.8+ (out of scope)
* Ensure installation of GDAL as it is required by django GIS (out of scope)
* Install Postgres with extenstion PostGIS (out of scope)
* Create python virtual environment (venv / virtualenv / virtualenvwrapper / pyenv) on your choise
    venv example in project directory:
    `python -m venv venv`, then activate it depends on OS
* Change dir to geodjango: `cd geodjango`
* install requirements: `pip install -r requirements.txt`
* apply migrations: `python manage.py migrate`
* run dev server: `python manage.py runserver`
* create superuser: `python manage.py createsuperuser`
* start app in dev mode: `python manage.py runserver`

Other times just run the last command

# After running:
* User be authorized with credentials of superuser for both main app and `/admin/`
* User can interact with app at home page as described above
* User can interact with admin to create another users and manage points
* After creating another users they can also be authorized and create / move their point at homepage
* For logout go to `http://localhost:8000/accounts/logout/` or use admin site
