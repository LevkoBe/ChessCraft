from typing import Dict, Optional
from ChessPiece import ChessPiece

class PieceMapping:
    def __init__(self):
        self.mapping: Dict[str, ChessPiece] = {}

    def add_piece(self, piece: ChessPiece):
        self.mapping[piece.symbol] = piece

    def get_piece(self, char: str) -> Optional[ChessPiece]:
        return self.mapping.get(char)

    def get_all_pieces(self) -> Dict[str, ChessPiece]:
        return self.mapping

    def set_all_pieces(self, pieces: list[ChessPiece]):
        for piece in pieces:
            self.add_piece(piece)
