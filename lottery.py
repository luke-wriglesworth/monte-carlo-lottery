import random
import matplotlib.pyplot as plt

class LotterySimulation:
    def __init__(self, ticket_cost=2, odds_of_winning=0.0000000300347201, jackpot_value=40000000,
                 weeks_to_simulate=520520):

        self.ticket_cost = ticket_cost
        self.odds_of_winning = odds_of_winning
        self.jackpot_value = jackpot_value
        self.weeks_to_simulate = weeks_to_simulate
        self.weeks_simulated = 0
        self.money_won = 0
        self.money_spent = 0

    # Getters and Setters for plotting portion of lab
    def get_ticket_cost(self):
        return self.ticket_cost

    def get_money_spent(self):
        return self.money_spent

    def set_money_spent(self, money):
        self.money_spent += money

    def get_money_won(self):
        return self.money_won

    def set_money_won(self):
        self.money_won += self.jackpot_value

    def set_weeks_simulated(self):
        self.weeks_simulated += 1

    def get_weeks_simulated(self):
        return self.weeks_simulated

    # If weeks to simulate is zero, the simulation will run until a jackpot is won, otherwise it
    # will run to the specified weeks argument
    def run_simulation(self):
        if self.weeks_to_simulate > 0:
            for week in range(self.weeks_to_simulate):
                self.money_spent += self.ticket_cost
                self.weeks_simulated += 1
                lottery_result = self.play_lottery()
                if lottery_result:
                    self.money_won += self.jackpot_value
        else:
            while self.money_won == 0:
                self.money_spent += self.ticket_cost
                self.weeks_simulated += 1
                lottery_result = self.play_lottery()
                if lottery_result:
                    self.money_won += self.jackpot_value

    def play_lottery(self):
        # Generates float between 0 and 1, and checks if the number is less than odds of winning.
        # If it is less than odds of winning then it will be a jackpot
        lottery_num = random.random()
        if lottery_num < self.odds_of_winning:
            return True
        else:
            return False

    # Returns a summary of the simulation
    def get_summary(self):
        return f'Money spent:     {self.money_spent}\n' \
               f'Money won:       {self.money_won}\n' \
               f'Weeks simulated: {self.weeks_simulated}'


lottery = LotterySimulation(odds_of_winning=0.0000000300347201, weeks_to_simulate=52000000)

# Week counter counts up to 100 and then the data at that point will be appended to the lists
week_counter = 0
# Empty lists where the plotting points will be appended
weeks_simulated = []
money_spent = []
money_won = []
net_profit = []

for week in range(lottery.weeks_to_simulate):
    # Updates lottery instance variables every week
    result = lottery.play_lottery()
    lottery.set_money_spent(lottery.get_ticket_cost())
    lottery.set_weeks_simulated()

    # If it's a win
    if result:
        lottery.set_money_won()

    # Every 100 years (approximately 5200 weeks) the data will be recorded to the lists
    if week_counter == 5200:
        money_spent.append(lottery.get_money_spent())
        money_won.append(lottery.get_money_won())
        net_profit.append(lottery.get_money_won() - lottery.get_money_spent())
        weeks_simulated.append(week)
        week_counter = 0
    week_counter += 1

# Creates the plot, and exports as image
profit_plot, = plt.plot(weeks_simulated, net_profit)
spend_plot, = plt.plot(weeks_simulated, money_spent)
won_plot, = plt.plot(weeks_simulated, money_won)
plt.legend((profit_plot, spend_plot, won_plot), ("Net Profit", "Money Spent", "Money Won"))
plt.xlabel("Weeks")
plt.ylabel("Money")
figure = plt.gcf()
figure.set_size_inches(8.0, 6.0)
figure.savefig('lottery_profit.png', dpi=100, format="png")
plt.show()
