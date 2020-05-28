# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research with Dr. Ioannis Panageas.

## Requirements
Make sure you have Python 3, Cython, scipy, matplotlib and seaborn installed.

## Running Experiments
- To compile Cython code, enter 'python3 setup.py build_ext --inplace' in the 'experiments' directory.
- Run experiments using 'python3 run_experiments.py --exp_type' in the 'bivariate' directory, and change configurations in the file for your own needs. The '--exp_type' can be either 'single_point', 'random_points' or 'random_points_vary_s'.
- To visualise the graphs for the Number of Iterations vs. Denominator experiment, enter 'python3 visualise.py --exp_type experiment_type --data_file_path /path/to/experiment_data_file'.

## Experiment Data Format
### Experiments
./learning\_rate-real\_means-fixed\_error/est\_means-s\_intervals-denominator-fixed\_error\_step

### Graphs
- Error vs. iteration graphs: ./error-vs.-iteration/steps-learning\_rate-real\_means-est\_means-s\_intervals-denominator.png
- Number of iterations vs. denominator graphs:
