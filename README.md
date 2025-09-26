# 3BC: Benchmarking and Visualization Based on Basin Connectivity

This repository contains the official implementation for the papers:

1.  [**Towards Benchmarking Multi-Objective Optimization Algorithms Based on the Basin Connectivity**](https://dl.acm.org/doi/10.1145/3712255.3734279) (GECCO '25 Companion)
2.  [**Visualization of Multiobjective Multimodal Benchmarking Based on Basin Connectivity**](https://dl.acm.org/doi/10.1145/3638530.3654190) (GECCO '24 Companion)

---

## Overview

Evaluating Multi-Objective Evolutionary Algorithms (MOEAs) on multimodal landscape is challenging. Standard benchmarks often have fitness landscapes that are unknown or fixed, making it difficult to analyze an algorithm's specific exploration and exploitation behaviors.

**Benchmarking Based on Basin Connectivity (3BC)**  allows users to pre-determine the fitness landscape by defining the structure and connectivity of basins of attraction via a basin graph. This provides a controlled environment to rigorously test how MOEAs navigate landscapes with specific challenges, such as multiple local and global optima.

To complement the 3BC generator, we proposed a novel visualization that projects the high-dimensional basins in a 2D plot, in which the individuals of benchmarked MOEAs for user-specified generations are visible. It helps researchers configure 3BC landscapes and, more importantly, understand the behavior of different MOEAs.

This repository provides the complete code for both the **3BC benchmark generator** and the **web-based visualization tool**.

---

## Getting Started

### Prerequisites

* Python 3.8+
* Node.js and Yarn (for the visualization tool's frontend)

## Getting started

### Install the environment

1. Create python virtual environments:

- ```python -m venv venv```

2. Active environments

- On Windows ``.\venv\Scripts\activate ``
- On Linux/MacOS ``source venv/bin/activate``

3. Install requirements

- ``pip install -r requirements.txt``

4. (Optional) You may need to install jupyter notebook in order to use jupyter notebook

- ``pip install jupyter``

### Run with CLI

1. With the activated environment and sample tree file ("sample.json"). If you do not wish to track
   the experiment with mlflow, append ``--disable_tracking`` flag as parameter to the command below:

- ``python cli_main.py -f sample.json --dim 2``

### Run with jupyter notebook

1. With the activated environment, start a jupyter notebook server:

- ``jupyter notebook``

2. In the opened browser window, find the file ``sample_experiment.ipynb`` and open it.
   ***If the browser did not open automatically, click or copy&paste the link displayed in the console***
3. Follow the instructions in the notebook.

## Visualizer
This visualizer was built with vue.js and FastAPI. You can either run the application with detached front-end and back end,
or to build the front-end and serve with FastAPI. If the development/experiment server is your current computer, no change
is needed. If it is a remote server, change the proxy in ``front-end/vue.config.js`` to your server's address.

### Frontend configuration


#### Build the front-end

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

### Backend configuration
The backend can run with one simple command: ``uvicorn main:app --reload``
(To make sure you are in the right directory, it's better to set ``PYTHPNPATH`` variable by: ``export PYTHONPATH=.``)


1. Backend requires specification on the experiment result file directory to run.
By default, it will search for data in the current directory. To change this, run the startup command with positional argument.
For instance, if the experiment data is in ``data`` directory, run the backend with:
``uvicorn main:app data --reload``

2. By default, the backend only runs on localhost, to expose it on the network, use ``--host`` flag (not recommended).
It is highly recommended to use a reverse proxy application for deployment such as Apache2 or Nginx.

----

## Citation

If you find our work useful, please consider citing our paper as follows:

```
@inproceedings{10.1145/3638530.3654190,
author = {Liu, Likun and Ota, Ryosuke and Yamamoto, Takahiro and Hamada, Naoki and Sakurai, Daisuke},
title = {Visualization of Multiobjective Multimodal Benchmarking Based on Basin Connectivity},
year = {2024},
isbn = {9798400704956},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3638530.3654190},
doi = {10.1145/3638530.3654190},
booktitle = {Proceedings of the Genetic and Evolutionary Computation Conference Companion},
pages = {347–350},
numpages = {4},
keywords = {multiobjective optimization, visualization, benchmarking},
location = {Melbourne, VIC, Australia},
series = {GECCO '24 Companion}
}
```
as well as the original 3BC paper:
```
@inproceedings{10.1145/3638530.3654190,
author = {Liu, Likun and Ota, Ryosuke and Yamamoto, Takahiro and Hamada, Naoki and Sakurai, Daisuke},
title = {Visualization of Multiobjective Multimodal Benchmarking Based on Basin Connectivity},
year = {2024},
isbn = {9798400704956},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3638530.3654190},
doi = {10.1145/3638530.3654190},
booktitle = {Proceedings of the Genetic and Evolutionary Computation Conference Companion},
pages = {347–350},
numpages = {4},
keywords = {multiobjective optimization, visualization, benchmarking},
location = {Melbourne, VIC, Australia},
series = {GECCO '24 Companion}
}
```

----

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. Note that the repository relies on third-party code, which is subject to their respective licenses.