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
        # for each in sai:
        #     print(each[0]+ ' of ' + each[1], end="    ")
        print()

        print("Your Cards: ", end="")
        self.printAsciiCards(sme)
        # for each in sme:
        #     print(each[0]+ ' of ' + each[1], end="    ")
        # print()
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



if __name__  == "__main__":
    name = input("What is your name? ")
    print("Hi, "+ name+" - let's play blackjack!")
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
    # val = 100
    p = Blackjack(val)
    startcount = val
    print("Let's get into it! Hit q when you want to stop")
    p.dealHand()
    # p.hitMe()
    play = True
    bettingtime = True
    while play:
        if bettingtime:
            while True:
                try:
                    if p.chips == 0:
                        play = False
                    print("Chipcount: " + str(p.chips))
                    bet = input("How much do you want to bet? ")
                    val = int(bet)
                    if val < 1:
                        raise ArithmeticError
                    if val>p.chips:
                        print("You dont have that many chips!")
                    else:
                        break
                except ValueError:
                    print("That's not an int!")
                except ArithmeticError:
                    print("Not a valid bet!")
            bet = val
            p.chips-=bet
            bettingtime = False
        bust, count = p.getState()
        if bust:
            myin = ""
            while myin == "":
                myin = input("You busted! If you want to play again using the same deck (to learn how to count cards), play again by hitting A, or hit R to reset the deck and play again! Hit q to quit.")
                bettingtime = True
                if myin in {"A", "a"}:
                    p.dealHand()
                    # p.hitMe()
                # elif myin in {"S", "s"}:
                elif myin in {"R", "r"}:
                    p.makeDeck()
                    p.dealHand()
                elif myin in {"Q", "q"}:
                    play = False
                else:
                    print("That's not a valid response - try again!")
                    myin = ""
        else:
            myin = ""
            while myin == "":
                print("Total count right now: "+ str(count))
                myin = input("What will you do? Hit H to see another card, or hit S to stop. ")
                if myin in {"H", "h"}:
                    p.hitMe()
                elif myin in {"S", "s"}:
                    winner =p.dealAI()
                    if winner == "HUM":
                        p.chips+=bet*2
                    if winner == "TIE":
                        p.chips+=bet
                    print("Chipcount: "+str(p.chips))
                    myin1 = ""
                    while myin1 == "":
                        myin1 = input("If you want to play again using the same deck (to learn how to count cards), play again by hitting A, or hit R to reset the deck and play again! ")
                        bettingtime = True
                        if myin1 in {"A", "a"}:
                            p.dealHand()
                            # p.hitMe()
                        # elif myin in {"S", "s"}:
                        elif myin1 in {"R", "r"}:
                            p.makeDeck()
                            p.dealHand()
                        elif myin1 in {"Q", "q"}:
                            play = False
                        else:
                            print("That's not a valid response - try again!")
                            myin1 = ""
                elif myin in {"Q", "q"}:
                    play = False
                else:
                    print("That's not a valid response - try again!")
                    myin = ""
    print("Game over: You finished with "+str(p.chips)+" chips, %.2f percent of your initial chipcount!" % (p.chips/startcount*100))