# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research.

## Requirements
Make sure you have Python 3, Cython, scipy, matplotlib and seaborn installed.

## Experiment Types
- `random_points_error_vs_step`: Using N random points from a uniform distribution as the initial estimated mean, get the change in error from the true mean with no. of update iterations.
- `random_points_epsilon_and_step`: Using N random points from a uniform distribution as the initial estimated mean, get the no. of iterations needed to reach a fixed error from the true mean.
- `single_point_vary_s`: Using a single fixed point as the initial estimated mean, get the no. of iterations needed for it to reach a fixed error from the true mean, while increasing/decreasing two dimensions of the integral intervals at a fixed rate.
- `trajectory`: Get the convergence trajectories of N initial points to a true mean, on the x-y plane.

## Running Experiments
- Build the Cython extensions in place for your Python version by entering `python3 setup.py build_ext --inplace` in the root directory.
- Run experiments using `python3 run_experiments.py --exp_type {random_points_error_vs_step, random_points_epsilon_and_step, single_point_vary_s, trajectory}` (you can change the appropriate configurations in `run_experiments.py`).
- To view the graph for an experiment, use `python3 visualise.py --exp_type {random_points_error_vs_step, random_points_epsilon_and_step, single_point_vary_s, trajectory} --data_file_path /path/to/experiment_data_file --graph_type {title, axes, ?}`.

## Reference
- http://jiffyclub.github.io/scipy/tutorial/integrate.html