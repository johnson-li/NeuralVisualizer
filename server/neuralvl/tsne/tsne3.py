import tensorflow as tf
import numpy as np
import os

old_v = tf.logging.get_verbosity()
tf.logging.set_verbosity(tf.logging.ERROR)
from tensorflow.examples.tutorials.mnist import input_data

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
np.random.seed(6278)
tf.set_random_seed(6728)
beta1, beta2, adam_e = 0.9, 0.999, 1e-8
num_epoch = 800
print_size = 10
learning_rate = 0.00009


# ======= Activation Function  ==========
def tf_elu(x): return tf.nn.elu(x)


def d_tf_elu(x): return tf.cast(tf.greater(x, 0), tf.float64) + (
        tf_elu(tf.cast(tf.less_equal(x, 0), tf.float64) * x) + 1.0)


def tf_tanh(x): return tf.nn.tanh(x)


def d_tf_tanh(x): return 1 - tf_tanh(x) ** 2


def tf_sigmoid(x): return tf.nn.sigmoid(x)


def d_tf_sigmoid(x): return tf_sigmoid(x) * (1.0 - tf_sigmoid(x))


def tf_atan(x): return tf.atan(x)


def d_tf_atan(x): return 1.0 / (1.0 + x ** 2)


def tf_iden(x): return x


def d_tf_iden(x): return 1.0


def tf_softmax(x): return tf.nn.softmax(x)


# ======= Activation Function  ==========

# ====== miscellaneous =====
# code from: https://github.com/tensorflow/tensorflow/issues/8246
def tf_repeat(tensor, repeats):
    """
    Args:

    input: A Tensor. 1-D or higher.
    repeats: A list. Number of repeat for each dimension, length must be the same as the number of dimensions in input

    Returns:

    A Tensor. Has the same type as input. Has the shape of tensor.shape * repeats
    """
    expanded_tensor = tf.expand_dims(tensor, -1)
    multiples = [1] + repeats
    tiled_tensor = tf.tile(expanded_tensor, multiples=multiples)
    repeated_tesnor = tf.reshape(tiled_tensor, tf.shape(tensor) * repeats)
    return repeated_tesnor


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


# ================= LAYER CLASSES =================
class CNN():

    def __init__(self, k, inc, out, act=tf_elu, d_act=d_tf_elu):
        self.w = tf.Variable(tf.random_normal([k, k, inc, out], stddev=0.05, seed=2, dtype=tf.float64))
        self.m, self.v_prev = tf.Variable(tf.zeros_like(self.w, dtype=tf.float64)), tf.Variable(
            tf.zeros_like(self.w, dtype=tf.float64))
        self.act, self.d_act = act, d_act

    def getw(self): return self.w

    def feedforward(self, input, stride=1, padding='SAME'):
        self.input = input
        self.layer = tf.nn.conv2d(input, self.w, strides=[1, stride, stride, 1], padding=padding)
        self.layerA = self.act(self.layer)
        return self.layerA

    def backprop(self, gradient, stride=1, padding='SAME'):
        grad_part_1 = gradient
        grad_part_2 = self.d_act(self.layer)
        grad_part_3 = self.input

        grad_middle = grad_part_1 * grad_part_2

        grad = tf.nn.conv2d_backprop_filter(input=grad_part_3, filter_sizes=self.w.shape, out_backprop=grad_middle,
                                            strides=[1, stride, stride, 1], padding=padding
                                            )

        grad_pass = tf.nn.conv2d_backprop_input(input_sizes=[number_of_example] + list(grad_part_3.shape[1:]),
                                                filter=self.w, out_backprop=grad_middle,
                                                strides=[1, stride, stride, 1], padding=padding
                                                )

        update_w = []
        update_w.append(tf.assign(self.m, self.m * beta1 + (1 - beta1) * (grad)))
        update_w.append(tf.assign(self.v_prev, self.v_prev * beta2 + (1 - beta2) * (grad ** 2)))
        m_hat = self.m / (1 - beta1)
        v_hat = self.v_prev / (1 - beta2)
        adam_middel = learning_rate / (tf.sqrt(v_hat) + adam_e)
        update_w.append(tf.assign(self.w, tf.subtract(self.w, tf.multiply(adam_middel, m_hat))))

        return grad_pass, update_w


class CNN_Trans():

    def __init__(self, k, inc, out, act=tf_elu, d_act=d_tf_elu):
        self.w = tf.Variable(tf.random_normal([k, k, inc, out], stddev=0.05, seed=2))
        self.m, self.v_prev = tf.Variable(tf.zeros_like(self.w)), tf.Variable(tf.zeros_like(self.w))
        self.act, self.d_act = act, d_act

    def getw(self): return self.w

    def feedforward(self, input, stride=1, padding='SAME'):
        self.input = input
        output_shape2 = self.input.shape[2].value * stride
        self.layer = tf.nn.conv2d_transpose(
            input, self.w, output_shape=[batch_size, output_shape2, output_shape2, self.w.shape[2].value],
            strides=[1, stride, stride, 1], padding=padding)
        self.layerA = self.act(self.layer)
        return self.layerA

    def backprop(self, gradient, stride=1, padding='SAME'):
        grad_part_1 = gradient
        grad_part_2 = self.d_act(self.layer)
        grad_part_3 = self.input

        grad_middle = grad_part_1 * grad_part_2

        grad = tf.nn.conv2d_backprop_filter(input=grad_middle,
                                            filter_sizes=self.w.shape, out_backprop=grad_part_3,
                                            strides=[1, stride, stride, 1], padding=padding
                                            )

        grad_pass = tf.nn.conv2d(
            input=grad_middle, filter=self.w, strides=[1, stride, stride, 1], padding=padding
        )

        update_w = []
        update_w.append(tf.assign(self.m, self.m * beta1 + (1 - beta1) * (grad)))
        update_w.append(tf.assign(self.v_prev, self.v_prev * beta2 + (1 - beta2) * (grad ** 2)))
        m_hat = self.m / (1 - beta1)
        v_hat = self.v_prev / (1 - beta2)
        adam_middel = learning_rate / (tf.sqrt(v_hat) + adam_e)
        update_w.append(tf.assign(self.w, tf.subtract(self.w, tf.multiply(adam_middel, m_hat))))

        return grad_pass, update_w


class FNN():

    def __init__(self, input_dim, hidden_dim, act, d_act):
        self.w = tf.Variable(tf.random_normal([input_dim, hidden_dim], stddev=0.05, seed=2, dtype=tf.float64))
        self.m, self.v_prev = tf.Variable(tf.zeros_like(self.w, dtype=tf.float64)), tf.Variable(
            tf.zeros_like(self.w, dtype=tf.float64))
        self.v_hat_prev = tf.Variable(tf.zeros_like(self.w))
        self.act, self.d_act = act, d_act

    def feedforward(self, input=None):
        self.input = input
        self.layer = tf.matmul(input, self.w)
        self.layerA = self.act(self.layer)
        return self.layerA

    def backprop(self, gradient=None):
        grad_part_1 = gradient
        grad_part_2 = self.d_act(self.layer)
        grad_part_3 = self.input

        grad_middle = grad_part_1 * grad_part_2
        grad = tf.matmul(tf.transpose(grad_part_3), grad_middle)
        grad_pass = tf.matmul(tf.multiply(grad_part_1, grad_part_2), tf.transpose(self.w))

        update_w = []
        update_w.append(tf.assign(self.m, self.m * beta1 + (1 - beta1) * (grad)))
        update_w.append(tf.assign(self.v_prev, self.v_prev * beta2 + (1 - beta2) * (grad ** 2)))
        m_hat = self.m / (1 - beta1)
        v_hat = self.v_prev / (1 - beta2)
        adam_middel = learning_rate / (tf.sqrt(v_hat) + adam_e)
        update_w.append(tf.assign(self.w, tf.subtract(self.w, tf.multiply(adam_middel, m_hat))))

        return grad_pass, update_w


class ICA_Layer():

    def __init__(self, inc):
        self.w_ica = tf.Variable(tf.random_normal([inc, inc], stddev=0.05, seed=2))
        # self.w_ica = tf.Variable(tf.eye(inc)*0.0001)

    def feedforward(self, input):
        self.input = input
        self.ica_est = tf.matmul(input, self.w_ica)
        self.ica_est_act = tf_atan(self.ica_est)
        return self.ica_est_act

    def backprop(self):
        grad_part_2 = d_tf_atan(self.ica_est)
        grad_part_3 = self.input

        grad_pass = tf.matmul(grad_part_2, tf.transpose(self.w_ica))
        g_tf = tf.linalg.inv(tf.transpose(self.w_ica)) - (2 / batch_size) * tf.matmul(tf.transpose(self.input),
                                                                                      self.ica_est_act)

        update_w = []
        update_w.append(tf.assign(self.w_ica, self.w_ica + 0.2 * g_tf))

        return grad_pass, update_w


class TSNE_Layer():

    def __init__(self, inc, outc, P):
        self.w = tf.Variable(tf.random_normal(shape=[inc, outc], dtype=tf.float64, stddev=0.05, seed=2))
        self.P = P
        self.m, self.v = tf.Variable(tf.zeros_like(self.w)), tf.Variable(tf.zeros_like(self.w))

    def getw(self): return self.w

    def tf_neg_distance(self, X):
        X_sum = tf.reduce_sum(X ** 2, 1)
        distance = tf.reshape(X_sum, [-1, 1])
        return -(distance - 2 * tf.matmul(X, tf.transpose(X)) + tf.transpose(distance))

    def tf_q_tsne(self, Y):
        distances = self.tf_neg_distance(Y)
        inv_distances = tf.pow(1. - distances / 2.0, -1.5)
        inv_distances = tf.matrix_set_diag(inv_distances, tf.zeros([inv_distances.shape[0].value], dtype=tf.float64))
        return inv_distances / tf.reduce_sum(inv_distances), inv_distances

    def tf_tsne_grad(self, P, Q, W, inv):
        pq_diff = P - Q
        pq_expanded = tf.expand_dims(pq_diff, 2)
        y_diffs = tf.expand_dims(W, 1) - tf.expand_dims(W, 0)

        # Expand our inv_distances matrix so can multiply by y_diffs
        distances_expanded = tf.expand_dims(inv, 2)

        # Multiply this by inverse distances matrix
        y_diffs_wt = y_diffs * distances_expanded

        # Multiply then sum over j's and
        grad = 4. * tf.reduce_sum(pq_expanded * y_diffs_wt, 1)
        return grad

    def feedforward(self, input):
        self.input = input
        self.Q, self.inv_distances = self.tf_q_tsne(self.input)
        return self.Q

    def backprop(self):
        grad = self.tf_tsne_grad(self.P, self.Q, self.input, self.inv_distances)
        update_w = []
        update_w.append(tf.assign(self.m, self.m * beta1 + (1 - beta1) * (grad)))
        update_w.append(tf.assign(self.v, self.v * beta2 + (1 - beta2) * (grad ** 2)))
        m_hat = self.m / (1 - beta1)
        v_hat = self.v / (1 - beta2)
        adam_middel = learning_rate / (tf.sqrt(v_hat) + adam_e)
        update_w.append(tf.assign(self.w, tf.subtract(self.w, tf.multiply(adam_middel, m_hat))))

        return grad


# ================= LAYER CLASSES =================

# data
#mnist = input_data.read_data_sets('Dataset/MNIST/', one_hot=False, validation_size=0)
#image_train, label_train, test_batch, test_label = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels


# ======= TSNE ======
def neg_distance(X):
    X_sum = np.sum(X ** 2, 1)
    distance = np.reshape(X_sum, [-1, 1])
    return -(distance - 2 * X.dot(X.T) + distance.T)


def softmax_max(X, diag=True):
    X_exp = np.exp(X - X.max(1).reshape([-1, 1]))
    X_exp = X_exp + 1e-20
    if diag: np.fill_diagonal(X_exp, 0.)
    return X_exp / X_exp.sum(1).reshape([-1, 1])


def calc_prob_matrix(distances, sigmas=None):
    """Convert a distances matrix to a matrix of probabilities."""
    if sigmas is not None:
        two_sig_sq = 2. * sigmas.reshape([-1, 1]) ** 2
        return softmax_max(distances / two_sig_sq)
    else:
        return softmax_max(distances)


def perplexity(distances, sigmas):
    """Wrapper function for quick calculation of
    perplexity over a distance matrix."""
    prob_matrix = calc_prob_matrix(distances, sigmas)
    entropy = -np.sum(prob_matrix * np.log2(prob_matrix + 1e-10), 1)
    perplexity = 2.0 ** entropy
    return perplexity


def binary_search(distance_vec, target, max_iter=20000, tol=1e-13, lower=1e-10, upper=1e10):
    """Perform a binary search over input values to eval_fn.
    # Arguments
        eval_fn: Function that we are optimising over.
        target: Target value we want the function to output.
        tol: Float, once our guess is this close to target, stop.
        max_iter: Integer, maximum num. iterations to search for.
        lower: Float, lower bound of search range.
        upper: Float, upper bound of search range.
    # Returns:
        Float, best input value to function found during search.
    """
    for i in range(max_iter):
        guess = (lower + upper) / 2.
        val = perplexity(distance_vec, np.array(guess))
        if val > target:
            upper = guess
        else:
            lower = guess
        if np.abs(val - target) <= tol:
            break
    return guess


def find_optimal_sigmas(distances, target_perplexity):
    """For each row of distances matrix, find sigma that results
    in target perplexity for that role."""
    sigmas = []
    # For each row of the matrix (each point in our dataset)
    for i in range(distances.shape[0]):
        # Binary search over sigmas to achieve target perplexity
        correct_sigma = binary_search(distances[i:i + 1, :], target_perplexity)
        # Append the resulting sigma to our output array
        sigmas.append(correct_sigma)
    return np.array(sigmas)


def p_conditional_to_joint(P):
    """Given conditional probabilities matrix P, return
    approximation of joint distribution probabilities."""
    return (P + P.T) / (2. * P.shape[0])


def p_joint(X, target_perplexity):
    """Given a data matrix X, gives joint probabilities matrix.

    # Arguments
        X: Input data matrix.
    # Returns:
        P: Matrix with entries p_ij = joint probabilities.
    """
    # Get the negative euclidian distances matrix for our data
    distances = neg_distance(X)
    # Find optimal sigma for each row of this distances matrix
    sigmas = find_optimal_sigmas(distances, target_perplexity)
    # Calculate the probabilities based on these optimal sigmas
    p_conditional = calc_prob_matrix(distances, sigmas)
    # Go from conditional to joint probabilities matrix
    P = p_conditional_to_joint(p_conditional)
    return P


class TSNE:
    def __init__(self, labelNumber, imageNumber, dimension, iteration, dataset):
        if dataset == 'mnist':
            mnist = tf.keras.datasets.mnist
        elif dataset == 'fashion':
            mnist = tf.keras.datasets.fashion_mnist
        (image_train, label_train), (test_batch, test_label) = mnist.load_data()
        image_train = image_train.reshape((image_train.shape[0], -1))
        image_train = image_train.astype(np.float32)
        image_train = image_train / 0xff
        print("shape of x: " + str(image_train.shape))

        number_images = imageNumber
        indexes = [np.asarray(np.where(label_train == i))[:, :number_images] for i in range(10)]
        labels = [label_train[i].T for i in indexes][:labelNumber]
        self.train_label = np.vstack(labels)
        self.train_label = np.squeeze(self.train_label)
        images = [np.squeeze(image_train[i]) for i in indexes][:labelNumber]
        self.train_batch = np.vstack(images)

        self.iteration = iteration
        self.label_number = labelNumber
        self.image_number = imageNumber
        self.perplexity_number = 30
        self.reduced_dimension = dimension
        self.number_of_example = self.train_batch.shape[0]
        self.P = p_joint(self.train_batch.reshape([self.number_of_example, -1]), self.perplexity_number)

        self.l0 = FNN(784, 256, act=tf_elu, d_act=d_tf_elu)
        self.l1 = FNN(256, 128, act=tf_elu, d_act=d_tf_elu)
        self.l2 = FNN(128, 64, act=tf_elu, d_act=d_tf_elu)
        self.l3 = FNN(64, 3, act=tf_elu, d_act=d_tf_elu)
        self.tsne_l = TSNE_Layer(self.number_of_example, self.reduced_dimension, self.P)

        self.x = tf.placeholder(shape=[self.number_of_example, 784], dtype=tf.float64)

        self.layer0 = self.l0.feedforward(self.x)
        self.layer1 = self.l1.feedforward(self.layer0)
        self.layer2 = self.l2.feedforward(self.layer1)
        self.layer3 = self.l3.feedforward(self.layer2)
        self.Q = self.tsne_l.feedforward(self.layer3)

        self.cost = -tf.reduce_sum(
            self.P * tf.log(tf.clip_by_value(self.P, 1e-5, 1e5) / tf.clip_by_value(self.Q, 1e-5, 1e5)))

        self.grad_l3, self.grad_l3_up = self.l3.backprop(self.tsne_l.backprop())
        self.grad_l2, self.grad_l2_up = self.l2.backprop(self.grad_l3)
        self.grad_l1, self.grad_l1_up = self.l1.backprop(self.grad_l2)
        self.grad_l0, self.grad_l0_up = self.l0.backprop(self.grad_l1)

        self.grad_update = self.grad_l3_up + self.grad_l2_up + self.grad_l1_up + self.grad_l0_up

    def train(self):

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for iter in range(self.iteration):
                sess_results = sess.run([self.cost, self.grad_update, self.layer3], feed_dict={self.x: self.train_batch.astype(np.float64)})
                temp_w = sess_results[2]
                yield temp_w
                print('current iter: ', iter, ' Current Cost:  ', sess_results[0], end='\r')
                if iter % print_size == 0:
                    print('\n-----------------------------\n')


if __name__ == '__main__':
    tsne = TSNE(3, 100, 3, 1000, 'fashion')
    for w in tsne.train():
        pass
