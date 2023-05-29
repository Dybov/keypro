# Initial task
## Applicant code test assignment
Make a (Geo)Django application for creating and moving point objects on map. For DB you might want to use PostGIS (PostgreSQL) or SQLite. For frontend you might want to use Leaflet or OpenLayers (they are supported by majority of frontend frameworks – ReactJS, Vue, Angular – though framework usage is not mandated, you can do it even in javascript or using jQuery). You are not limited in the tools or components you are using. 
## Application basic functionality
Application user main screen is map. User should be able to scroll the map (extent of the map is not important), to create point on a map by clicking on map pane, update positions of points he created by dragging them.

## Application advanced (optional) functionality
User should be able to see points other users created in one style (in example color or shape) and 
points he created in other style.

User should not be able to move points created by other users. When user closes the browser window and then opens it again, he should be able to continue creating and moving his points application (if no specific measure to delete data about user in browser is done).

Admin site should exist where admins see all the points, delete any of it or change its owner and coordinates. Points in admin should be able to be filtered by its creator. Also admins should be able to see user info with number of points they created and edit it. Admins should be able to assign other users admin rights. Admins should be able to delete users, in such case points should stay. 
## Project basic functionality
Project should be supplied in some code repository. Project should have instructions on installing and running it. 
## Project advanced (optional) functionality
Project should have some tests, preferably in frontend and backend. Project should have docstrings for code used in it. 
Application should be packaged in Docker to be able to run on windows or linux hosts. You might want to run nginx or some other web server to serve static content and some application server like gunicorn or uwsgi (or some other wsgi or asgi server) to run Django though it is not mandatory.