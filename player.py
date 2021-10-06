# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:17:17 2021
@author: yadhikari
"""


class player:
    # standard rules key (dealer face-up card): value (player hand total 4:21)
    rule_std = {2: ['H','H','H','H','H','H','D','D','H','S','S','S','S','S','S','S','S','S'],
                3: ['H','H','H','H','H','D','D','D','H','S','S','S','S','S','S','S','S','S'],
                4: ['H','H','H','H','H','D','D','D','S','S','S','S','S','S','S','S','S','S'],
                5: ['H','H','H','H','H','D','D','D','S','S','S','S','S','S','S','S','S','S'],
                6: ['H','H','H','H','H','D','D','D','S','S','S','S','S','S','S','S','S','S'],
                7: ['H','H','H','H','H','H','D','D','H','H','H','H','H','S','S','S','S','S'],
                8: ['H','H','H','H','H','H','D','D','H','H','H','H','H','S','S','S','S','S'],
                9: ['H','H','H','H','H','H','D','D','H','H','H','H','H','S','S','S','S','S'],
                10:['H','H','H','H','H','H','H','D','H','H','H','H','H','S','S','S','S','S'],
                1: ['H','H','H','H','H','H','H','H','H','H','H','H','H','S','S','S','S','S']}
    
    # standard rules key (dealer face-up card): value (player hand total 12:21)
    rule_sft = {2: ['H','H','H','H','H','H','S','S','S','S'],
                3: ['H','H','H','H','H','D','D','S','S','S'],
                4: ['H','H','H','D','D','D','D','S','S','S'],
                5: ['D','D','D','D','D','D','D','S','S','S'],
                6: ['D','D','D','D','D','D','D','S','S','S'],
                7: ['H','H','H','H','H','H','S','S','S','S'],
                8: ['H','H','H','H','H','H','S','S','S','S'],
                9: ['H','H','H','H','H','H','H','S','S','S'],
                10:['H','H','H','H','H','H','H','S','S','S'],
                1: ['H','H','H','H','H','H','H','S','S','S']}
    
    def __init__(self, starting_fund, min_bet = 25):
        self.funds = starting_fund
        self.tally = [self.funds]
        self.c1 = 0
        self.c2 = 0
        self.sum_cards = 0
        self.cards = 2
        
        self.min_bet = min_bet
        self.amt_bet = min_bet
        
        
    def action_simple(self, deal):
        self.cards = 2
        ace = 0
        self.amt_bet = self.min_bet
        
        if self.c1 == 1 and self.c2 != 1 or  self.c1 != 1 and self.c2 == 1:
            ace = 1
            self.sum_cards = self.c1 + self.c2 + 10
        elif self.c1 == 1 and self.c2 == 1:
            ace = 2
            self.sum_cards = self.c1 + self.c2 + 10
        else:
            self.sum_cards = self.c1 + self.c2
            
            
        while self.continue_drawing(ace, deal):
            
            next_c = deal.deal_card()
            self.cards += 1
            self.sum_cards += next_c
            if next_c == 1:
                ace += 1
                self.sum_cards += 10
            
            if self.sum_cards > 21 and ace > 0:
                ace -= 1
                self.sum_cards -= 10
                    
    
    def continue_drawing(self, ace, deal):
        
        # No draw if sum exceeded 21 already
        if self.sum_cards > 21:
            return False
        
        # if black jack ensure that appropriate pay out is given
        
        
        cmd = 'None'
        # Hard hand
        if ace == 0:
            if self.sum_cards >= 4 and self.sum_cards <= 21:
                cmd = self.rule_std[deal.c1][self.sum_cards-4]
            else:
                print("Error in hard hand")
        # Soft hand
        else:
            if self.sum_cards >= 12 and self.sum_cards <= 21:
                cmd = self.rule_sft[deal.c1][self.sum_cards-12]
            else:
                print("Error in soft hand")
        
        if cmd == 'H':
            return True
        elif cmd == 'S':
            return False
        elif cmd == 'D':
            if self.cards > 2:
                return True
            else:
                next_c = deal.deal_card()
                self.amt_bet += self.amt_bet
                self.sum_cards += next_c
                return False
        else:
            print('Error in command')
            return False
        