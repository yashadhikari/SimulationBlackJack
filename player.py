# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:17:17 2021

@author: yadhikari
"""


class player:
    def __init__(self, starting_fund, min_bet = 25):
        self.funds = starting_fund
        self.c1 = 0
        self.c2 = 0
        self.sum_cards = 0
        
        self.min_bet = min_bet
        self.amt_bet = min_bet
        
        
    def action_simple(self, dealer_c1):
        cards = 2
        ace = 0
        if self.c1 == 1 and self.c2 != 1 or  self.c1 != 1 and self.c2 == 1:
            ace = 1
            self.sum_cards = self.c1 + self.c2 + 10
        elif self.c1 == 1 and self.c2 == 1:
            ace = 2
            self.sum_cards = self.c1 + self.c2 + 10
        else:
            self.sum_cards = self.c1 + self.c2
            
            
        while self.continue_drawing(ace, cards, dealer_c1):
            
            next_c = self.deal_card()
            self.sum_cards += next_c
            if next_c == 1:
                ace += 1
                self.sum_cards += 10
            
            if self.sum_cards > 21 and ace > 0:
                ace -= 1
                self.sum_cards -= 10
                    
    def double(self, ace, dealer_c1):
        if ace == 0:
            if self.sum_cards == 11:
                return True
            elif self.sum_cards == 10 and dealer_c1 < 10 and dealer_c1 > 1:
                return True
            elif 
        else:
            pass
    def continue_drawing(self, ace, cards, dealer_c1):
        
        if cards == 2 and self.double(ace, dealer_c1):
            self.amt_bet += self.amt_bet
            next_c = self.deal_card()
            self.sum_cards += next_c
            if next_c == 1 and self.sum_cards + 10 <= 21:
                self.sum_cards += 10
            
            return False
        
        return False