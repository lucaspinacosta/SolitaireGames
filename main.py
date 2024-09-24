
import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QMainWindow)

from script.cards import Card, Suit


class CardItem(QGraphicsItem):
    def __init__(self, card):
        super().__init__()
        self.card = card

    # Override boundingRect, paint, and mouse events to manage drag-and-drop


class TableauColumn:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        return self.cards.pop()

    def can_place_card(self, card):
        # Add logic to determine if a card can be placed
        pass


class Solitaire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Solitaire Game')
        self.setGeometry(100, 100, 800, 600)

        # Create the game scene and view
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 800, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Initialize deck, tableau, foundation, stockpile, etc.
        self.deck = self.create_deck()
        self.tableau = [[] for _ in range(7)]  # 7 tableau columns
        self.foundation = [[] for _ in range(4)]  # 4 foundation piles
        self.stockpile = []  # Cards left in the deck
        self.waste = []  # Cards drawn from the stockpile
        self.back_side = "green_back"

        self.card_width = 80  # Set card width
        self.card_height = 120  # Set card height

        self.deal_cards()  # Deal the initial cards to the tableau

        self.show()

    def create_deck(self):
        """Creates and shuffles a standard deck of 52 cards."""
        suits = [Suit.HEARTS.value, Suit.DIAMONDS.value,
                 Suit.CLUBS.value, Suit.SPADES.value]
        # 1 = Ace, 11 = Jack, 12 = Queen, 13 = King
        values = list(range(1, 14))
        deck = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        """Deals cards to the tableau. First column gets 1 card, second gets 2, etc."""
        # Distribute cards to the tableau columns
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.pop()
                if j == i:
                    card.flip()  # Flip the last card in the column to be face-up
                self.tableau[i].append(card)
                self.display_card(card, i, j)

    def display_card(self, card, column, row):
        """Displays a card on the screen."""
        if card.is_face_up():
            image_path = card.get_image_path()
        else:
            image_path = f'assets/back_side/{self.back_side}.png'

        pixmap = QPixmap(image_path).scaled(
            self.card_width, self.card_height, Qt.KeepAspectRatio)
        pixmap_item = self.scene.addPixmap(pixmap)

        # Dynamically calculate positions based on the card size and the column/row layout
        # Spacing between columns
        x_position = 100 + column * (self.card_width + 20)
        # Overlapping the cards within a column
        y_position = 50 + row * (self.card_height // 4)

        pixmap_item.setPos(x_position, y_position)

        # Add interactivity (drag and drop, etc.)
        pixmap_item.setFlag(pixmap_item.ItemIsMovable)

    def move_card(self, source, destination):
        """Moves a card from the source pile to the destination."""
        # Example of moving cards from tableau to foundation, etc.
        card = source.pop()
        destination.append(card)

    def is_win(self):
        """Checks if all foundation piles are complete."""
        return all(len(pile) == 13 for pile in self.foundation)
      
    def resizeEvent(self, event):
        """Override resize event to make sure everything scales when the window is resized."""
        # Fit the scene into the view without scrollbars
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        # Call the base resize event handler
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Solitaire()
    sys.exit(app.exec_())
