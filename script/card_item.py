from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap


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

        # For dragging
        self.is_being_dragged = False  # To track dragging
        self.is_selected = False  # To track selection for highlighting
        # Store offset to handle smooth dragging
        self.drag_offset = QPointF(0, 0)

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
        # Only allow face-up cards to be dragged
        if not self.card.is_face_up():
            return

        if self.contains_point(event.pos()):
            self.is_being_dragged = True
            self.is_selected = True  # Highlight when selected
            self.original_pos = self.pos
            self.drag_offset = event.pos() - self.pos  # Calculate the drag offset

    def mouseReleaseEvent(self, event, other_cards):
        """Stop dragging and snap the card when the mouse is released."""
        self.is_being_dragged = False
        self.is_selected = False  # Remove highlight after release

    def mouseMoveEvent(self, event):
        """Move the card while it's being dragged."""
        if self.is_being_dragged:
            # Move the card based on the mouse position minus the drag offset
            self.pos = event.pos() - self.drag_offset

    def contains_point(self, point):
        """Check if a point is within the bounding rect of the card."""
        rect = QRectF(self.pos.x(), self.pos.y(), self.width, self.height)
        return rect.contains(point)
