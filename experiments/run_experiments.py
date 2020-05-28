import bivariate
import numpy as np
import os
import argparse

def main(exp_type):
    all_est_means = []
    interval_change = 0.1
    learning_rate = 0.01

    # true_means = (2.534, 6.395)
    # est_means = (1,0)
    # s_intervals = [(1, 2), (-3, 1.5)]

    true_means = (2, 1)
    est_means = (5, 4)
    s_intervals = [(-2, 2), (-2, 2)]

    epsilon = 0.1
    num_of_points = 100
    np.random.seed(42)

    # for experiments with values close to [1,0]
    if exp_type == 'single_point':
        path = './single_point'
        if not os.path.exists(path):
            os.makedirs(path)
        epsilon_step, _ = bivariate.run(learning_rate, true_means, est_means, s_intervals, epsilon)
        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['epsilon_step'] = str(epsilon_step)
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = str(est_means)
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()

    # for experiments with 100 random points from uniform distribution --> save points
    elif exp_type == 'random_points':
        path = './random_points'
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []
        points_1 = np.random.uniform(-5,5,num_of_points)
        points_2 = np.random.uniform(-5,5,num_of_points)
        all_est_means = []
        for i in range(num_of_points):
            epsilon_step, _ = bivariate.run(learning_rate, true_means, est_means, s_intervals, epsilon)
            all_est_means.append((points_1[i],points_2[i]))
            all_epsilon_steps.append(epsilon_step)
        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['epsilon_steps'] = all_epsilon_steps
        save_dict['max_epsilon_step'] = str(max(all_epsilon_steps))
        save_dict['min_epsilon_step'] = str(min(all_epsilon_steps))
        save_dict['avg_epsilon_step'] = str(sum(all_epsilon_steps) / len(all_epsilon_steps))
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = str(all_est_means)
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()

    # for experiments with saved 100 random points, varying S intervals
    elif exp_type == 'random_points_vary_s':
        path = './random_points_vary_s'
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []
        all_denominators = []
        interval_start = s_intervals[1][1]
        for i in np.arange(interval_start, interval_start+10, interval_change):
            s_intervals[1] = (s_intervals[1][0], round(i,1))
            epsilon_step, denominator = bivariate.run(learning_rate, true_means, est_means, s_intervals, epsilon)
            all_epsilon_steps.append(epsilon_step)
            all_denominators.append(denominator)
        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['epsilon_steps'] = all_epsilon_steps
        save_dict['denominators'] = all_denominators
        save_dict['max_epsilon_step'] = str(max(all_epsilon_steps))
        save_dict['min_epsilon_step'] = str(min(all_epsilon_steps))
        save_dict['avg_epsilon_step'] = str(sum(all_epsilon_steps) / len(all_epsilon_steps))
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = str(est_means)
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_type')
    args = parser.parse_args()

    main(args.exp_type)