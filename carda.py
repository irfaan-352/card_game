import random
import threading
import time


class MiniCasino:

    def __init__(self):
        self.chosen_players = []
        self.pl_points = []
        self.pl_names = []

    def get_players(self, players_count):
        player_lst = []
        for player in range(1, players_count + 1):
            if player == 1:
                print("\nEnter the player details below")
            name = str(input("\nEnter the player name:"))
            age = int(input("Enter player's age:"))
            initial_points = int(input("Enter initial points:"))
            pl_tuple = (name, age,initial_points )
            if pl_tuple:
                player_lst.append(pl_tuple)
        return player_lst

    def choose_player(self, players):
        Mini.chosen_players = random.sample(players, 2)
        if Mini.chosen_players:
            for i in Mini.chosen_players:
                Mini.pl_points.append(i[2])
                Mini.pl_names.append(i[0])

    @classmethod
    def deck(cls):  # a deck of 52 cards is created once this function is called
        card_colors = ["red", "black"]
        card_symbols = ['diamond', 'hearts', 'spades', 'club']
        cards = range(1, 14)
        map_dict = dict()
        for color in card_colors:
            if color == "red":
                map_dict[color] = card_symbols[:2]
            elif color == "black":
                map_dict[color] = card_symbols[2:]
        deck = []
        # color, symbol, number in a card --> Eg: ("red","diamond",4)
        for color in map_dict.keys():
            symbols = map_dict[color]
            for symbol in symbols:
                for card_num in cards:
                    card = (color, symbol, card_num)
                    deck.append(card)
        return deck

    def reward_points(self,cards):
        rew_points = []
        card_color = [color[0] for color in cards]
        card_type = [c_type[1] for c_type in cards]
        card_num = [num[2] for num in cards]
        num_pts = [rew_points.append(5) for pts in card_num if pts > 10]
        color_pts = [rew_points.append(2) if col == "red" else rew_points.append(1) for col in card_color]
        for c_type in card_type:
            if c_type == "hearts":
                rew_points.append(5)
            elif c_type == "diamond":
                rew_points.append(3)
            elif c_type == "club":
                rew_points.append(2)
            elif c_type == "spades":
                rew_points.append(1)
        rew_points = sum(rew_points)
        return rew_points

    def calculate_score_and_bet(self,trial,trial_dct,pp1,pp2,Balance1,Balance2):
        cmp_lst = []
        for player,score in trial_dct.items():
            cmp_lst.append(score)
        max_val = max(cmp_lst)
        winner = [k for k,v in trial_dct.items() if v == max_val]
        Players = list(trial_dct.keys())
        print(f"\n{winner[0]} wins this trial")
        if winner[0] == Players[0]:
            rew_pt = abs(pp1-pp2)
            print(f"Reward point for trial {trial} is {rew_pt}")
            pp1 += rew_pt
            print(f"Reward point of {Players[0]} is {pp1}")
            Balance1 += rew_pt
            print(f"Balance of {Players[0]} is {Balance1}")
            pp2 -= rew_pt
            print(f"Reward point of {Players[1]} is {pp2}")
            Balance2 -= rew_pt
            print(f"Balance of {Players[1]} is {Balance2}")
        else:
            rew_pt = abs(pp2 - pp1)
            print(f"Reward point for trial {trial} is {rew_pt}")
            pp1 -= rew_pt
            print(f"Reward point of {Players[0]} is {pp1}")
            Balance1 -= rew_pt
            print(f"Balance of {Players[0]} is {Balance1}")
            pp2 += rew_pt
            print(f"Reward point of {Players[1]} is {pp2}")
            Balance2 += rew_pt
            print(f"Balance of {Players[1]} is {Balance2}")
        return winner[0],pp1,pp2,Balance1,Balance2

    def random_trials(self,trials,players,deck,pp1,pp2,Balance1,Balance2):

        trial_dict = {}
        winner_list = []
        for trial in range(1,int(trials)+1):
            trial_dict[trial] = {}
            if Balance1 <= 0 or Balance2 <= 0 or pp1 <= 0 or pp2 <= 0:
                print("\n0 Balance or point detected! Can't proceed")
                break
            for player in players:
                sample = random.sample(MiniCasino.deck(), 5)
                pl_pt = Mini.reward_points(sample)
                trial_dict[trial][player[0]] = pl_pt
            r_winner,point1,point2,Bal1,Bal2 = Mini.calculate_score_and_bet(trial,trial_dict[trial],pp1,pp2,Balance1,Balance2)
            winner_list.append(r_winner)
            pp1 = point1
            pp2 = point2
            Balance1 = Bal1
            Balance2 = Bal2
        fb1 = Balance1
        fb2 = Balance2
        return trial_dict,winner_list,fb1,fb2

Mini = MiniCasino()
print("\nWELCOME TO MINI CASINO")
players_count = int(input("\nEnter the no of players :"))
if not players_count >= 5:
    print(f"\n Not enough players to play")
else:
    players = Mini.get_players(players_count)
    deck = threading.Thread(target=MiniCasino.deck, args=())
    choose = threading.Thread(target=Mini.choose_player,args=(players,))
    deck.start()
    choose.start()
    start_time = time.time()
    deck.join()
    choose.join()
    end_time = time.time()
    print(f"Execution time between two threads is {end_time-start_time}")
    print(f"\nThe chosen players are {Mini.chosen_players[0][0]} and {Mini.chosen_players[1][0]}")
    pp1 = Mini.pl_points[0]
    pp2 = Mini.pl_points[1]
    no_of_trials = input("\nEnter the no of trials :")
    Balance_1 = int(input(f"\nEnter {Mini.pl_names[0]} betting amount :"))
    Balance_2 = int(input(f"Enter {Mini.pl_names[1]} betting amount :"))
    trial_out,winner_lst,fbal1,fbal2 = Mini.random_trials(no_of_trials,Mini.chosen_players,deck,pp1,pp2,Balance_1,Balance_2)
    print(f"\n-------winner for each round {winner_lst}-------")
    count_1 = winner_lst.count(Mini.pl_names[0])
    count_2 = winner_lst.count(Mini.pl_names[1])
    if count_1>count_2:
        print(f"\n{Mini.pl_names[0]} wins the most of rounds")
    elif count_2>count_1:
        print(f"\n{Mini.pl_names[1]} wins the most of rounds")
    else:
        print("\nDraw in term of trials")
    if fbal1 > fbal2:
        print(f"\n{Mini.pl_names[0]} has the most cash after the trials")
    elif fbal2 > fbal1:
        print(f"\n{Mini.pl_names[1]} has the most cash after the trials")
    else:
        print(f"\n Tie in cash after all rounds")


