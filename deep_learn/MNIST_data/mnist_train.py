import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")

mnist = input_data.read_data_sets("data/",one_hot="True")#one_hot取值为向量

#训练批次大小
batch_size = 50
n_batch =    mnist.train.num_examples //batch_size

x =            tf.placeholder(tf.float32,[None,784])
y =            tf.placeholder(tf.float32,[None,10])

p_keep_input = tf.placeholder(tf.float32)
p_keep_hidden = tf.placeholder(tf.float32)

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def init_biases(shape):
    return tf.Variable(tf.zeros(shape))

weights_1 = init_weights([784,500])
biases_1 =  init_biases([1,500])

weights_2 = init_weights([500,100])
biases_2 =  init_biases([1,100])

weights =   init_weights([100,10])
biases =    init_biases([1,10])

def model_softmax(x,weight,biase,drop = 1):
    output =     tf.matmul(x,weight)+biase
    prediction = tf.nn.softmax(output)
    prediction = tf.nn.dropout(prediction,drop)
    return prediction,output

def model_sigmoid(x,weight,biase,drop = 1):
    output =     tf.matmul(x,weight)+biase
    prediction = tf.nn.sigmoid(output)
    prediction = tf.nn.dropout(prediction,drop)
    return prediction,output

prediction_1,output_1 = model_sigmoid(x,weights_1,biases_1,p_keep_input)
prediction_2,output_2 = model_sigmoid(prediction_1,weights_2,biases_2,p_keep_hidden)
prediction,output =     model_softmax(prediction_2,weights,biases)

loss =         tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
#train =        tf.train.RMSPropOptimizer(0.001, 0.9).minimize(loss)
train =        tf.train.AdamOptimizer(0.001).minimize(loss)

#求准确率
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(output,1))
accuracy           = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

epoch_count = 20
keep_input = 0.7
keep_hidden = 0.75

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(epoch_count):
      for batch in range(n_batch):
        batch_x,batch_y = mnist.train.next_batch(batch_size)
        sess.run(train,feed_dict={x:batch_x,y:batch_y, p_keep_input: keep_input, p_keep_hidden: keep_hidden})
        
      acc_vali = sess.run(accuracy,feed_dict={x:mnist.validation.images,y:mnist.validation.labels,p_keep_input: 1., p_keep_hidden: 1.})
      print("iter:",epoch,",vilidation Accuracy:",acc_vali)
    test_acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,p_keep_input: 1., p_keep_hidden: 1.})
    print("Testing Accuracy:",test_acc)



