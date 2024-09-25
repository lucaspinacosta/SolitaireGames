import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from script.card_item import CardItem
from script.cards import Card, Suit


class Solitaire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Solitaire Game')
        self.setFixedSize(1000, 800)

        # Set up the main layout to contain the game
        self.central_widget = GameWidget(self)
        self.setCentralWidget(self.central_widget)

        # Initialize deck and tableau
        self.deck = self.create_deck()
        self.tableau = [[] for _ in range(7)]  # 7 tableau columns

        self.central_widget.deck = self.deck
        self.central_widget.tableau = self.tableau

        self.deal_cards()

        self.show()

    def create_deck(self):
        """Creates and shuffles a standard deck of 52 cards."""
        suits = [Suit.HEARTS.value, Suit.DIAMONDS.value,
                 Suit.CLUBS.value, Suit.SPADES.value]
        values = list(range(1, 14))
        deck = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        """Deals cards to the tableau."""
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.pop()
                if j == i:
                    card.flip()  # Flip the last card in the column to be face-up
                self.tableau[i].append(card)
                self.central_widget.add_card(card, i, j)


class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deck = []
        self.tableau = []
        self.card_width = 80
        self.card_height = 120
        self.cards = []
        self.dragged_card = None  # The currently dragged card

    def add_card(self, card, column, row):
        """Adds card information to be drawn later."""
        card_item = CardItem(card, self.card_width, self.card_height)
        x_position = 150 + column * (self.card_width + 20)
        y_position = 200 + row * (self.card_height // 4)
        self.cards.append((card_item, x_position, y_position))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor('#09175c'))
        gradient.setColorAt(1.0, QColor('#bdb4ff'))
        painter.fillRect(self.rect(), gradient)

        # Draw the cards on the widget
        for card_item, x, y in self.cards:
            card_item.render(painter, x, y)

    def mousePressEvent(self, event):
        """Handle the mouse press to start dragging a card."""
        for card_item, x, y in self.cards:
            if card_item.contains_point(event.pos()):
                card_item.mousePressEvent(event)
                if card_item.is_being_dragged:
                    self.dragged_card = card_item
                    break

    def mouseMoveEvent(self, event):
        """Handle the mouse move event to drag the card."""
        if self.dragged_card:
            self.dragged_card.mouseMoveEvent(event)
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle the mouse release to snap the card."""
        if self.dragged_card:
            self.dragged_card.mouseReleaseEvent(
                event, [card_item for card_item, x, y in self.cards])
            self.dragged_card = None
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Solitaire()
    sys.exit(app.exec_())
