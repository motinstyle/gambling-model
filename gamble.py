import numpy as np
import math
import matplotlib.pyplot as plt

class Player:
    def __init__(self, balance, gamble, goal, max_loss):
        self.balance = balance
        self.start_balance = balance
        self.gamble = gamble
        self.goal = goal
        self.max_loss = max_loss
        # self.max_loss = -1*(self.start_balance + self.goal)*self.gamble
        self.iterations = 0
        self.ready = True

    def update(self, price, reward):
        self.balance += reward - price
        self.iterations += 1
        self.ready = True if self.balance >= self.max_loss and self.balance <= self.goal*(1+self.gamble) else False

    def __str__(self):
        return f"{self.start_balance:5d} | {self.balance:7d} | {self.gamble:0.5f} | {self.goal:5d} | {self.max_loss:8f} | {self.iterations:5d}"

class RandomBox:
    def __init__(self, probs, rewards, price):
        self.probs = probs
        self.rewards = rewards
        self.price = price

    def correction(self):
        if len(self.probs) != len(self.rewards):
            print("incorrect num of rewards or probs")
            return False
        elif np.sum(self.probs) != 1.0:
            return False
        return True

    def expected_value(self):
        print("expected: ", np.dot(self.rewards-self.price, self.probs))
    
    def play(self):
        return np.random.choice(a=self.rewards, p=self.probs)


def main():

    # players
    num_of_palyers = 1000
    num_of_ready = num_of_palyers
    players = [
                Player(
                    np.random.randint(10,500),
                    np.random.random(),
                    0,
                    -1*np.random.randint(0, 200))
                    for i in range(num_of_palyers) 
              ]
    for player in players:
        player.goal = player.balance + np.random.randint(player.balance, player.balance*np.random.randint(2, math.ceil(3+player.gamble*10)))
        player.max_loss = -1*(player.start_balance + player.goal)*player.gamble  


    # random box
    probs = np.array([0.4, 0.35, 0.15, 0.05, 0.03, 0.02])
    rewards = np.array([1.25, 10, 15, 25, 50, 100])
    price = 11
    box = RandomBox(probs=probs, rewards=rewards, price=price)
    box.correction()
    box.expected_value()


    # main loop
    for i in range(10000):
        num_of_ready = 0
        for player in players:
            if player.ready:
                reward = box.play()
                player.update(price=box.price, reward=reward)
                num_of_ready += 1
        if num_of_ready == 0:
            break        
    
    # results
    more_then_zero = 0
    profited = 0
    # print(f"start | balance | gamble  | goal  | max_loss | iters")
    players.sort(key=lambda player: player.balance - player.start_balance)
    for player in players:
        if player.balance > 0:
            more_then_zero += 1
        if player.balance > player.start_balance:
            profited += 1    
        # print(player)
    print("more then zero", more_then_zero, "/", len(players))
    print("profited", profited, "/", len(players))
    plt.plot([player.balance - player.start_balance for player in players], [player.iterations for player in players], linestyle="",marker="o")
    plt.show()

if __name__ == "__main__":
    main()