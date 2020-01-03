import bivariate
import numpy as np

# TODO: change values for your bivariate experiments
interval_start = 2
interval_change = 0.1 # 0.05
steps = 10000
learning_rate = 0.01 # 0.05/0.1
real_means = (2,1)
est_means = (5,4)
s_intervals = [(-2, 2), (-2, None)]
error_checkpoint = 0.1

for i in np.arange(interval_start, interval_start+10, interval_change):
    s_intervals[1] = (s_intervals[1][0], round(i,1))
    bivariate.run(steps, learning_rate, real_means, est_means, s_intervals, error_checkpoint)