class Tiles:
    def __init__(self, tileset, tile_width, tile_height):
        self.tileset = tileset
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.all = self.get_all_tiles()

    def get_all_tiles(self):
        tile_positions = [
            (4, 1),
            (5, 1),
            (6, 1),
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 0)
        ]
        tiles = []
        for position in tile_positions:
            tiles.append(self.tile_getter(position))
        return tiles

    def tile_getter(self, position):
        x, y = position
        return self.tileset.subsurface((x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
