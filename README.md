Report Hub
==============================

Report Hub is a web service to host and visualize your html reports that is not necessarily a single web page application.

Initially, this tool was created to easily visualize the reports generated during a test pipeline (JMeter, Selenium,...). 

---
Deployment
------------

---
Contributing
------------
Install de pendency:
__pip install -r requirements.txt__

---
Application EndPoint
------------

---
Project Organization
------------
    ├── README.md          <- The top-level README for developers using this project.
    ├── static
    │   ├── commons        <- Containt static web ellements (js,css,...) of the application
    │   └── reports        <- Containt static web element (js,css,...) of each report
    │
    ├── templates
    │   ├── commons        <- Containt html component of th application
    │   └── reports        <- Containt index.html of each report
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    └── app.py             <- Main of app. Define REST API endpoint
--------
