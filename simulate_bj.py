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

def simulate(hours_played = 2, players = 1, decks = 8, iterate = 100, min_bet = 25):
    
    def distribute(player_list, deal):
        
        for obj in player_list:
            obj.c1 = deal.deal_card()
        deal.c1 = deal.deal_card()
        for obj in player_list:
            obj.c2 = deal.deal_card()
        deal.c2 = deal.deal_card()
            
    funds_tally = []
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
                obj.action_simple(deal.c1)
            
            # Complete dealer's action
            deal.action()
            
            # Tally player's money
            
            # Reset deck if its close to being empty (> 87.5% complete)
            if deal.reset_deck:
                deal.init_deck()
            
        for obj in player_list:
            funds_tally.append(obj.funds)
        
    print(funds_tally)

if __name__ == "__main__":
    simulate()