#Tensorboard
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import numpy as np
import warnings


projector_DIR = r"D:\python\MNIST_data\model"

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def init_biases(shape):
    return tf.Variable(tf.zeros(shape))

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

#监控函数
def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean',mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var-mean)))
        tf.summary.scalar('stddev',stddev)
        tf.summary.scalar('max',tf.reduce_max(var))
        tf.summary.scalar('min',tf.reduce_min(var))
        tf.summary.histogram('histogram',var)

warnings.filterwarnings("ignore")

mnist = input_data.read_data_sets("data/",one_hot="True")#one_hot取值为向量

#训练批次大小
batch_size = 50
n_batch =    mnist.train.num_examples //batch_size
#训练次数
epoch_count = 20
#dropout概率
keep_input = 0.7
keep_hidden = 0.75

with tf.name_scope('input'):
  x = tf.placeholder(tf.float32,[None,784],name="x-input")
  y = tf.placeholder(tf.float32,[None,10],name='y-input')

#显示图片
with tf.name_scope('input_reshape'):
    image_shaped_input = tf.reshape(x,[-1,28,28,1])
    tf.summary.image('input',image_shaped_input,10)

p_keep_input = tf.placeholder(tf.float32)
p_keep_hidden = tf.placeholder(tf.float32)

with tf.name_scope('layer1'):
    weights_1 = init_weights([784,500])
    biases_1 =  init_biases([1,500])
    prediction_1,output_1 = model_sigmoid(x,weights_1,biases_1,p_keep_input)
    variable_summaries(weights_1)
    variable_summaries(biases_1)

with tf.name_scope('layer2'):
    weights_2 = init_weights([500,100])
    biases_2 =  init_biases([1,100])
    prediction_2,output_2 = model_sigmoid(prediction_1,weights_2,biases_2,p_keep_hidden)
    variable_summaries(weights_2)
    variable_summaries(biases_2)


with tf.name_scope('layer3'):
    weights =   init_weights([100,10])
    biases =    init_biases([1,10])
    prediction,output =     model_softmax(prediction_2,weights,biases)
    variable_summaries(weights)
    variable_summaries(biases)

with tf.name_scope('loss'):
    loss =         tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    tf.summary.scalar('loss',loss)

with tf.name_scope('train'):
    train =        tf.train.AdamOptimizer(0.001).minimize(loss)

with tf.name_scope('acc'):
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(output,1))
    accuracy           = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    tf.summary.scalar('accuracy', accuracy)

merged = tf.summary.merge_all()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #保存模型
    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(projector_DIR,sess.graph)
    #写入日志
    #writer = tf.summary.FileWriter('logs/',sess.graph)
    for epoch in range(epoch_count):
      for batch in range(n_batch):
        i = (batch+1)+epoch*n_batch
        batch_x,batch_y = mnist.train.next_batch(batch_size)
        run_options = tf.RunOptions(trace_level = tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        #列表形式跑两个session
        _,summary = sess.run([train,merged],feed_dict={x:batch_x,y:batch_y, p_keep_input: keep_input, p_keep_hidden: keep_hidden},options=run_options,run_metadata=run_metadata)



        #查看所有监控
        writer.add_run_metadata(run_metadata,'step%03d'%i)
        writer.add_summary(summary,i) 
      #writer.add_summary(summary,epoch)  
      acc_vali = sess.run(accuracy,feed_dict={x:mnist.validation.images,y:mnist.validation.labels,p_keep_input: 1., p_keep_hidden: 1.})
      print("iter:",epoch,",vilidation Accuracy:",acc_vali)
    test_acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,p_keep_input: 1., p_keep_hidden: 1.})
    print("Testing Accuracy:",test_acc)

    #保存训练模型
    saver.save(sess,projector_DIR+'/mnist_model.ckpt',global_step=n_batch*epoch_count)
    writer.close()


