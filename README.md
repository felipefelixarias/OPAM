# Occupancy Prediction and Annotation from Maps

OPAM, or occupancy prediction and annotation for maps, is a library for learning and analyzing motion patterns in environments with traversability maps. It may be used to annotate an environment with trajectories from a dataset, generate synthetic pedestrian trajectories in a given map, or predict motion patterns using neural networks. For a narrative explanation of the features and how to use them, please check out the tutorials.

## Installation 
While we intend to support multiple installation methods in the future, the easiest way to get started is run the following commands:

```bash
git clone https://github.com/felipefelixarias/OPAM.git --recursive
cd OPAM 
conda create -n opam python=3.6
conda activate opam
pip install -r requirements.txt
cd opam/Python-RVO2
python setup.py build
python setup.py install
cd ../..
pip install -e .
```







