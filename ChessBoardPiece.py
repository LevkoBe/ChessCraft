class ChessBoardPiece:
    def __init__(self, piece: str, color: str):
        self.piece = piece
        self.color = color
    
    def __str__(self) -> str:
        return self.piece + self.color
    
    @classmethod
    def from_string(cls, piece_string: str):
        piece = piece_string[0]
        color = piece_string[1]
        return cls(piece, color)
