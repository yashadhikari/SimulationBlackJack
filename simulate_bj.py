# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:56:34 2021
Assumptions:
    
    - Number of hands / minute is set to 2
    - Player is allowed to go negative (assuming a re-buy). Otherwise, results 
    maybe skewed towards the player with lower bound of 0 and no upper bound.
    
    
@author: yadhikari
"""

from player import player
from dealer import dealer
import matplotlib.pyplot as plt
import numpy as np

def simulate(hours_played = 1, players = 1, decks = 8, iterate = 1000, min_bet = 25):
    
    def distribute(player_list, deal):
        # Distribute cards to all players and the dealer in typical order
        for obj in player_list:
            obj.c1 = [deal.deal_card()]     # requires card to be in a list
        deal.c1 = deal.deal_card()
        for obj in player_list:
            obj.c2 = [deal.deal_card()]     # requires card to be in a list
        deal.c2 = deal.deal_card()
    
    def update_funds(player_list, deal):
        # Subtract or add player funds based on win or loss
        
        
        for obj in player_list:
            for i in range(obj.hands):
                
                obj.hands_total += 1
                
                # player black jack
                if obj.sum_cards[i] == 21 and obj.cards[i] == 2 and not(deal.sum_cards == 21 and deal.cards == 2):
                    obj.funds += obj.amt_bet[i] * (3/2)
                    
                    obj.hands_won += 1
                    
                # dealer black jack
                elif deal.sum_cards == 21 and deal.cards == 2:
                    obj.funds -= obj.amt_bet[i]
                # player bust (happens first)
                elif obj.sum_cards[i] > 21:
                    obj.funds -= obj.amt_bet[i]
                # dealer bust (happens after player's turn)
                elif deal.sum_cards > 21:
                    obj.funds += obj.amt_bet[i]
                    
                    obj.hands_won += 1
                    
                # dealer vs. player (nothing happens if they are equal)
                elif obj.sum_cards[i] > deal.sum_cards:
                    obj.funds += obj.amt_bet[i]
                    
                    obj.hands_won += 1
                    
                elif obj.sum_cards[i] < deal.sum_cards:
                    obj.funds -= obj.amt_bet[i]
                
                obj.tally.append(obj.funds)
            obj.hands = 1 # reset for splits
            
            
#            print( obj.c1, obj.c2, obj.sum_cards, obj.cards, deal.c1, deal.c2, deal.sum_cards, deal.cards, obj.funds)
   
    def analyze(funds_tally, history_tally, hours_played, iterate, players, hands_tally, won_tally):
        # Plot the analysis
        print(funds_tally)
        print(sum(funds_tally)/len(funds_tally))
        print('Number of times player is positive: ', len(np.where(np.array(funds_tally) >= 300)[0]))
        print('Total times: ', len(funds_tally))
        no_rebuy_total = sum(np.array(funds_tally)[np.where(np.array(funds_tally) >= 0)]) - iterate*300*players
        rebuy_total = sum(funds_tally) - iterate*300*players
        print('Total result if no re-buy: ', no_rebuy_total, '\tAverage: ', no_rebuy_total/(iterate*players))
        print('Result if re-buy: ', rebuy_total, '\tAverage: ', rebuy_total/(iterate*players))
        
        print('Number of total hands: ', sum(hands_tally), 'Number of hands won: ', sum(won_tally))
        
        for h in history_tally:
            plt.plot(h)
        plt.plot([300]*hours_played*120, )
        plt.xlabel("Hand Number")
        plt.ylabel("Total Funds")
        plt.title("Funds Over Time")
        plt.show()
        
    funds_tally = []
    history_tally = []
    hands_tally = []
    won_tally = []
    
    for iteration in range(1,iterate+1):
    
        # create all players including the dealer which controls the deck
        player_list = []
        for i in range(players):
            player_list.append(player(300))
        deal = dealer(decks)
        
        # Run for x iterations that represent the number of hands played within a 
        # time period (2 hands/minute)
        hands = hours_played*120
        for i in range(1, hands+1):
            # Distribute cards to all players while 'hiding' the dealer's 2nd card
            distribute(player_list, deal)
            # Allow player(s) to take action based on dealer's face-up card
            for obj in player_list:
                obj.action_simple(deal)
            # Complete dealer's action
            deal.action()
            # Tally player's money
            update_funds(player_list, deal)
            # Reset deck if its close to being empty (> 87.5% complete)
            if deal.reset_deck:
                deal.init_deck()
                
            
        for obj in player_list:
            funds_tally.append(obj.funds)
            history_tally.append(obj.tally)
            
            hands_tally.append(obj.hands_total)
            won_tally.append(obj.hands_won)
            
    analyze(funds_tally, history_tally, hours_played, iterate, players, hands_tally, won_tally)
    

if __name__ == "__main__":
    simulate()