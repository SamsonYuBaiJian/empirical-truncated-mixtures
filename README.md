# Empirical Truncated Mixtures
Empirical truncated Gaussian mixture research with Dr. Ioannis Panageas.

## Usage
### Bivariate
- To compile Cython code, enter 'python3 setup.py build_ext --inplace' in the 'bivariate' directory.
- Run experiments using 'python3 run_experiments.py' in the 'bivariate' directory, and change configurations in the file for your own needs.
- Enter 'python3' to start Python in the 'bivariate' directory.
- Enter 'import bivariate' for bivariate experiments.
- To load experimental results, enter 'bivariate.view(/path/to/result/file)'.
- To view the graphs for the Number of Iterations vs. Denominator experiment, enter 'bivariate.plot\_denom(/path/to/bivariate/experiments/experiment\_folder)'.

### Univariate
- To compile Cython code, enter 'python3 setup.py build_ext --inplace' in the 'univariate' directory.
- Enter 'python3' to start Python in the 'univariate' directory.
- Enter 'import univariate' for univariate experiments.
- Run experiments using 'univariate.run(\*args)'.
- Enter 'univariate.help()' for more details on how to run the program.
- To load experimental results, enter 'univariate.view(/path/to/result/file)'.
- To view the graphs for the Number of Iterations vs. Denominator experiment, enter 'univariate.plot\_denom(/path/to/univariate/experiments/experiment\_folder)'.

## Bivariate Data Format
### Experiments
./learning\_rate-real\_means-fixed\_error/est\_means-s\_intervals-denominator-fixed\_error\_step

### Graphs
- Error vs. iteration graphs: ./error-vs.-iteration/steps-learning\_rate-real\_means-est\_means-s\_intervals-denominator.png
- Number of iterations vs. denominator graphs:
