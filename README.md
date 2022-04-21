# Violence Against Women and Girls Dashboard

This dashboard was created as a means for to review the [Violence Against Women and Girls dataset](https://www.kaggle.com/datasets/andrewmvd/violence-against-women-and-girls) collected by [Demographic and Health Surveys (DHS)](https://dhsprogram.com/methodology/Survey-Types/DHS.cfm). See their documentation which they provide with this dataset in the [`docs`](https://github.com/LukeAC/vio-agnst-wmn-dash/tree/main/docs) section of this project. This dashboard is built using [Dash](https://plotly.com/dash/), a python-based framework for interactive web-application development created by the makers of Plotly. It is written on top of Flask, Plotly. js and React. js.

The latest deployed version of this app can be found at https://viowmndash.herokuapp.com/

<img width="941" alt="image" src="https://user-images.githubusercontent.com/75291170/164549431-338ff3a1-54b4-468d-9bc7-1ca7757a50f1.png">


# Usage

To run this dashboard locally, clone this repository to your local machine and follow the steps below:

1. install dependencies running either of the following commands in shell.

`$ pip install -r requirements.txt` (note: this should ideally be executed within your desired venv)

or

`$ conda env create -f environment.yml`

2. run the following command in your terminal from the `viowmndash/` directory, adjusting the parameters as desired.

`FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python app.py`


# Contributions

Contributions are always welcome - I recommend forking this repository if you plan to prepare any improvements or alterations to the dashboard. Feel free to reach out with any questions you may have about this application.
