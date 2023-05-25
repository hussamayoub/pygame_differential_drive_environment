import tensorflow as tf
import numpy as np
import random
import gym


class Actor(tf.keras.Model):
    def __init__(self, state_dim, action_dim, action_bound):
        super(Actor, self).__init__()
        self.dense1 = tf.keras.layers.Dense(400, activation='relu')
        self.dense2 = tf.keras.layers.Dense(300, activation='relu')
        self.dense3 = tf.keras.layers.Dense(action_dim, activation='tanh')
        self.action_bound = action_bound

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        x = self.dense3(x)
        return self.action_bound * x


class Critic(tf.keras.Model):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()
        self.dense1 = tf.keras.layers.Dense(400, activation='relu')
        self.dense2 = tf.keras.layers.Dense(300, activation='relu')
        self.dense3 = tf.keras.layers.Dense(1)

    def call(self, inputs, actions):
        x = tf.concat([inputs, actions], axis=-1)
        x = self.dense1(x)
        x = self.dense2(x)
        return self.dense3(x)


class DDPG:
    def __init__(self, state_dim, action_dim, action_bound):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_bound = action_bound

        self.actor = Actor(state_dim, action_dim, action_bound)
        self.target_actor = Actor(state_dim, action_dim, action_bound)
        self.critic = Critic(state_dim, action_dim)
        self.target_critic = Critic(state_dim, action_dim)

        self.critic_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.actor_optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

        self.gamma = 0.99
        self.tau = 0.001
        self.batch_size = 64
        self.train_step = 0
        self.target_update_frequency = 10

        self.update_target_networks()

    def update_target_networks(self):
        self.target_actor.set_weights(self.actor.get_weights())
        self.target_critic.set_weights(self.critic.get_weights())

    def train(self, env, num_episodes):
        for episode in range(num_episodes):
            state = env.reset()
            done = False
            total_reward = 0

            while not done:
                env.render()
                action = self.select_action(state)
                next_state, reward, done, _ = env.step(action)

                self.replay_buffer.append((state, action, reward, next_state, done))

                if len(self.replay_buffer) >= self.batch_size:
                    self.train_actor_critic()

                state = next_state
                total_reward += reward

            print(f"Episode {episode + 1}: Total Reward = {total_reward}")

    def select_action(self, state):
        state = np.expand_dims(state, axis=0)
        action = self.actor(state)
        return action.numpy()[0]

    def train_actor_critic(self):
        # minibatch = random.sample(self.replay_buffer, self.batch_size)

        # states = np.array([transition[0] for transition in minibatch])
        # actions = np.array([transition[1] for transition in minibatch])
        # rewards = np.array([transition[2] for transition in minibatch])
        # next_states = np.array([transition[3] for transition in minibatch])
        # dones = np.array([transition[4] for transition in minibatch])

        # with tf.GradientTape() as tape:
        #     target_actions = self.target_actor(next_states)
        #     target_q_values = self.target_critic(next_states, target_actions)
        #     targets = rewards + self.gamma * target_q_values * (1 - dones)
        #     predicted_q_values = self.critic(states, actions)
        #     critic_loss = tf.reduce_mean(tf.square(targets - predicted_q_values))

        # critic_gradients = tape.gradient(critic_loss, self.critic.trainable_variables)
        # self.critic_optimizer.apply_gradients(zip(critic_gradients, self.critic.trainable_variables))

        # with tf.GradientTape() as tape:
        #     predicted_actions = self.actor(states)
        #     actor_loss = -tf.reduce_mean(self.critic(states, predicted_actions))

        # actor_gradients = tape.gradient(actor_loss, self.actor.trainable_variables)
        # self.actor_optimizer.apply_gradients(zip(actor_gradients, self.actor.trainable_variables))

        # self.update_target_networks()

        minibatch = random.sample(self.replay_buffer, self.batch_size)

        states = np.array([transition[0] for transition in minibatch])
        actions = np.array([transition[1] for transition in minibatch])
        rewards = np.array([transition[2] for transition in minibatch])
        next_states = np.array([transition[3] for transition in minibatch])
        dones = np.array([transition[4] for transition in minibatch])

        with tf.GradientTape() as tape:
            target_actions = self.target_actor(next_states)
            target_q_values = self.target_critic(next_states, target_actions)
            targets = rewards + self.gamma * target_q_values * (1 - dones)
            predicted_q_values = self.critic(states, actions)
            critic_loss = tf.reduce_mean(tf.square(targets - predicted_q_values))

        critic_gradients = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic_optimizer.apply_gradients(zip(critic_gradients, self.critic.trainable_variables))

        with tf.GradientTape() as tape:
            predicted_actions = self.actor(states)
            actor_loss = -tf.reduce_mean(self.critic(states, predicted_actions))

        actor_gradients = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor_optimizer.apply_gradients(zip(actor_gradients, self.actor.trainable_variables))

        # Update target networks with a delay
        
        self.update_target_networks()

        # Decay exploration noise
        # exploration_noise *= self.exploration_decay_factor

        self.train_step += 1