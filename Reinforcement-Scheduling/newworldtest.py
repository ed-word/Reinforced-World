import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

from myWorld import myEnv

env = myEnv()

gamma = 0.99

def discount_rewards(r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


class Agent():
    def __init__(self, lr, s_size, a_size, h_size):
        # These lines established the feed-forward part of the network. The agent takes a state and produces an action.
        s_shape = [None]
        s_shape.extend(s_size)
        self.state_in = tf.placeholder(shape=s_shape, dtype=tf.float32)
        flattened = slim.flatten(self.state_in)
        hidden = slim.fully_connected(flattened, h_size, biases_initializer=None, activation_fn=tf.nn.relu)
        self.output = slim.fully_connected(hidden, a_size, activation_fn=tf.nn.softmax, biases_initializer=None)
        self.chosen_action = tf.argmax(self.output, 1)

        # The next six lines establish the training proceedure. We feed the reward and chosen action into the network
        # to compute the loss, and use it to update the network.
        self.reward_holder = tf.placeholder(shape=[None], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[None], dtype=tf.int32)

        self.indexes = tf.range(0, tf.shape(self.output)[0]) * tf.shape(self.output)[1] + self.action_holder
        self.responsible_outputs = tf.gather(tf.reshape(self.output, [-1]), self.indexes)

        self.loss = -tf.reduce_mean(tf.log(self.responsible_outputs) * self.reward_holder)

        tvars = tf.trainable_variables()
        self.gradient_holders = []
        for idx, var in enumerate(tvars):
            placeholder = tf.placeholder(tf.float32, name=str(idx) + '_holder')
            self.gradient_holders.append(placeholder)

        self.gradients = tf.gradients(self.loss, tvars)

        optimizer = tf.train.AdamOptimizer(learning_rate=lr)
        self.update_batch = optimizer.apply_gradients(zip(self.gradient_holders, tvars))


tf.reset_default_graph()

myAgent =Agent(lr=1e-2, s_size=(31,31,5), a_size=4, h_size=32)


total_episodes = 5000
max_ep = 999
update_frequency = 5

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    i = 0
    total_reward = []
    total_lenght = []

    gradBuffer = sess.run(tf.trainable_variables())
    for ix, grad in enumerate(gradBuffer):
        gradBuffer[ix] = grad * 0

    while i < total_episodes:
        s = env.reset()
        running_reward = 0
        ep_history_s = []
        ep_history_a = []
        ep_history_r = []
        for j in range(max_ep):
            a_dist = sess.run(myAgent.output, feed_dict={myAgent.state_in: [s]})
            p = np.random.random()
            if p <= 0.3:
                a = np.random.randint(0,3)
            else:
                a = np.argmax(a_dist)

            s1, d, r = env.execute(a)

            ep_history_s.append(s)
            ep_history_a.append(a)
            ep_history_r.append(r)
            s = s1
            running_reward += r
            if d:
                ep_history_r = discount_rewards(np.array(ep_history_r))
                feed_dict = {myAgent.reward_holder: ep_history_r,
                             myAgent.action_holder: ep_history_a, myAgent.state_in: ep_history_s}
                grads = sess.run(myAgent.gradients, feed_dict=feed_dict)
                for idx, grad in enumerate(grads):
                    gradBuffer[idx] += grad

                if i % update_frequency == 0 and i != 0:
                    feed_dict = dictionary = dict(zip(myAgent.gradient_holders, gradBuffer))
                    _ = sess.run(myAgent.update_batch, feed_dict=feed_dict)
                    for ix, grad in enumerate(gradBuffer):
                        gradBuffer[ix] = grad * 0

                total_reward.append(running_reward)
                total_lenght.append(j)
                break

        if i % 100 == 0:
            print(np.mean(total_reward[-100:]))
        i += 1
