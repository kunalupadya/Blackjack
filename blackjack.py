from random import shuffle

class Blackjack():
    def __init__(self, starting_chips):
        self.chips = starting_chips
        self.short = True
        self.humhand = []
        self.aihand = []
        self.deck = []
        self.makeDeck()
        # self.runout = []

    def makeDeck(self):
        self.deck = list(range(0,52))
        shuffle(self.deck)

    def dealCard(self):
        c = self.deck.pop()#randint(0,51)
        num = c % 13
        suit = c//13
        num+=2
        return (num, suit)

    def dealHand(self):
        self.humhand = []
        self.aihand = []
        if len(self.deck)<10:
            self.makeDeck()
        # self.runout = []
        self.humhand.append(self.dealCard())
        self.humhand.append(self.dealCard())
        self.aihand.append(self.dealCard())
        self.aihand.append(self.dealCard())
        # print(self.humhand)

    def dealAI(self):
        # print("AI Cards: ")
        humbool, humcount = self.isBusted(self.humhand)
        aibool, aicount= self.isBusted(self.aihand)
        while (not aibool) and (aicount<humcount):
            self.hitAI()
            aibool, aicount = self.isBusted(self.aihand)
        sai = []
        for cardind in range(len(self.aihand)):
            sai.append(self.cardToString(self.aihand[cardind]))
        print("AI Cards:")
        self.printAsciiCards(sai)
        print("Total AI count: " + str(aicount))
        if (aicount<humcount) or aibool:
            print("You win!!!!")
            return "HUM"
        if aicount>humcount:
            print("You lose :(")
            return "AI"
        else:
            print("Tie!")
            return "TIE"

    def hit(self, l):
        l.append(self.dealCard())
        return self.isBusted(l)

    def hitMe(self):
        return self.hit(self.humhand)

    def hitAI(self):
        return self.hit(self.aihand)


    def isBusted(self, hand):
        count = 0
        aces = 0
        for each in hand:
            v = each[0]
            if v in {11,12,13}:
                v = 10
            if v == 14:
                v = 11
                aces+=1
            count+=v
        while(count>21) and(aces>0 ):
            count-=10
            aces-=1
        return (count>21,count)

    def getState(self):
        sme = []
        for card in self.humhand:
            sme.append(self.cardToString(card))
        sai = [("?", "?")]
        for cardind in range(1, len(self.aihand)):
            sai.append(self.cardToString(self.aihand[cardind]))


        print("AI Cards:")
        self.printAsciiCards(sai)
        print()

        print("Your Cards: ", end="")
        self.printAsciiCards(sme)
        return self.isBusted(self.humhand)

    def startHand(self):
        self.dealHand()

    def printAsciiCards(self, cardsstringlist):
        print(cardsstringlist)
        a = "+----+\n|    |\n|    |\n|    |\n+----+"
        totstring = "\n\n\n\n".split("\n")
        newcard = a.split("\n")
        for each in cardsstringlist:
            m = list(newcard[1])
            m[1] = each[1]
            m[4] = each[0]
            m = "".join(m)
            newcard[1] = m
            for each in range(len(totstring)):
                totstring[each] += " " + newcard[each]
        print("\n".join(totstring))

    def cardToString(self, card):
        num = card[0]
        suit = card[1]
        suits = {0:"Spades", 1:"Hearts", 2:"Clubs", 3:"Diamonds"}
        shortSuits = {0:"♠", 1:"♥", 2:"♣", 3:"♦"}
        shortCards = {13:"K", 14:"A", 10:"T", 11:"J", 12: "Q"}
        cards = {13: "King", 14: "Ace", 11: "Jack", 12: "Queen"}
        if self.short:
            suit = shortSuits[suit]
            if num in shortCards:
                num = shortCards[num]
        else:
            suit = suits[suit]
            if num in cards:
                num = cards[num]
        num = str(num)
        return (num,suit)

class BlackjackInputRunner():
    def __init__(self):
        name = input("What is your name? ")
        print("Hi, " + name + " - let's play blackjack!")
        while True:
            try:
                userInput = input("How many chips do you want to start with? ")
                val = int(userInput)
                if val < 1:
                    raise ArithmeticError
                break
            except ValueError:
                print("That's not an int!")
            except ArithmeticError:
                print("Not a valid chipcount!")
        self.startcount = val
        self.game = Blackjack(val)

    def startGame(self):
        print("Let's get into it! Hit q when you want to stop")
        self.game.dealHand()
        # p.hitMe()
        self.runGameLoop()

    def runGameLoop(self):
        play = True
        bettingtime = True
        while play:
            if bettingtime:
                bet, bettingtime, play = self.allowBetting(bettingtime, play)
            bust, count = self.game.getState()
            if bust:
                print("You busted!")
                bettingtime, play = self.askAboutNewGame(bettingtime, play)
            else:
                bettingtime, play = self.notBustedPrompt(bet, bettingtime, count, play)
        print("Game over: You finished with " + str(
            self.game.chips) + " chips, %.2f percent of your initial chipcount!" % (
                      self.game.chips / self.startcount * 100))

    def notBustedPrompt(self, bet, bettingtime, count, play):
        myin = ""
        while myin == "":
            print("Total count right now: " + str(count))
            myin = input("What will you do? Hit H to see another card, or hit S to stop. ")
            if myin in {"H", "h"}:
                self.game.hitMe()
            elif myin in {"S", "s"}:
                winner = self.game.dealAI()
                if winner == "HUM":
                    self.game.chips += bet * 2
                if winner == "TIE":
                    self.game.chips += bet
                bettingtime, play = self.askAboutNewGame(bettingtime, play)
            elif myin in {"Q", "q"}:
                play = False
            else:
                print("That's not a valid response - try again!")
                myin = ""
        return bettingtime, play

    def askAboutNewGame(self, bettingtime, play):
        myin = ""
        while myin == "":
            if self.game.chips == 0:
                play = False
                print("You have no more chips :(")
                break
            myin = input(
                "If you want to play again using the same deck (to learn how to count cards), play again by hitting A, or hit R to reset the deck and play again! Hit q to quit.")
            bettingtime = True
            if myin in {"A", "a"}:
                self.game.dealHand()
                # p.hitMe()
            # elif myin in {"S", "s"}:
            elif myin in {"R", "r"}:
                self.game.makeDeck()
                self.game.dealHand()
            elif myin in {"Q", "q"}:
                play = False
            else:
                print("That's not a valid response - try again!")
                myin = ""
        return bettingtime, play

    def allowBetting(self, bettingtime, play):
        while True:
            try:
                print("Chipcount: " + str(self.game.chips))
                bet = input("How much do you want to bet? ")
                val = int(bet)
                if val < 1:
                    raise ArithmeticError
                if val > self.game.chips:
                    print("You dont have that many chips!")
                else:
                    break
            except ValueError:
                print("That's not an int!")
            except ArithmeticError:
                print("Not a valid bet!")
        bet = val
        self.game.chips -= bet
        bettingtime = False
        return bet, bettingtime, play


if __name__  == "__main__":
    game = BlackjackInputRunner()
    game.startGame()
