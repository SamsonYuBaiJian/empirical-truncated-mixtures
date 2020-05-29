import ast
import argparse

def main(data_file_path):
    data_dict = open(str(data_file_path), 'r').readlines()
    data_dict = ast.literal_eval(data_dict[0])
    print(data_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file_path')
    args = parser.parse_args()

    main(args.data_file_path)