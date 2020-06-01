import ast
import matplotlib.pyplot as plt
import math
import seaborn as sns
import argparse


def euclidean_distance(real, est):
    return math.sqrt(pow((real[0] - est[0]),2) + pow((real[1] - est[1]),2))

def main(exp_type, data_file_path, graph_type):
    if exp_type == 'random_points_epsilon_and_step':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        # get histogram
        plt.hist(data_dict['epsilon_steps'])
        if graph_type == 'title':
            plt.title("Epsilon Steps")
        elif graph_type == 'axes':
            pass
        plt.show()

        # get scatter plot
        distances = []
        true_mean = ast.literal_eval(data_dict['true_means'])

        for est_mean in data_dict['est_means']:
            distances.append(euclidean_distance(true_mean, est_mean))

        sns.regplot(distances, data_dict['epsilon_steps'])
        if graph_type == 'title':
            plt.title("Epsilon Step vs. Initial Distance")
        elif graph_type == 'axes':
            pass
        plt.show()

    elif exp_type == 'single_point_vary_s':
        # get graph for S interval stretch
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        if graph_type == 'title':
            plt.title('Epsilon Step vs. Denominator')
        elif graph_type == 'axes':
            plt.xlabel('Measure of the Truncated Set Under "Appropriate Mixture Distribution"')
            plt.ylabel('Avg No. of Iterations for Error Threshold of 0.1')
        plt.plot(data_dict['denominators'], data_dict['epsilon_steps'])
        plt.show()

    elif exp_type == 'random_points_error_vs_step':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        if graph_type == 'title':
            plt.title('2D Error vs. Step')
        elif graph_type == 'axes':
            pass
        plt.plot(data_dict['steps'], data_dict['errors'])
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_type')
    parser.add_argument('--data_file_path')
    parser.add_argument('--graph_type')
    args = parser.parse_args()

    main(args.exp_type, args.data_file_path, args.graph_type)