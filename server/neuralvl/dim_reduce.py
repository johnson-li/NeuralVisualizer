from time import time

# import numpy as np
# import matplotlib.pyplot as plt
import neuralvl.tsne.tsne3 as tsne3


# def plot_embedding(X, y, title=None):
#    plt.figure()
#    for i in range(X.shape[0]):
#        plt.text(X[i, 0], X[i, 1], str(y[i]),
#                 color=plt.cm.Set1(y[i] / 10.),
#                 fontdict={'weight': 'bold', 'size': 9})
#
#    if title is not None:
#        plt.title(title)
#    plt.show()


def tsne(labelNumber, imageNumber, dimension, iteration, dataset):
    # print("Computing t-SNE embedding")
    # tsne_model = manifold.TSNE(n_components=dimension, init='pca', random_state=0)
    # x_tsne = tsne_model.fit_transform(x)
    # return normalize(x_tsne)
    yield from tsne3.TSNE(labelNumber, imageNumber, dimension, iteration, dataset).train()


def load_dataset(number, dataset):
    pass


#    if dataset == 'MNIST':
#        (x_train, y_train), (x_test, y_test) = mnist.load_data()
#        x = x_train[:number]
#        x = np.array([a.flatten() for a in x])
#        y = y_train[:number]
#        return x, y


def reduce(algorithm, labelNumber, imageNumber, dataset, dimension, iteration):
    if algorithm == 'TSNE':
        algorithm = tsne
    yield from algorithm(labelNumber, imageNumber, dimension, iteration, dataset)


def main():
    number = 300
    # t0 = time()
    # x, y = load_dataset(number, 'MNIST')
    # x_tsne = reduce('TSNE', number, 'MNIST', 3)
    # plot_embedding(x_tsne, y, "t-SNE embedding of the digits (time %.2fs)" % (time() - t0))


if __name__ == '__main__':
    #main()
    from sklearn import manifold
    import tensorflow as tf
    import numpy as np
    from neuralvl import utils
    tsne_model = manifold.TSNE(n_components=3, init='pca', random_state=0)
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x = x_train[:100]
    x = np.array([a.flatten() for a in x])
    x_tsne = tsne_model.fit_transform(x)
    print(utils.normalize(x_tsne))
