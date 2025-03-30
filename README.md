# Benchmark problem version 0.1

## NOTE: For arbitrary numbers of objectives problem implementation, please go to  [arbitrary numbers of objective branch](https://github.com/dsakurai/benchmark-visualizer/tree/l-liu/n_objectives).

## Install the environment

1. Create python virtual environments:

- ```python -m venv venv```

2. Active environments

- On Windows ``.\venv\Scripts\activate ``
- On Linux/MacOS ``source venv/bin/activate``

3. Install requirements

- ``pip install -r requirements.txt``

4. (Optional) You may need to install jupyter notebook in order to use jupyter notebook

- ``pip install jupyter``

## Run with CLI

1. With the activated environment and sample tree file ("sample.json"). If you do not wish to track
   the experiment with mlflow, append ``--disable_tracking`` flag as parameter to the command below:

- ``python cli_main.py -f sample.json --dim 2``

## Run with jupyter notebook

1. With the activated environment, start a jupyter notebook server:

- ``jupyter notebook``

2. In the opened browser window, find the file ``sample_experiment.ipynb`` and open it.
   ***If the browser did not open automatically, click or copy&paste the link displayed in the console***
3. Follow the instructions in the notebook.

# Visualizer version 0.1

This visualizer was built with vue.js and FastAPI. You can either run the application with detached front-end and back end,
or to build the front-end and serve with FastAPI. If the development/experiment server is your current computer, no change
is needed. If it is a remote server, change the proxy in ``front-end/vue.config.js`` to your server's address.

## Frontend configuration


### Build the front-end

1. Install node.js.

2. Go to the front-ends directory and install dependencies via:
- ``yarn install``

(Make sure core pack is enabled, for more see: https://)

3. Build the front-end:
- ``yarn build``
4.Your front end should appear in ``front-end/dist``

### Run stand alone front-end application

1. Install node.js
2. Run the application using:
``npm run``

## Backend configuration
The backend can run with one simple command: ``uvicorn main:app --reload``
(To make sure you are in the right directory, it's better to set ``PYTHPNPATH`` variable by: ``export PYTHONPATH=.``)


1. Backend requires specification on the experiment result file directory to run.
By default, it will search for data in the current directory. To change this, run the startup command with positional argument.
For instance, if the experiment data is in ``data`` directory, run the backend with:
``uvicorn main:app data --reload``

2. By default, the backend only runs on localhost, to expose it on the network, use ``--host`` flag (not recommended).
It is highly recommended to use a reverse proxy application for deployment such as Apache2 or Nginx.