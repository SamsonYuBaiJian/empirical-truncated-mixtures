import bivariate
import numpy as np
import os

if not os.path.exists('./manual'):
    os.makedirs('./manual')
if not os.path.exists('./random-points'):
    os.makedirs('./random-points')
if not os.path.exists('./random-points-vary-s'):
    os.makedirs('./random-points-vary-s')

interval_start = 2
interval_change = None
learning_rate = 0.01
true_means = (2.534, 6.395)
est_means = None
s_intervals = [(1, 2), (-3, 1.5)]
error_checkpoint = 0.1


# # for experiments with values close to [1,0]
# path = './manual'
# est_means = (1,0)
# fixed_error_step, _ = bivariate.run(learning_rate, true_means, est_means, s_intervals, error_checkpoint)
# save metrics
# f = open(path, 'w')
# save_dict = {}
# save_dict['fixed_error_step'] = str(fixed_error_step)
# save_dict['learning_rate'] = str(learning_rate)
# save_dict['real_means'] = str(true_means)
# save_dict['est_means'] = str(est_means)
# save_dict['s_intervals'] = str(s_intervals)
# save_dict['error_checkpoint'] = str(error_checkpoint)
# f.write(str(save_dict))
# f.close()


# for experiments with 1000 random points from uniform distribution --> save points
path = './random-points'
num_of_points = 1000
all_points = []
all_fixed_error_steps = []
points_1 = np.random.uniform(-5,5,num_of_points)
points_2 = np.random.uniform(-5,5,num_of_points)
for i in range(num_of_points):
    est_means = (points_1[i],points_2[i])
    fixed_error_step, _ = bivariate.run(learning_rate, true_means, est_means, s_intervals, error_checkpoint)
    all_points.append(est_means)
    all_fixed_error_steps.append(fixed_error_step)
# save metrics
experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
if len(experiment_nos) == 0:
    target_no = 1
else:
    target_no = max(experiment_nos) + 1
f = open(path + '/experiment-' + str(target_no), 'w')
save_dict = {}
save_dict['points'] = all_points
save_dict['fixed_error_steps'] = all_fixed_error_steps
save_dict['max_fixed_error_step'] = str(max(all_fixed_error_steps))
save_dict['min_fixed_error_step'] = str(min(all_fixed_error_steps))
save_dict['avg_fixed_error_step'] = str(sum(all_fixed_error_steps) / len(all_fixed_error_steps))
save_dict['learning_rate'] = str(learning_rate)
save_dict['real_means'] = str(true_means)
save_dict['est_means'] = str(est_means)
save_dict['s_intervals'] = str(s_intervals)
save_dict['error_checkpoint'] = str(error_checkpoint)
f.write(str(save_dict))
f.close()


# # for experiments with saved 1000 random points, varying S intervals --> load excel spreadsheet
# path = './random-points-vary-s'
# interval_change = 0.1
# all_fixed_error_steps = []
# all_denominators = []
# s_intervals = [(1, 2), (-3, None)]
# for i in np.arange(interval_start, interval_start+10, interval_change):
#     s_intervals[1] = (s_intervals[1][0], round(i,1))
#     fixed_error_step, denominator = bivariate.run(learning_rate, true_means, est_means, s_intervals, error_checkpoint)
#     all_fixed_error_steps.append(fixed_error_step)
#     all_denominators.append(denominator)

# # save metrics
# f = open(path, 'w')
# save_dict = {}
# save_dict['fixed_error_steps'] = all_fixed_error_steps
# save_dict['denominators'] = all_denominators
# save_dict['max_fixed_error_step'] = str(max(all_fixed_error_steps))
# save_dict['min_fixed_error_step'] = str(min(all_fixed_error_steps))
# save_dict['avg_fixed_error_step'] = str(sum(all_fixed_error_steps) / len(all_fixed_error_steps))
# save_dict['learning_rate'] = str(learning_rate)
# save_dict['real_means'] = str(true_means)
# save_dict['est_means'] = str(est_means)
# save_dict['s_intervals'] = str(s_intervals)
# save_dict['error_checkpoint'] = str(error_checkpoint)
# f.write(str(save_dict))
# f.close()