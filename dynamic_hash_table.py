from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_data = self.table
        old_size = self.table_size
        self.table_size = get_next_size()
        self.count = 0
        self.table = [None] * self.table_size
        for i in range(old_size):
            if old_data[i] is not None:
                if self.collision_type == "Chain":
                    for item in old_data[i]:
                        if item is not None:
                            self.insert(item) # hash set hai isliye bas key padi hogi item mein
                else:
                    self.insert(old_data[i])
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)

        if self.get_load() >= 0.5:
            self.rehash()

class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_data = self.table
        old_size = self.table_size
        self.count = 0
        self.table_size = get_next_size() # table size updated
        self.table = [None] * self.table_size
        for i in range(old_size):
            if old_data[i] is not None:
                if self.collision_type == "Chain":
                    for key, value in old_data[i]:
                        if key is not None:
                            self.insert((key, value))
                else:
                    self.insert(old_data[i])

    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)

        if self.get_load() >= 0.5:
            self.rehash()