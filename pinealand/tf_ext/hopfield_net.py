import tensorflow as tf


class HopfieldNetwork(tf.Module):
    def __init__(self, num_neurons):
        super(HopfieldNetwork, self).__init__()
        self.num_neurons = num_neurons
        self.w = tf.Variable(tf.zeros([num_neurons, num_neurons]), dtype=tf.float32)

    @tf.function
    def call(self, inputs):
        output = tf.sign(tf.matmul(inputs, self.w))
        return output

    @tf.function
    def train(self, patterns):
        patterns = tf.sign(patterns)
        self.w.assign_add(tf.matmul(patterns, patterns, transpose_a=True))


if __name__ == '__main__':
    # 测试
    patterns = tf.constant([[1, 1, -1, -1,
                             1, 1, -1, -1,
                             -1, -1, 1, 1,
                             0, 0, 0, 1]], dtype=tf.float32)
    input_data = tf.constant([[1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1]], dtype=tf.float32)

    # 创建和训练Hopfield网络
    hopfield_net = HopfieldNetwork(num_neurons=16)
    hopfield_net.train(patterns)

    # 运行网络并输出结果
    output = hopfield_net.call(input_data)
    print("Output:", output.numpy())
