# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research.

## Requirements
Make sure you have Python 3, Cython, scipy, matplotlib and seaborn installed.

## Experiment Types
- `single_point`: Using a single fixed point as the initial estimated mean, get the change in error from the true mean with no. of update iterations
- `random_points`: Using 100 random points from a uniform distribution as the initial estimated mean, get the no. of iterations needed to reach a fixed error from the true mean
- `single_point_vary_s`: Using a single fixed point as the initial estimated mean, get the no. of iterations needed for it to reach a fixed error from the true mean, while increasing/decreasing one dimension of the integral intervals at a fixed rate.

## Running Experiments
- Compile Cython code by entering `python3 setup.py build_ext --inplace` in the root directory.
- Run experiments using `python3 run_experiments.py --exp_type experiment_type` (or change the appropriate configurations in the Python file).
- To view the graph for an experiment, use `python3 visualise.py --exp_type experiment_type --data_file_path /path/to/experiment_data_file`.
- To view the data for an experiment, use `python3 view_data.py --data_file_path /path/to/experiment_data_file`.

## Visualisations
- Scatterplot for no. of iterations needed for the error between the 100 random points and the true mean to reach a fixed epsilon, and the initial error between the points and the true mean
- Histogram for no. of iterations needed for the error between the 100 random points and the true mean to reach a fixed epsilon

## References
- http://jiffyclub.github.io/scipy/tutorial/integrate.html
