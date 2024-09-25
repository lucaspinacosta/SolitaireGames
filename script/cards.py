from enum import Enum


class Suit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"


class Card:
    def __init__(self,  suit: Suit, value: int, back_style='green_back'):
        """
        Initializes a card with a suit, value, and face-up status.

        :param suit: Suit of the card (H = Hearts, D = Diamonds, C = Clubs, S = Spades)
        :param value: Value of the card (1 = Ace, 11 = Jack, 12 = Queen, 13 = King)
        """
        self.suit = suit
        self.value = value
        self.face_up = False  # Cards start face-down by default
        self.back_style = back_style

    def flip(self):
        """Flips the card to show the opposite side."""
        self.face_up = not self.face_up

    def is_face_up(self):
        """Returns True if the card is face-up."""
        return self.face_up

    def get_image_path(self):
        """Returns the path to the image file for the card."""
        if self.face_up:
            # Assuming you have a folder with card images named like '1S.png'
            return f"assets/cards/{self.value}{self.suit}.png"
        else:
            return f"assets/back_side/{self.back_style}.png"

    def __str__(self):
        """Returns a string representation of the card (for debugging)."""
        face_status = "Face-Up" if self.face_up else "Face-Down"
        return f"{self.value} of {self.suit} ({face_status})"

