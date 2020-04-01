# Graphing Bandwidth Challenge

## Starting the services

To start the python API, run ```./startAPI.sh``` in this directory. This will start up a virtual environment with the necessary packages (Flask and Flasak-related packages) and then start the api at http://127.0.0.1:5000/, with a single endpoint at /bandwidth.


To start the graph viewer, run ```./startGraphViewer.sh``` in this directory. This will call ```yarn``` to install the necessary npm packages (primarily Axios and Recharts), and then yarn start and run the graph viewer on http://localhost:3000/

A device ID is required for the get request, so a url such as http://localhost:3000/?device_uuid=69639c99-dea4-4c2d-8bb2-412145fada65 should be used.
