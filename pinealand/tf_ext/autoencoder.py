import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from keras import layers

if __name__ == '__main__':
    # 加载图像数据
    (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()

    # 数据预处理
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # 将图像从二维矩阵转换为一维向量
    x_train = x_train.reshape((len(x_train), -1))
    x_test = x_test.reshape((len(x_test), -1))

    # 定义编码器和解码器网络结构
    input_dim = x_train.shape[1]
    encoding_dim = 32

    # 编码器
    encoder_input = layers.Input(shape=(input_dim,))
    encoder_output = layers.Dense(encoding_dim, activation='relu')(encoder_input)

    # 解码器
    decoder_output = layers.Dense(input_dim, activation='sigmoid')(encoder_output)

    # 构建自动编码器模型
    autoencoder = tf.keras.Model(encoder_input, decoder_output)

    # 编译自动编码器模型
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

    # 训练自动编码器模型
    autoencoder.fit(x_train, x_train, epochs=10, batch_size=128, validation_data=(x_test, x_test))

    # 使用训练好的自动编码器进行数据重构
    reconstructed_data = autoencoder.predict(x_test)

    # 选择要展示的图像数量
    num_images = 5

    # 从测试数据中选择随机的图像索引
    random_indexes = np.random.randint(0, len(x_test), num_images)

    # 显示原始图像和重构图像
    for i, index in enumerate(random_indexes):
        # 原始图像
        original_image = x_test[index].reshape(28, 28)
        # 重构图像
        reconstructed_image = reconstructed_data[index].reshape(28, 28)

        # 绘制原始图像
        plt.subplot(2, num_images, i + 1)
        plt.imshow(original_image, cmap='gray')
        plt.title("Original")
        plt.axis('off')

        # 绘制重构图像
        plt.subplot(2, num_images, num_images + i + 1)
        plt.imshow(reconstructed_image, cmap='gray')
        plt.title("Reconstructed")
        plt.axis('off')

    # 展示图像
    plt.show()
