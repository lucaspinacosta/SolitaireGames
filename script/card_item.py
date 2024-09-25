from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget


class CardItem:
    def __init__(self, card, width, height):
        self.card = card
        self.width = width
        self.height = height

        # Load the card image
        if card.is_face_up():
            self.pixmap = QPixmap(card.get_image_path()).scaled(
                self.width, self.height, Qt.KeepAspectRatio
            )
        else:
            self.pixmap = QPixmap(f'assets/back_side/{card.back_style}.png').scaled(
                self.width, self.height, Qt.KeepAspectRatio
            )

        # Store the position of the card
        self.pos = QPointF(0, 0)
        # Original position for snapping back
        self.original_pos = QPointF(0, 0)

        # For group dragging
        self.child_cards = []
        self.is_being_dragged = False  # To track dragging
        self.is_selected = False  # To track selection for highlighting

    def render(self, painter, x, y):
        """Manually draw the card using the given QPainter."""
        self.pos = QPointF(x, y)
        painter.drawPixmap(int(x), int(y), self.pixmap)

        # If the card is selected, draw a red border around it
        if self.is_selected:
            pen = QPen(QColor('red'))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRect(int(x), int(y), self.width, self.height)
        else:
            painter.setPen(Qt.NoPen)

    def add_child_card(self, card_item):
        """Adds a child card below this card."""
        self.child_cards.append(card_item)

    def mousePressEvent(self, event):
        """Start dragging when the mouse is pressed."""
        if self.contains_point(event.pos()):
            self.is_being_dragged = True
            self.is_selected = True  # Highlight when selected
            self.original_pos = self.pos

    def mouseReleaseEvent(self, event, other_cards):
        """Stop dragging and snap the card when the mouse is released."""
        self.is_being_dragged = False
        self.is_selected = False  # Remove highlight after release
        self.snap_to_closest(other_cards)

    def mouseMoveEvent(self, event):
        """Move the card while it's being dragged."""
        if self.is_being_dragged:
            delta = event.pos() - self.pos
            self.move_card(delta.x(), delta.y())

    def move_card(self, delta_x, delta_y):
        """Move the card by a certain offset and update the child cards."""
        new_x = self.pos.x() + delta_x
        new_y = self.pos.y() + delta_y
        self.pos = QPointF(new_x, new_y)

        # Move child cards along with this card
        for idx, child_card in enumerate(self.child_cards):
            child_card.move_card(0, (idx + 1) * (self.height // 4))

    def snap_to_closest(self, other_cards):
        """Find the closest card from a list of other cards and snap to it."""
        closest_card_item = self.find_closest_card(other_cards)
        if closest_card_item:
            # Snap to the position below the closest card
            target_pos = closest_card_item.pos + QPointF(0, self.height // 4)
            self.pos = target_pos

            # Also snap child cards to follow this card
            for idx, child_card in enumerate(self.child_cards):
                child_card.move_card(0, (idx + 1) * (self.height // 4))

    def find_closest_card(self, other_cards):
        """Find the closest card for snapping purposes."""
        min_distance = float('inf')
        closest_card_item = None

        snapping_distance = 50  # Define a reasonable snapping distance

        for card_item in other_cards:
            if card_item != self:
                distance = (card_item.pos - self.pos).manhattanLength()
                if distance < min_distance and distance < snapping_distance:
                    min_distance = distance
                    closest_card_item = card_item

        return closest_card_item

    def contains_point(self, point):
        """Check if a point is within the bounding rect of the card."""
        rect = QRectF(self.pos.x(), self.pos.y(), self.width, self.height)
        return rect.contains(point)
