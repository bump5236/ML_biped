import os


def path_txt(save_name, path):
    f = open(save_name, 'w')
    for file in os.listdir(path):
        path_name = path + file + '\n'
        f.writelines(path_name)
    f.close()
    print('Finish')


save_name = 'path.txt'
path = 'dataset_1/'
path_txt(save_name, path)
