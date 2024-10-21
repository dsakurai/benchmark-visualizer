# Benchmark problem version 0.1

## NOTE: For arbitrary numbers of objectives problem implementation, please kindly go to  [arbitrary numbers of objective branch](https://github.com/dsakurai/benchmark-visualizer/tree/l-liu/n_objectives).

## Install the environment
1. Create python virtual environments:
-  ```python -m venv venv```

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
2. In the opened browser window, find the file ``sample_experiment.ipynb`` and open it. ***If the browser did not open automatically, click or copy&paste the link displayed in the console***
3. Follow the instructions in the notebook.
