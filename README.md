# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research with Dr. Ioannis Panageas.

## Requirements
Make sure you have Python 3, Cython, scipy, matplotlib and seaborn installed.

## Running Experiments
- Compile Cython code by entering 'python3 setup.py build_ext --inplace' in the 'experiments' directory.
- Run experiments using 'python3 run_experiments.py --exp_type experiment_type'. Change configurations in the file for your own needs. The '--exp_type' can be either 'single_point', 'random_points' or 'random_points_vary_s'.
- To view the graphs an experiment, enter 'python3 visualise.py --exp_type experiment_type --data_file_path /path/to/experiment_data_file'.
- To view dictionary data for an experiment, enter 'python3 view_data.py --data_file_path /path/to/experiment_data_file'.