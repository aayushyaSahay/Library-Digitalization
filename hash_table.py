from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.params = params
        self.collision_type = collision_type
        self.z = params[0]
        self.table_size = params[3] if self.collision_type == "Double" else params[1]
        self.table = [None] * self.table_size
        self.count = 0  # To track the number of entries in the table
        self.keys = []
        self.values = []
        # Additional parameters for double hashing
        if self.collision_type == "Double":
            self.z2 = params[1]
            self.c2 = params[2]
            
    def polynomial_hash(self, key, z_value, mod_value):
        # Polynomial accumulation for hashing
        hash_value = 0
        new_key = key[::-1]
        for char in new_key:
            p_val = ord(char) - ord('a') if 'a' <= char <= 'z' else ord(char) - ord('A') + 26
            hash_value = (hash_value * z_value + p_val) % mod_value
        return hash_value
    
    def get_primary_hash(self, key):
        # Get primary hash based on first z parameter and table size
        return self.polynomial_hash(key, self.z, self.table_size)

    def get_secondary_hash(self, key):
        # Only for double hashing, using z2 and c2 as params
        return self.c2 - (self.polynomial_hash(key, self.z2, self.c2) % self.c2)
    
    def insert(self, x):
        slot = self.get_slot(x)
        if self.collision_type == "Chain":
            self.chaining_insert(slot, x)
        else:
            if self.table[slot] is None:
                self.table[slot] = x
                self.count += 1
                self.keys.append(x)
    
    # this returns TRUE FALSE VALUES and therefore needs to be modified in the HashTable class
    def find(self, key):
        if self.collision_type == "Chain":
            slot = self.get_primary_hash(key)
            if self.table[slot] is not None and key in self.table[slot]:
                return True
            else:
                return False
        elif self.collision_type == "Linear":
            return self.linear_probe(key, True)
        elif self.collision_type == "Double":
            return self.double_hash(key, True)
    
    def get_slot(self, key):
        # Returns the slot index for a given key based on collision handling
        if self.collision_type == "Chain":
            return self.get_primary_hash(key)
        elif self.collision_type == "Linear":
            return self.linear_probe(key)
        elif self.collision_type == "Double":
            return self.double_hash(key)
    
    def chaining_insert(self, slot, entry):
        # Insert logic for chaining, appending to list in slot
        if self.table[slot] is None:
            self.table[slot] = [entry]
            self.count += 1
        else:
            self.table[slot].append(entry)
            self.count += 1
        self.keys.append(entry)

    def linear_probe(self, key, finding = False):
        # Linear probing to find an open slot for a given key
        slot = self.get_primary_hash(key)

        _ = 0
        if finding == True:
            while self.table[slot] is not None and _ < self.table_size: 
                if self.table[slot] == key:
                    return True
                slot = (slot + 1) % self.table_size
                _ += 1
            return False

        # Insertion 
        while self.table[slot] is not None and  _ < self.table_size:
            slot = (slot + 1) % self.table_size
            _ += 1
        if _ == self.table_size:
            raise Exception("Either table is full")
        return slot

    def double_hash(self, key, finding = False):
        # Double hashing for finding a slot
        slot = self.get_primary_hash(key)
        step_size = self.get_secondary_hash(key)
        
        _ = 0
        if finding == True:
            while self.table[slot] is not None and _ < self.table_size:
                if self.table[slot] == key:
                    return True
                slot = (slot + step_size) % self.table_size
                _ += 1
            return False

        while self.table[slot] is not None and _ < self.table_size: # here there is a possibility to get stuck in an infinite loop where you are going in cycles
            slot = (slot + step_size) % self.table_size
            _ += 1
        if _ == self.table_size:
            raise Exception("Either table is full or any of the paramters is not a prime")
        return slot
    
    def get_load(self):
        return self.count / self.table_size
    
    def __str__(self):
        result = []
        for slot in self.table:
            if slot is None:
                result.append("<EMPTY>")
            else:
                if self.collision_type == "Chain":
                    # For chaining, join multiple entries with semicolons
                    slot_entries = [str(entry) for entry in slot]
                    result.append(" ; ".join(slot_entries))
                else:
                    # For probing methods, just convert the entry to string
                    result.append(str(slot))
        return " | ".join(result)
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, key):
        if not self.find(key):
            super().insert(key)
        # else:
        #     print("Key already exists")    
    
    # TODO: for now leaving this function in all classes, will get this done by gpt or claude
    def __str__(self):
        return super().__str__()
        
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x): # haven't implemented the super().__init__ because the get_slot(x) is written in the super().__init__ which will cause problem.
        # x = (key, value)
        key, value = x
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            self.chaining_insert(slot, x)
        else:
            if self.table[slot] is None:
                self.table[slot] = x
                self.count += 1
                self.keys.append(key)
                self.values.append(value)
                
    def chaining_insert(self, slot, entry):
        # Insert logic for chaining, appending to list in slot
        if self.table[slot] is None:
            self.table[slot] = [entry]
            self.count += 1
        else:
            self.table[slot].append(entry)
            self.count += 1
        self.keys.append(entry[0])
        self.values.append(entry[1])
    
    def find(self, key):
        if self.collision_type == "Chain":
            slot = super().get_primary_hash(key)
            for k,v in self.table[slot]:
                if k == key:
                    return v
            else:
                return None
        elif self.collision_type == "Linear":
            slot = self.get_primary_hash(key)
            _ = 0
            while self.table[slot] is not None and _ < self.table_size:
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                slot = (slot + 1) % self.table_size
                _ += 1
            return False
        elif self.collision_type == "Double":
            slot = self.get_primary_hash(key)
            step_size = self.get_secondary_hash(key)
            _ = 0
            while self.table[slot] is not None and _ < self.table_size:
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                slot = (slot + step_size) % self.table_size
                _ += 1
            return False

    
    
    # TODO: implement this function at last in all the classes
    def __str__(self):
        result = []
        for slot in self.table:
            if slot is None:
                result.append("<EMPTY>")
            else:
                if self.collision_type == "Chain":
                    slot_entries = [f"({k}, {v})" for k, v in slot]
                    result.append(" ; ".join(slot_entries))
                else:
                    # For probing methods, format the single (key, value) pair
                    key, value = slot
                    result.append(f"({key}, {value})")
        return " | ".join(result)