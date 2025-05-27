import random

#Class Will Represent Each Card (Color + Value)
class Card:
  def __init__(self, color, value):
    #Red, Green, Yellow, Blue, Wild
    self.color = color

    #0-9, Skip, Reverse, Draw +2, Wild, Wild +4
    self.value = value

  #The Function Ensures The Playing Card Matches The Top Card
  def isMatch(self, topCard):
    return (
      self.color == topCard.color or
      self.value == topCard.value or
      self.color == "Wild"
    )

  #The Function Will Return The Card (Ex: "Blue 9")
  def __str__(self):
    return self.color.upper() + " " + str(self.value)

class Deck:
  #Generates Deck and Discard Pile
  def __init__(self):
    self.drawPile = self.generateDeck()
    self.discardPile = []
    random.shuffle(self.drawPile)

  def generateDeck(self):
    #Stores All Possible Colors
    colors = ["Red", "Green", "Blue", "Yellow"]

    #Stores All Possible Values
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw +2"]

    deck = []

    #Generates The Cards And Stores Them In The Deck
    for color in colors:
      #One Zero Per Color
      deck.append(Card(color, "0"))
      
      #Twice Repetition of Values Per Color (Exception of 0)
      for i in range(2):
        for value in values[1:]: #Skips Zero
          deck.append(Card(color, value))
    
    #Appending Wild & Wild +4 Cards 4 Times Each
    for i in range(4):
      deck.append(Card("Wild", "Wild"))
      deck.append(Card("Wild", "Wild +4"))

    return deck

  def drawCard(self):
    #Check If The Pile Is Empty
    if not self.drawPile:
      #Adds Cards Back To Pile From Discard Pile
      self.reshuffle()
    #Returns Top Card Of Pile
    return self.drawPile.pop()

  #Resets Draw Pile & Discard Pile
  def reshuffle(self):
    # Save the last card (top of discard pile)
    top_card = self.discardPile[-1]
    # Take all but the top card to reshuffle
    self.drawPile = self.discardPile[:-1]
    # Set the discard pile to only the top card
    self.discardPile = [top_card]
    random.shuffle(self.drawPile)

  #Draws A Card To Start The Game
  def startDiscard(self):
    card = self.drawCard()
    #If The Starting Card Is A Wild Card
    while card.color == "Wild":
      #Place Wild Card On The Bottom Of The Draw Pile
      self.drawPile.insert(0, card)
      #Shuffle The Draw Pile
      random.shuffle(self.drawPile)
      #Draw Top Card Again To Start Game
      card = self.drawCard()
    return card

class Player: 
  #Establishes Name And Hand Of Each Player
  def __init__(self, name):
    self.name = name
    self.hand = []

  def drawCards(self, deck, count = 1): #Count = 1 Ensures Only One Card Is Drawn Unless Specified Otherwise
    for i in range(count):
      #Draws A Card From Draw Pile
      card = deck.drawCard()
      #Adds To The Existing Hand
      self.hand.append(card)

  #Plays The Card In Hand At Specified Index
  def playCard(self, index):
    return self.hand.pop(index)

  #Check If There Is A Playable Card In Hand
  def validMove(self, topCard):
    #Loop Through Hand To See If Any Card In Hand Matches Top Card (Either In Color Or Value)
    i = 0
    while i < len(self.hand):
      #Check For Match
      if self.hand[i].isMatch(topCard):
        return True
      i = i + 1
    #No Playable Card
    return False

  def __str__(self):
    #Declare The Player
    result = self.name + "'s Hand: \n"
    #Loop Through The Specified Players hand
    i = 0
    while i < len(self.hand):
      #Present Each Card (Format: "[1] Blue 9")
      result = result + "[" + str(i) + "]" + str(self.hand[i]) + "\n"
      i = i + 1
    return result
    
class Game: 
  #Establishes The Deck And The Players As Well As All Their Attributes
  def __init__(self, player1Name, player2Name):
    self.deck = Deck()
    self.players = [Player(player1Name), Player(player2Name)]
    self.currentPlayerIndex = 0
    self.direction = 1
    self.skipNext = False
    self.drawStack = 0
    self.currentColor = None

  #Initializes The Game
  def startGame(self):
    #Deal 7 Cards To Both Players
    i = 0
    while i < 7:
      self.players[0].drawCards(self.deck)
      self.players[1].drawCards(self.deck)
      i = i + 1

    #Start Discard Pile
    firstCard = self.deck.startDiscard()
    self.deck.discardPile.append(firstCard)
    self.currentColor = firstCard.color
    #Announce The First Card
    print("The First Card Is " + str(firstCard))

  def nextPlayer(self):
    #Ensures The Taking Turns System Accounting For The Direction In Case Of Reverse
    self.currentPlayerIndex = (self.currentPlayerIndex + self.direction) % len(self.players)

  def applyEffects(self, card):
    #Applies The Special Effects Of All Non-Numerical Cards
    if card.value == "Skip":
      print("Next Player Will Be Skipped!")
      self.skipNext = True
    elif card.value == "Reverse":
      print("Direction Reversed!")
      self.direction = self.direction * -1
    elif card.value == "Draw +2":
      print("Next Player Must Draw 2 Cards")
      self.drawStack = self.drawStack + 2
    elif card.value == "Wild":
      self.chooseColor()
      print("The current color is now " + self.currentColor)
    elif card.value == "Wild +4":
      print("Next Player Must Draw 4 Cards")
      self.drawStack = self.drawStack + 4
      self.chooseColor()
      print("The current color is now " + self.currentColor)

  def chooseColor(self):
    #Possible Colors
    colors = ["Red", "Blue", "Green", "Yellow"]
    chosenColor = ""
    #Verify Inputted Color Is A Valid Choice
    while chosenColor not in colors:
      chosenColor = input("Choose A Color (Red, Blue, Green, Yellow)")
    #Apply New Color
    self.currentColor = chosenColor
    print("The Color Changed To " + self.currentColor)

  def play(self):
    self.startGame()
    gameOver = False

    #Loop Until A Winner Is Declared
    while gameOver == False:
      player = self.players[self.currentPlayerIndex]
      #Express The Circumstances
      print("\n" + player.name + "'s Turn")
      print(player) #Displays Hand
      print("Top Card On Discard Pile: " + str(self.deck.discardPile[-1]))

      #Check If The Player Is Required To Draw Any Cards
      if self.drawStack > 0:
        print(player.name + " Must Draw " + str(self.drawStack) + "Cards")
        player.drawCards(self.deck, self.drawStack)
        self.drawStack = 0
        self.nextPlayer()
        continue 

      #Check If Player's Turn Is Skipped
      if self.skipNext == True:
        print(player.name + " Is Skipped!")
        self.skipNext = False
        self.nextPlayer()
        continue 

      #Conduct Player's Turn (A Valid Card Or Draw)
      if any(card.color == self.currentColor or card.color == "Wild" or card.value == self.deck.discardPile[-1].value for card in player.hand):
        validChoice = False
        while validChoice == False:
          #Player Chooses A Possible Card
          choice = input("Enter Card Number (Index) To Play Or Type 'Draw' To Draw A Card  ")
          if choice == "Draw":
            #Draw A Card
            player.drawCards(self.deck)
            print(player.name + " Drew A Card!")
            validChoice = True
          #If Player Chooses An Index Of Their Hand To Play
          elif choice.isdigit() == True:
            index = int(choice) 
            #Ensure Index Is Valid
            if index >= 0 and index < len(player.hand):
              selectedCard = player.hand[index]
              #Ensure If Card Matches Color/Value With Top Card Or Is A Wild Card
              if (selectedCard.color == self.currentColor or
                  selectedCard.value == self.deck.discardPile[-1].value or
                  selectedCard.color == "Wild"):
                #Allow Player To Play Card
                playedCard = player.playCard(index)
                #Place Card On Top Of Discard Pile
                self.deck.discardPile.append(playedCard)
                #Update The Current Color
                if playedCard.color != "Wild":
                  self.currentColor = playedCard.color
                #Apply Special Effects
                self.applyEffects(playedCard)
                print(player.name + "Played " + str(playedCard))

                #Enforce The "UNO!" Rule When One Card Remains In A Hand
                if len(player.hand) == 1:
                  while True:
                    #Normalize The Word UNO Regardless Of How Its Inputted
                    uno = input("You have ONE card! Type 'UNO' to continue:").strip().lower()
                    if uno == "uno":
                      print("UNO Acknowledged")
                      break
                    else:
                      print("You Must Type UNO To Continue")
                  
                validChoice = True
              else: 
                #If Unplayable Card Selected
                print("You Cannot Play That Card Now! Try Again!")
            else:
              #If Index Out Of Bounds of Existing Hand
              print("Invalid Card Number (Index). Try Again!")
          else:
            #If Input Is Not "Draw" or Digit
            print("Invalid Input. Try Again")
      if not any(card.color == self.currentColor or card.color == "Wild" or card.value == self.deck.discardPile[-1].value for card in player.hand):
        #If The Player Has No Playable Cards And Must Draw
        print(player.name + " has no playable cards.")
        while True:
          draw_input = input("Type 'Draw' to draw a card: ").strip().lower()
          if draw_input == "draw":
            player.drawCards(self.deck)
            print(player.name + " drew a card.")
            break
          else:
            print("Invalid input. You must type 'Draw' to continue.")         

      #Check If A Player Won
      if len(player.hand) == 0:
        print(player.name + " Has Won The Game! Congratulations!")
        gameOver = True
      else:
        self.nextPlayer()  

#Main
print("Welcome To UNO!")
player1 = input("Enter Player 1 Name: ")
player2 = input("Enter Player 2 Name: ")
game = Game(player1, player2)
game.play()