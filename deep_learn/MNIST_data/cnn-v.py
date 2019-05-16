import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import warnings

def init_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def init_biases(shape):
    return tf.Variable(tf.constant(0.1,shape=shape))

def conv2d(x,w,padding='SAME'):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding=padding)

def pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

warnings.filterwarnings("ignore")

mnist = input_data.read_data_sets("data/",one_hot="True")#one_hot取值为向量

# 训练批次大小
batch_size = 100

n_batch = mnist.train.num_examples // batch_size

x = tf.placeholder(tf.float32,[None,784])
y = tf.placeholder(tf.float32,[None,10])
x_img = tf.reshape(x,[-1,28,28,1])


#神经网络层
#第一层卷积，池化层
#过滤器：长宽5x5，步长1，全0填充，深度6
#激活函数relu
#最大池化，步长为2
w_conv1 = init_weights([5,5,1,32])
b_conv1 = init_biases([32])

h_covn1 = tf.nn.bias_add(conv2d(x_img,w_conv1),b_conv1)
h_relu1 = tf.nn.relu(h_covn1)

h_pool1 = pool_2x2(h_relu1)

#第二层卷积，池化层
#过滤器：长宽5x5，步长1，不填充，深度16
#激活函数relu
#最大池化，步长为2
w_conv2 = init_weights([5,5,32,64])
b_conv2 = init_biases([64])
h_covn2 = tf.nn.bias_add(conv2d(h_pool1,w_conv2),b_conv2)
h_relu2 = tf.nn.relu(h_covn2)

h_pool2 = pool_2x2(h_relu2)

#第一个全连接层，节点数120
w_fc1 = init_weights([7*7*64,120])
b_fc1 = init_biases([120])

h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1)+b_fc1)

#第二层全连接，节点84
w_fc2 = init_weights([120,84])
b_fc2 = init_biases([84])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1,w_fc2)+b_fc2)

#第三层全连接，节点10
w_fc3 = init_weights([84,10])
b_fc3 = init_biases([10])
output = tf.nn.relu(tf.matmul(h_fc2,w_fc3)+b_fc3)
prediction = tf.nn.softmax(output)
#神经网络层结束

#损失函数
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=output,labels=y)
loss = tf.reduce_mean(cross_entropy)


# 自适应学习率优化器
optimizer = tf.train.AdamOptimizer(1e-4)
train = optimizer.minimize(loss)


# 求准确率
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(21):
        for batch in range(n_batch):
            batch_x,batch_y = mnist.train.next_batch(batch_size)
            sess.run(train,feed_dict={x:batch_x,y:batch_y})

        acc_vali = sess.run(accuracy,feed_dict={x:mnist.validation.images,y:mnist.validation.labels})
        print("iter:",epoch,", validation Accuracy:",acc_vali)

    test_acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
    print("Testing Accuracy:", test_acc)