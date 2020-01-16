# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research with Dr. Ioannis Panageas.

## Running Experiments
- To compile Cython code, enter 'python3 setup.py build_ext --inplace' in the 'experiments' directory.
- Run experiments using 'python3 run_experiments.py' in the 'bivariate' directory, and change configurations in the file for your own needs.
- To load experimental results, enter 'bivariate.view(/path/to/result/file)'.
- To view the graphs for the Number of Iterations vs. Denominator experiment, enter 'bivariate.plot\_denom(/path/to/bivariate/experiments/experiment\_folder)'.

## Experiment Data Format
### Experiments
./learning\_rate-real\_means-fixed\_error/est\_means-s\_intervals-denominator-fixed\_error\_step

### Graphs
- Error vs. iteration graphs: ./error-vs.-iteration/steps-learning\_rate-real\_means-est\_means-s\_intervals-denominator.png
- Number of iterations vs. denominator graphs:
