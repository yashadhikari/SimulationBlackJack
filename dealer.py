# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:30:36 2021
@author: yadhikari
"""
import random
import numpy as np


class dealer:
    def __init__(self, num_decks = 8):
        # Initialize deck and dealer specific variables
        self.deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]*(4*num_decks)
        self.c1 = 0
        self.c2 = 0
        
        self.reset_deck = False
        self.randomize()
        self.sum_cards = 0
        self.cards = 2
        
        self.num_decks = num_decks
        
    def action(self):
        # Dealer has simple rules that it follows which are slightly different 
        # when there is a soft 17
        ace = 0
        self.cards = 2
        if self.c1 == 1 and self.c2 != 1 or  self.c1 != 1 and self.c2 == 1:
            ace = 1
            self.sum_cards = self.c1 + self.c2 + 10
        elif self.c1 == 1 and self.c2 == 1:
            ace = 2
            self.sum_cards = self.c1 + self.c2 + 10
        else:
            self.sum_cards = self.c1 + self.c2
            
        while ace == 0 and self.sum_cards < 17 or ace > 0 and self.sum_cards < 18:
            
            next_c = self.deal_card()
            self.sum_cards += next_c
            self.cards += 1
            if next_c == 1:
                ace += 1
                self.sum_cards += 10
            
            if self.sum_cards > 21 and ace > 0:
                ace -= 1
                self.sum_cards -= 10
    
    def randomize(self):
        # returns a shuffled deck
        np.random.shuffle(self.deck)
        
    def init_deck(self):
        # shuffle a new deck
        self.deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]*(4*self.num_decks)
        self.randomize()
        self.reset_deck = False
        
    def deal_card(self):
        # reset_deck is set to true if most of the deck has been used up
        # return the last card on deck (pop it out)
        if len(self.deck)-1 < 0.125*(52*self.num_decks):
            self.reset_deck = True
        return self.deck.pop()