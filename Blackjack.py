import random

"""
Deck with 52 cards created
Deck shuffled
Player makes a bet
Player is dealt 2 cards
Dealer is dealt 2 cards, 1 is printed out
Player's total is printed
If it's Blackjack, Player wins 1.5x the bet
Player's bankroll is updated
New game starts,

If it's less than 21, player is asked to hit or stand
Hit - another card is dealt to the player, new total is printed, check for win or bust
Stand - dealer's turn
Both dealer's cards are printed together with their total
If more than 17 - compare with Player
Announce winner or tie
Update bankroll
New game starts
"""
class Card(object):
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        try:
            if rank.upper() == "A":
                self.value = 1
            elif rank.upper() in ("J", "Q", "K"):
                self.value = 10
            else:
                self.value = int(rank)
        except:
            pass
    
    def __repr__(self):
        return self.rank.upper() + self.suit

    def draw(self):
        pass

class Deck(object):
    
    def __init__(self):
        self.cards = []
        for suit in ('h','s','d','c'):
            for rank in ('2','3','4','5','6','7','8','9','10','J','Q','K','A'):
                self.cards.append(Card(suit, rank))
    
    def __len__(self):
        return len(self.cards)
                
    def shuffle(self):
        return random.shuffle(self.cards)

class Player(object):
    
    def __init__(self, name, bankroll = 1000, status = 0):
        self.name = name
        self.bankroll = bankroll
        self.hand = Hand()
        #status of the player, 0 = in play, 1 = waiting for showdown, 2 = 21, 3 = blackjack 4 = busted
        self.status = status
        
    def __repr__(self):
        return self.name
    
    def getBankroll(self):
        return self.bankroll
    
    def setBankroll(self, delta):
        self.bankroll += delta
        
    def setHand(self, hand):
        self.hand = hand
    
    def getHand(self):
        return self.hand

class Hand(object):
    
    def __init__(self):
        self.cards = []
    
    def __len__(self):
        return len(self.cards)
    
    def hit(self, deck, i=0):
        self.cards.append(deck.cards.pop(i))
        #print self.cards
    """       
    def sortDesc(self):
        c = self.cards
        for j in range(len(c)):
            for i in range(len(c) - j):
                if c[i+1].value > c[i].value:
                    bigger = c[i+1]
                    c[i+1] = c[i]
                    c[i] = bigger
        self.cards = c
        return 0
    """
    
    def count(self):
        total = 0
        self.cardsDesc = sorted(self.cards, key = lambda card: card.value, reverse=True)
        for ind, card in enumerate(self.cardsDesc):
            #print total
            if card.value <> 1:
                total += card.value
            else:
                #following are 1 or more aces 
                if total + len(self) - ind + 10 <= 21:
                    total += 11
                else:
                    total += 1
        return total

    """
    def count(self):
        total = 0
        self.sortDesc()
        for card in self.cards:
            if card.value <> 1:
                total += card.value
            else:
                if total + 11 <= 21:
                    total +=  11
                else:
                    total += 1
        return total
        """

class Game(object):
    
    def __init__(self, pNames, bet = 10):
        self.pNum = len(pNames)
        self.bet = bet
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.players = []
                
        for p in pNames:
            self.players.append(Player(p))

        self.players.append(Player("DEALER"))
        
        for c in range(2):
            for p in self.players:
                p.getHand().hit(self.deck)
                
        
    def playerPlay(self, player_index):
        player = self.players[player_index]
        hand = self.players[player_index].getHand()
        action = 0
        #announce current state
        
        
        total = hand.count()
        print "\n\r"
        print "Your hand: " + str(hand.cards) + " is giving you " + str(total)

        if total == 21 and len(hand) == 2:
            print "Woah! You got Black Jack!"
            return 3
        
        while action <> 2:
            #ask for next step
            #print "Asking for input"
            action = int(raw_input("Enter 1 to hit, 2 to stand"))
            #print "Got the input"
            if action == 1:
                #hit
                print "\n\r"
                print "Hit, here's one more!"
                hand.hit(self.deck)
                #print "Your hand: " + str(hand.cards) 
            elif action == 2:
                #stand
                print "Stand. Final total: {}".format(total)
                return 1
            
            #announce result
            total = hand.count()
            if total == 21:
                print "\n\r"
                print "Your hand: " + str(hand.cards) 
                print "Yes, it's 21!"
                return 2
            elif total > 21:
                print "\n\r"
                print "Your hand: " + str(hand.cards) 
                print "{} - it's a bust! Too bad!".format(total)
                return 4
            elif total < 21:
                return 0                
    
    def dealerPlay(self):
        player = self.players[-1]
        hand = self.players[-1].getHand()
        
        #announce current state
        total = hand.count()
        print "Dealer's hand is: {}".format(hand.cards) + "giving a total of {}".format(total)
        if total == 21 and len(hand) == 2:
            print "Woah! Dealer got Blackjack!"
            return 3
        
        #decide on the next step
        if total < 17:
            #hit
            #print "Hit, here's one more!"
            hand.hit(self.deck)
        else:
            #stand
            print "Stand. Final total: {}".format(total)
            return 1
        
        #announce result
        total = hand.count()
        if total == 21:
            print "Dealer got 21!"
            return 2
        elif total > 21:
            print "Dealer busted!"
            return 4
        elif total < 21:
            print "Dealer's current total: " + str(total)
            return 0                
    
    def main(self):
        #Shuffled deck, players created with new Game, each player and dealer were dealt 2 cards, players play one after another
        print "###################################"
        print "Dealer shows " + str(self.players[-1].getHand().cards[1])
        for p in range(self.pNum):
            #print "Current status: " + str(self.players[p].status)
            print "\n\r"
            print "###################################"
            print self.players[p].name + ", it is your turn"
            while self.players[p].status == 0:
                self.players[p].status = self.playerPlay(p)
                #print "New status: " + str(self.players[p].status)
        print "Dealer's playing"
        while self.players[-1].status == 0:
            self.players[-1].status = self.dealerPlay()
        #checking results and adusting bankrolls
        if self.players[-1].status == 3:
            
        for p in range(self.pNum):
            if p.status == 


game1 = Game(["Ran", "Zver"])
game1.main()
