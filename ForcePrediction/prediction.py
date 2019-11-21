# -*- coding: utf-8 -*-
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import pandas as pd
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import cuda
from chainer import optimizers
from chainer import training
from chainer import iterators
from chainer import serializers
from chainer.training import extensions
from chainer.training import triggers
from chainer.datasets import ImageDataset
from chainer.datasets import TransformDataset
from chainer.datasets import TupleDataset
from chainer.datasets import split_dataset
from chainer.datasets import split_dataset_random
from chainercv.transforms import resize


class AlexNet(chainer.Chain):

    def __init__(self, n_out, train=True):
        super().__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(None, 96, ksize=11, stride=2)
            self.conv2 = L.Convolution2D(None, 256, ksize=5, pad=2)
            self.conv3 = L.Convolution2D(None, 384, ksize=3, pad=1)
            self.conv4 = L.Convolution2D(None, 384, ksize=3, pad=1)
            self.conv5 = L.Convolution2D(None, 256, ksize=3, pad=1)
            self.fc6 = L.Linear(None, 4096)
            self.fc7 = L.Linear(None, 4096)
            self.fc8 = L.Linear(None, n_out)

    def __call__(self, x):
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv1(x))), 3, stride=2)
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv2(h))), 3, stride=2)
        h = F.relu(self.conv3(h))
        h = F.relu(self.conv4(h))
        h = F.max_pooling_2d(F.relu(self.conv5(h)), 3, stride=2)
        h = F.dropout(F.relu(self.fc6(h)))
        h = F.dropout(F.relu(self.fc7(h)))
        h = self.fc8(h)

        return h


class Model(chainer.Chain):

    def __init__(self, n_out, Train=True):
        super().__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(None, 64, ksize=5, stride=2)
            self.conv2 = L.Convolution2D(None, 64, ksize=3, pad=1)
            self.fc3 = L.Linear(None, 4096)
            self.fc4 = L.Linear(None, n_out)

    def __call__(self, x):
        h = F.max_pooling_2d(F.relu(self.conv1(x)), 3)
        h = F.max_pooling_2d(F.relu(self.conv2(h)), 3)
        h = F.dropout(F.relu(self.fc3(h)))
        h = self.fc4(h)

        return h


def transform(data):
    data = resize(data, (256, 256))
    picture = data / 255.
    return picture


path = 'path.txt'  # 500fps
picture = ImageDataset(path)
picture = TransformDataset(picture, transform)

path = '20191101/2019110110201.csv'  # 1000fps
force = np.loadtxt(path, delimiter=',', skiprows=7)
force_z = force[:len(picture) * 2:2, 3].astype(np.float32)

x = picture
t = np.reshape(force_z, (6400, 1))
dataset = TupleDataset(x, t)

n_train = int(len(dataset) * 0.8)
n_valid = int(len(dataset) * 0.1)
train, valid_test = split_dataset(dataset, n_train)
valid, test = split_dataset(valid_test, n_valid)
# train, valid_test = split_dataset_random(dataset, n_train, seed=0)
# valid, test = split_dataset_random(valid_test, n_valid, seed=0)

print('Training dataset size:', len(train))
print('Validation dataset size:', len(valid))
print('Test dataset size:', len(test))

train_mode = False

if train_mode == True:
    batchsize = 16
    train_iter = iterators.SerialIterator(train, batchsize)
    valid_iter = iterators.SerialIterator(
        valid, batchsize, shuffle=False, repeat=False)

    net = Model(n_out=1)
    model = L.Classifier(net, lossfun=F.mean_squared_error)
    model.compute_accuracy = False  # regression

    gpu_id = 0
    cuda.get_device(gpu_id).use()
    model.to_gpu(gpu_id)

    max_epoch = 16
    print('max_epoch: {}'.format(max_epoch))
    now = datetime.datetime.now()
    now = now.strftime('%Y%m%d%H%M')
    optimizer = optimizers.Adam().setup(model)
    updater = training.StandardUpdater(train_iter, optimizer, device=0)
    # trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='result/{}'.format(now))
    trigger = triggers.EarlyStoppingTrigger(
        monitor='val/main/loss', check_trigger=(1, 'epoch'), patients=5, max_trigger=(max_epoch, 'epoch'))
    trainer = training.Trainer(updater, trigger, out='result/{}'.format(now))

    trainer.extend(extensions.LogReport(trigger=(1, 'epoch'), log_name='log'))
    trainer.extend(extensions.Evaluator(
        valid_iter, model, device=0), name='val')
    trainer.extend(extensions.PlotReport(
        ['main/loss', 'val/main/loss'], x_key='epoch', file_name='loss.png'))
    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'val/main/loss', 'elapsed_time']))

    trainer.run()

    model.to_cpu()
    serializers.save_npz('result/{}/model.npz'.format(now), model)

else:
    net = Model(n_out=1)
    model = L.Classifier(net, lossfun=F.mean_squared_error)

    datetime = 201911202101
    serializers.load_npz('result/{}/model.npz'.format(datetime), model)

    gpu_id = 0
    cuda.get_device(gpu_id).use()
    model.to_gpu(gpu_id)

    y_list = []
    t_list = []

    for i in range(len(test)):
        x, t = test[i]
        x = x[None, ...]
        x = model.xp.asarray(x)

        with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
            y = net(x)
        y = y.array
        y = cuda.to_cpu(y)

        y_list.append(y[0][0])
        t_list.append(t[0])

    plt.figure(figsize=(7, 5))
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    data_list = np.arange(0, len(t_list)) / 500 * 1000
    plt.plot(data_list, t_list, color='skyblue', label='Truth', lw=2)
    plt.plot(data_list, y_list, color='darkblue', label='Prediction', lw=2)

    plt.xlabel('Time [msec]')
    plt.ylabel('Fz [N]')
    plt.xlim(0, len(data_list) / 500 * 1000)
    plt.ylim(-100, 700)

    plt.gca().xaxis.set_major_locator(tick.MultipleLocator(200))  # x_locator
    plt.gca().xaxis.set_minor_locator(tick.MultipleLocator(20))
    plt.gca().yaxis.set_major_locator(tick.MultipleLocator(200))  # y_locator
    plt.gca().yaxis.set_minor_locator(tick.MultipleLocator(20))
    plt.grid(ls='--', which='major')
    plt.grid(ls='--', which='minor', alpha=0.25)

    plt.legend(loc='upper right')
    plt.tight_layout()
    # plt.show()
    plt.savefig('result/{}/test.png'.format(datetime))

print('Finish')
