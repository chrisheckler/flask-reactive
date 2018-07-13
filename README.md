# Overview
Flask is a Python web microframework that can also serve as an excellent RESTful API.  This project aims to make a useful template for many API use cases. 

## Installation
This app requires a JUJU installation, cloud provider or can be bootstrapped on your local machine for prototyping.  Once these requirements are met, deploy the following JUJU solutions:
	juju deploy cs:~chrisheckler/flask-reactive --series bionic
	juju deploy nginx
	juju deploy postgresql
Next, you will need to:
	juju relate flask-reactive:pgsql postgresql:db
	juju expose nginx

### Contact Information
Chris Heckler <hecklerchris@hotmail.com>

