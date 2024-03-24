from ChessPiece import ChessPiece
piece = ChessPiece("barbie", "b", ["+0", "++", "0+", "-+", "-0", "--", "0-", "+-"], "8")
directions = piece.calculate_reachable_cells((5, 5), 8, 8)
print("hiiii")