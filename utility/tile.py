class Tile:

    piece_on_tile = None
    tile_coord = None

    def __init__(self, coord, piece):
        self.tile_coord = coord
        self.piece_on_tile = piece
