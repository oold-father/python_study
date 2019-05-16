import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
import warnings

warnings.filterwarnings("ignore")

# 记录传入数据的均值和标准差
def variable_summaries(var):
    with tf.name_scope("summaries"):
        mean = tf.reduce_mean(var)
        tf.summary.scalar("mean",mean)
        with tf.name_scope("stddev"):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var-mean)))
        tf.summary.scalar("stddev", stddev)
        tf.summary.scalar("max", tf.reduce_max(var))
        tf.summary.scalar("min", tf.reduce_min(var))
        tf.summary.histogram("histogram", var)

# 载入mnist数据
mnist = input_data.read_data_sets("data", one_hot=True)

# 图片数量
image_num = 3000
# 文件路径
projector_DIR = r"D:\python\MNIST_data\projector"
meta_DIR = projector_DIR + r"\metadata.tsv"
# 载入图片
embedding = tf.Variable(tf.stack(mnist.test.images[:image_num]),trainable=False,name="embedding")

# 训练批次大小
batch_size = 100
n_batch = mnist.train.num_examples // batch_size

# 命名空间
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32,[None,784],name="x-input")
    y = tf.placeholder(tf.float32,[None,10],name="y-input")

# 显示图片
with tf.name_scope('input_reshape'):
    imge_shaped_input = tf.reshape(x,[-1,28,28,1])
    tf.summary.image("input",imge_shaped_input,10)

# 隐藏层
with tf.name_scope('layer1'):
    Weight_L1 = tf.Variable(tf.random_normal([784,300], stddev=0.2),name="w1")
    biases_L1 = tf.Variable(tf.constant(0.1, shape=[1,300]),name="b1")

    L1 = tf.matmul(x,Weight_L1) + biases_L1
    a1 = tf.nn.relu(L1)

    variable_summaries(Weight_L1)
    variable_summaries(biases_L1)

with tf.name_scope('layer2'):
    Weight_L2 = tf.Variable(tf.random_normal([300,10], stddev=0.2),name="w2")
    biases_L2 = tf.Variable(tf.constant(0,1, shape=[1,10]),name="b2")

    variable_summaries(Weight_L2)
    variable_summaries(biases_L2)

    L2 = tf.matmul(a1,Weight_L2) + biases_L2
    prediction = tf.nn.softmax(L2)

with tf.name_scope('loss'):
    # 损失函数
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=L2,labels=y)
    loss = tf.reduce_mean(cross_entropy)
    tf.summary.scalar("loss", loss)

with tf.name_scope('train'):
    # 自适应学习率优化器
    optimizer = tf.train.AdamOptimizer(0.001)
    train = optimizer.minimize(loss)

with tf.name_scope('acc'):
    # 求准确率
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar("accuracy", accuracy)

# 显示所有的summary
merged = tf.summary.merge_all()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    # 产生metadata文件
    with open(meta_DIR, 'w') as f:
        test_labels = sess.run(tf.argmax(mnist.test.labels[:], 1))
        for i in range(image_num):
            f.write(str(test_labels[i]) + '\n')

    # 保存模型
    saver = tf.train.Saver()

    # 可视化配置
    writer = tf.summary.FileWriter(projector_DIR,sess.graph)
    config = projector.ProjectorConfig()
    embed = config.embeddings.add()
    embed.tensor_name = embedding.name
    embed.metadata_path = meta_DIR
    #
    embed.sprite.image_path = projector_DIR + r'\mnist_10k_sprite.png'
    embed.sprite.single_image_dim.extend([28, 28])
    projector.visualize_embeddings(writer, config)

    for epoch in range(21):
        for batch in range(n_batch):
            i = (batch+1)+epoch*n_batch
            batch_x,batch_y = mnist.train.next_batch(batch_size)
            run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
            run_metadata = tf.RunMetadata()

            _, summary = sess.run([train,merged], feed_dict={x:batch_x, y:batch_y}, \
                                  options=run_options, run_metadata=run_metadata)

            writer.add_run_metadata(run_metadata, "step%03d" % i)
            writer.add_summary(summary, i)

        acc_vali = sess.run(accuracy,feed_dict={x:mnist.validation.images,y:mnist.validation.labels})
        print("iter:",epoch,", validation Accuracy:",acc_vali)

    test_acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
    print("Testing Accuracy:", test_acc)

    saver.save(sess, projector_DIR+r'\mnist_model.ckpt', global_step=n_batch*21)
    print(n_batch*21)
    writer.close()
