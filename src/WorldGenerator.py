import math
import random

class WorldGenerator:
    def __init__(self):
        self.can_build_blocks = True
        self.world_objects = []
        self.speed = 400
        self.create_base_block()
        
    def create_base_block(self):
        for i in range(20):
            self.create_object(4, i * 64, 8 * 64)

    def create_object(self, type_id, pos_x, pos_y):
        self.world_objects.append({
            "type_id": type_id,
            "pos_x": pos_x,
            "pos_y": pos_y
        })

    def delete_object(self, obj):
        self.world_objects.remove(obj)

    def update_objects(self, delta_time):
        max_pos = -1000
        next_pos = math.ceil(self.speed * delta_time)
        for obj in self.world_objects:
            if obj["pos_x"] <= -64:
                self.delete_object(obj)
            else:
                obj["pos_x"] -= next_pos
                if obj["pos_x"] > max_pos:
                    max_pos = obj["pos_x"]
        if max_pos < 31 * 64:
            self.create_blocks(max_pos)

    def create_blocks(self, max_pos):
        initial_x = 0
        final_x = 29

        second_platform_qnt = self.get_second_platform_qnt(initial_x, final_x)
        print(second_platform_qnt)
        
        for i in range(initial_x, final_x):
            self.create_object(4, i * 64 + max_pos, 8 * 64)

    def get_second_platform_qnt(self, initial_x, final_x, safe_spot=2):
        qnt = random.choices([0, 1, 2, 3], weights=[4, 3, 2, 1], k=1)[0]
        if qnt == 0:
            return []
        platforms = []
        initial_x += safe_spot
        final_x -= safe_spot
        section = (final_x - initial_x) / qnt
        
        for i in range(qnt):
            size = random.choices([3, 4, 5, 6], weights=[2, 4, 4, 2], k=1)[0]
            start = random.randint(int(i * section + 1), int(section * (i + 1)) - (size - 1))
            platform = [start + j + safe_spot for j in range(size)]
            platforms.append(platform)
        
        return platforms

    def get_third_platform_qnt(self):
        return random.choices([0, 1, 2], weights=[4, 2, 1], k=1)

    def get_holes_qnt(self):
        return random.choices([0, 1, 2], weights=[3, 2, 1], k=1)