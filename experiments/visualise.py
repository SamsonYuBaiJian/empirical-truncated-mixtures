import ast
import matplotlib.pyplot as plt
import math
import seaborn as sns
import argparse

def euclidean_distance(real, est):
    return math.sqrt(pow((real[0] - est[0]),2) + pow((real[1] - est[1]),2))

def main(exp_type, data_file_path):
    if exp_type == 'random_points':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        # get histogram
        plt.hist(data_dict['epsilon_steps'])
        # plt.title("Epsilon Steps")
        plt.show()

        # get scatter plot
        distances = []
        true_mean = ast.literal_eval(data_dict['true_means'])

        for est_mean in data_dict['est_means']:
            distances.append(euclidean_distance(true_mean, est_mean))

        sns.regplot(distances, data_dict['epsilon_steps'])
        # plt.title("Epsilon Step vs. Distance")
        plt.show()

    elif exp_type == 'random_points_vary_s':
        # get graph for S interval stretch
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        # plt.title('Epsilon Step vs. Denominator')
        plt.plot(data_dict['denominators'], data_dict['epsilon_steps'])
        plt.show()

    elif exp_type == 'single_point':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        # plt.title('Epsilon Step vs. Denominator')
        plt.plot(data_dict['denominators'], data_dict['epsilon_steps'])
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_type')
    parser.add_argument('--data_file_path')
    args = parser.parse_args()

    main(args.exp_type, args.data_file_path)