class ChessBoardPiece:
    def __init__(self, piece: str, color: str):
        self.piece = piece
        self.color = color
    
    def __str__(self) -> str:
        return self.piece + self.color
