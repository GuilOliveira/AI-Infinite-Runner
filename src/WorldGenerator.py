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

    def create_object(self, type_id, pos_x, pos_y, t="ground", size=64):
        self.world_objects.append({
            "type_id": type_id,
            "type": "ground",
            "size": size,
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

        holes = self.get_holes_qnt(initial_x, final_x)
        second_platform = self.get_second_platform_qnt(initial_x, final_x)
        third_plataforms = self.get_third_platform_qnt(initial_x, final_x, second_platform)
        
        for i in range(0,len(holes)-1):
            if holes[i] == initial_x or holes[i] == final_x:
                self.create_object(4, holes[i] * 64 + max_pos, 8 * 64)
            elif holes[i]-1!=holes[i-1]:
                self.create_object(3, holes[i] * 64 + max_pos, 8 * 64)
            elif holes[i]+1!=holes[i+1]:
                self.create_object(5, holes[i] * 64 + max_pos, 8 * 64)
            else:
                self.create_object(4, holes[i] * 64 + max_pos, 8 * 64)
        
        if second_platform!=[]:
            for i in second_platform:
                
                for j in range(0,len(i)):
                    if j==0:
                        self.create_object(0, i[j] * 64 + max_pos, 5 * 64)
                    elif j==len(i)-1:
                        self.create_object(2, i[j] * 64 + max_pos, 5 * 64)
                    else:
                        self.create_object(1, i[j] * 64 + max_pos, 5 * 64)

        if third_plataforms!=[]:
            for i in third_plataforms:
                for j in range(0,len(i)):
                    if j==0:
                        self.create_object(0, i[j] * 64 + max_pos, 2 * 64)
                    elif j==len(i)-1:
                        self.create_object(2, i[j] * 64 + max_pos, 2 * 64)
                    else:
                        self.create_object(1, i[j] * 64 + max_pos, 2 * 64)
                    


    def get_second_platform_qnt(self, initial_x, final_x, safe_spot=2):
        qnt = random.choices([0, 1, 2, 3], weights=[3, 3, 2, 1], k=1)[0]
        if qnt == 0:
            return []
        plataforms = []
        initial_x += safe_spot
        final_x -= safe_spot
        section = (final_x - initial_x) / qnt

        for i in range(qnt):
            size = random.choices([3, 4, 5, 6], weights=[2, 4, 4, 2], k=1)[0]
            start = random.randint(int(i * section + 1), int(section * (i + 1)) - (size - 1))
            platform = [start + j + safe_spot for j in range(size)]
            plataforms.append(platform)
        
        return plataforms

    def get_third_platform_qnt(self, initial_x, final_x, m_plataforms, safe_spot=2):
        if len(m_plataforms) == 0:
            return[]

        plataforms = []
        initial_x += safe_spot

        for i in m_plataforms:
            qnt = random.choices([0, 1], weights=[5, 6], k=1)[0]
            if qnt:
                size = random.choices([2, 3, 4, 5], weights=[2, 4, 4, 2], k=1)[0]
                start = random.randint(i[1], len(i)+i[1]-2)
                if start+size<=final_x+1:
                    platform = [start + j + safe_spot for j in range(size)]
                    plataforms.append(platform)
        return plataforms

    def get_holes_qnt(self, initial_x, final_x, safe_spot=2):
        plataforms = []
        for i in range(initial_x,final_x):
            plataforms.append(i)
        qnt = random.choices([0, 1, 2], weights=[2, 2, 1], k=1)[0]
        if qnt == 0:
            return plataforms

        initial_x += safe_spot
        final_x -= safe_spot
        section = (final_x - initial_x) / qnt
        
        for i in range(qnt):
            size = random.choices([2, 3, 4], weights=[4, 3, 1], k=1)[0]
            start = random.randint(int(i * section + 1), int(section * (i + 1)) - size - 2)
            for j in range(0,size):
                plataforms.remove(start+j+safe_spot)
            
        return plataforms
    
    def set_obstacles(self, y, x ):
         pass