# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research with Dr. Ioannis Panageas.

## Requirements
Make sure you have Python 3, Cython, scipy, matplotlib and seaborn installed.

## Running Experiments
- Compile Cython code by entering 'python3 setup.py build_ext --inplace' in the 'experiments' directory.
- Run experiments using 'python3 run_experiments.py --exp_type experiment_type'. Change configurations in the file for your own needs. The '--exp_type' can be either 'single_point', 'random_points' or 'random_points_vary_s'.
- To view the graph for an experiment, enter 'python3 visualise.py --exp_type experiment_type --data_file_path /path/to/experiment_data_file'.
- To view the dictionary data for an experiment, enter 'python3 view_data.py --data_file_path /path/to/experiment_data_file'.

## Visualisations
- Scatterplot for steps taken for the distance between the 100 random points and the true mean to reach a fixed epsilon and the initial distance between the points and the true mean
- Histogram for steps taken for the distance between the 100 random points and the true mean to reach a fixed epsilon

## References
- http://jiffyclub.github.io/scipy/tutorial/integrate.html