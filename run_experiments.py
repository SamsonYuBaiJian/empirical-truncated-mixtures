import bivariate
import numpy as np
import os
import argparse

def main(exp_type):
    all_est_means = []
    learning_rate = 0.01
    epsilon = 0.1

    # for 2D Error vs Step experiment with random points from uniform distribution
    if exp_type == 'random_points_error_vs_step':
        path = './experiments/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)

        # parameters
        step_limit = 10000
        num_of_points = 100
        np.random.seed(42)
        true_means = (2.534, 6.395)
        s_intervals = [(1, 2), (-3, 1.5)]
        print_every = 10

        points_1 = np.random.uniform(-7,7,num_of_points)
        points_2 = np.random.uniform(-7,7,num_of_points)
        all_est_means = []
        final_error_list = [0] * step_limit

        print("Doing " + str(num_of_points) + " random points for 2D Error vs Step experiment...")
        for i in range(num_of_points):
            est_means = (points_1[i],points_2[i])
            step_list, error_list = bivariate.run(step_limit, learning_rate, true_means, est_means, s_intervals, epsilon)
            all_est_means.append(est_means)
            for j in range(step_limit):
                final_error_list[j] += error_list[j]
            if (i + 1) % print_every == 0:
                print(str(i) + "/" + str(num_of_points) + " random point(s) done.")
        for i in range(step_limit):
            final_error_list[i] /= num_of_points
        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['steps'] = step_list
        save_dict['errors'] = final_error_list
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = all_est_means
        save_dict['s_intervals'] = str(s_intervals)
        f.write(str(save_dict))
        f.close()

    # for histogram and scatter with random points from uniform distribution
    elif exp_type == 'random_points_epsilon_and_step':
        path = './experiments/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []

        # parameters
        num_of_points = 100
        np.random.seed(42)
        true_means = (2.534, -6.395)
        s_intervals = [(1, 2), (-3, 1.5)]

        points_1 = np.random.uniform(-7,7,num_of_points)
        points_2 = np.random.uniform(-7,7,num_of_points)
        all_est_means = []

        print("Doing " + str(num_of_points) + " random points for histogram and scatterplot experiments...")
        for i in range(num_of_points):
            est_means = (points_1[i],points_2[i])
            epsilon_step, _ = bivariate.run(None, learning_rate, true_means, est_means, s_intervals, epsilon)
            all_est_means.append(est_means)
            all_epsilon_steps.append(epsilon_step)
            if (i + 1) % print_every == 0:
                print(str(i) + "/" + str(num_of_points) + " random point(s) done.")
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
        save_dict['est_means'] = all_est_means
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()

    # for experiments with single point, varying S intervals
    elif exp_type == 'single_point_vary_s':
        path = './experiments/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []
        all_denominators = []

        # parameters
        interval_change = 0.1
        est_means = (1, 0)
        true_means = (-2.534, 6.395)
        s_intervals = [(1, 2), (-3, 0)]
        # est_means = (5, 4)
        # true_means = (2, 1)
        # s_intervals = [(-2, 2), (-2, 2)]

        interval_start = s_intervals[1][1]
        
        print("Doing a single point for interval varying experiment...")
        for i in np.arange(interval_start, interval_start+10, interval_change):
            s_intervals[1] = (s_intervals[1][0], round(i,1))
            epsilon_step, denominator = bivariate.run(None, learning_rate, true_means, est_means, s_intervals, epsilon)
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

    if not os.path.exists('./experiments'):
        os.makedirs('./experiments')

    main(args.exp_type)