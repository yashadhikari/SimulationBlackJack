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
    
    # soft hand rules key (dealer face-up card): value (player hand total 12:21)
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
    
    # Paired hand rules key (dealer face-up card): value (player hand 1:10)
    rule_pair = {2: ['P','P','P','H','D','P','P','P','P','S'],
                3: ['P','P','P','H','D','P','P','P','P','S'],
                4: ['P','P','P','H','D','P','P','P','P','S'],
                5: ['P','P','P','P','D','P','P','P','P','S'],
                6: ['P','P','P','P','D','P','P','P','P','S'],
                7: ['P','P','P','H','D','H','P','P','S','S'],
                8: ['P','H','H','H','D','H','H','P','P','S'],
                9: ['P','H','H','H','D','H','H','P','P','S'],
                10:['P','H','H','H','H','H','H','P','S','S'],
                1: ['P','H','H','H','H','H','H','S','S','S']}
    
    def __init__(self, starting_fund, min_bet = 25):
        self.funds = starting_fund
        self.tally = [self.funds]
        self.c1 = [0]
        self.c2 = [0]
        self.sum_cards = [0]
        self.cards = [2]
        self.hands = 1
        self.cur_hand = 1
        
        self.min_bet = min_bet
        self.amt_bet = [min_bet]
        
        self.hands_total = 0
        self.hands_won = 0
    
    def reinitialize(self):
        # Reset values for player in order to start from a fresh slate
        self.sum_cards = [0]
        self.cards = [2]
        self.cur_hand = 1
        self.amt_bet = [self.min_bet]
    
    def count_ace (self):
        # sums the first 2 cards and counts the number of aces in the hand
        ace = 0
        hand_idx = self.cur_hand-1
        if self.c1[hand_idx] == 1 and self.c2[hand_idx] != 1 or  self.c1[hand_idx] != 1 and self.c2[hand_idx] == 1:
            ace = 1
            self.sum_cards[hand_idx] = self.c1[hand_idx] + self.c2[hand_idx] + 10
        elif self.c1[hand_idx] == 1 and self.c2[hand_idx] == 1:
            ace = 2
            self.sum_cards[hand_idx] = self.c1[hand_idx] + self.c2[hand_idx] + 10
        else:
            self.sum_cards[hand_idx] = self.c1[hand_idx] + self.c2[hand_idx]
        
        return ace
    
    def action_simple(self, deal):
        
        if self.hands == 1:
            self.reinitialize()
        ace = self.count_ace()
        hand_idx = self.cur_hand-1
        
        while self.continue_drawing(ace, deal):
            # draw the next card for the current hand
            next_c = deal.deal_card()
            self.cards[hand_idx] += 1
            self.sum_cards[hand_idx] += next_c
            if next_c == 1:
                ace += 1
                self.sum_cards[hand_idx] += 10
            
            if self.sum_cards[hand_idx] > 21 and ace > 0:
                ace -= 1
                self.sum_cards[hand_idx] -= 10
        # handle splits
        if self.cur_hand < self.hands:
            # print('c1: ', self.c1, '\tc2: ', self.c2)
            self.cur_hand += 1
            self.action_simple(deal)
        
    def continue_drawing(self, ace, deal):
        
        hand_idx = self.cur_hand-1
        # No draw if sum exceeded 21 already
        if self.sum_cards[hand_idx] > 21:
            return False
        
        cmd = 'None'
        # Hard hand
        if ace == 0:
            if self.sum_cards[hand_idx] >= 4 and self.sum_cards[hand_idx] <= 21:
                if self.c1[hand_idx] == self.c2[hand_idx]:
                    cmd = self.rule_pair[deal.c1][self.c1[hand_idx]-1]
                else:
                    cmd = self.rule_std[deal.c1][self.sum_cards[hand_idx]-4]
            else:
                print("Error in hard hand")
        # special case with 2 aces - not allowed to split again
        elif ace == 2 and self.hands == 1 and self.cards[hand_idx] == 2:
            self.c1.append(self.c2[hand_idx])
            self.c2[hand_idx] = deal.deal_card()
            self.c2.append(deal.deal_card())
            self.hands += 1
            self.cur_hand += 1
            self.sum_cards = [self.c1[i] + self.c2[i] + 10 for i in range(self.hands)]
            self.amt_bet = self.amt_bet*2
            self.cards = [2,2]
            return False
        # Soft hand
        else:
            if self.sum_cards[hand_idx] >= 12 and self.sum_cards[hand_idx] <= 21:
                cmd = self.rule_sft[deal.c1][self.sum_cards[hand_idx]-12]
            else:
                print("Error in soft hand")
#        print(cmd)
        
        
        
        if cmd == 'H':
            return True
        elif cmd == 'S':
            return False
        elif cmd == 'D':
            if self.cards[hand_idx] > 2:
                return True
            else:
                next_c = deal.deal_card()
                self.sum_cards[hand_idx] += next_c
                self.amt_bet[hand_idx] += self.amt_bet[hand_idx]
                self.cards[hand_idx] += 1
                return False
        elif cmd == 'P':
            self.hands += 1
            self.c1.append(self.c2[hand_idx])
            self.c2[hand_idx] = deal.deal_card()
            self.c2.append(deal.deal_card())
            
            self.sum_cards.append(0)
            self.amt_bet.append(self.amt_bet[hand_idx])
            self.cards.append(2)
            
            return self.continue_drawing(self.count_ace(), deal)
        else:
            print('Error in command')
            return False
        