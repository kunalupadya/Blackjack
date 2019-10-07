##Blackjack

This is my implementation of Blackjack - you start with a chipcount and 

Run from console using `python poker.py`

Enjoy!

I utilized object oriented design principles to design blackjack in classes. I created one class to handle the game and the game logic, named Blackjack. This class deals with the mechanics of the game, dealing out cards to the human and ai dealer. It also handles conversion of hands to any format, as cards are stored as ints initially to create the deck (0-51), and converted to strings when needed to be displayed. Because of this design, the user of this class has access to two different string representations of cards, both the ascii line art and also a textual representation of the cards. The BlackjackInputRunner class handles asking for user input and running the input into the Blackjack class. This involves running game loops and waiting for inputs. This allows the whole game to be run with only two lines, by instantiating the BlackjackInputRunner class and calling its startgame function. Overall, I am happy with the design of this game, but I wish that I had made tests for the class - it would have saved time in the long run by allowing me to be sure my game worked without extensive tests.

I used python as I was very familiar with it and knew I could easily run my program in console. I also had originally planned on utilizing an API to create poker AI by relying on handstrengths, but I could not find any suitable APIs that were free.    