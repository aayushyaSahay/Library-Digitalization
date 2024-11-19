from prime_generator import set_primes, get_next_size
from hash_table import HashSet, HashMap
from dynamic_hash_table import DynamicHashSet, DynamicHashMap
from tqdm import tqdm  # For progress bars
import random
import string
import time
start_time = time.time()
# Prime sizes (ensure they are suitable for the hash table)
prime_sizes = [87811,87811,87811,87811,87811,87811,87811,87811,87811,87811,49739,49739,49739,49739,49739,49739]
set_primes(prime_sizes)  # Set prime sizes for `get_next_size` to function correctly

# Parameters for Dynamic HashSet and Dynamic HashMap
z = 31  # Parameter for polynomial accumulation
z1, z2, c2 = 31, 37, 9421  # Parameters for double hashing
initial_table_size = 10069  # Initial table size

params_chain = (z, initial_table_size)
params_linear = (z, initial_table_size)
params_double = (z1, z2, c2, initial_table_size)

# Initialize DynamicHashSet for each collision resolution method
dynamic_hashset_chain = DynamicHashSet("Chain", params_chain)
dynamic_hashset_linear = DynamicHashSet("Linear", params_linear)
dynamic_hashset_double = DynamicHashSet("Double", params_double)

# Initialize DynamicHashMap for each collision resolution method
dynamic_hashmap_chain = DynamicHashMap("Chain", params_chain)
dynamic_hashmap_linear = DynamicHashMap("Linear", params_linear)
dynamic_hashmap_double = DynamicHashMap("Double", params_double)

# Function to generate random strings (to simulate keys/values)
random.seed(42)

def generate_unique_strings(length, count):
    generated = set()
    while len(generated) < count:
        letters = string.ascii_letters
        new_str = ''.join(random.choice(letters) for _ in range(length))
        if new_str not in generated:
            generated.add(new_str)
    return list(generated)

# Define test elements to be added to hash tables/sets
num_elements = 40000  # Insert more elements to trigger rehashing
key1 = generate_unique_strings(2, 2000)
key2 = generate_unique_strings(3, num_elements - 2000)
keys = key1 + key2
values = generate_unique_strings(3, num_elements)

# Insert elements into DynamicHashSet and DynamicHashMap with progress bar
def test_dynamic_hashset(dynamic_hashset):
    print(f"\nTesting DynamicHashSet ({dynamic_hashset.collision_type})...")
    for key in tqdm(keys, desc="Inserting keys into DynamicHashSet"):
        dynamic_hashset.insert(key)
        # Force rehash when the load factor is too high
       
    print("DynamicHashSet testing complete.")

def test_dynamic_hashmap(dynamic_hashmap):
    print(f"\nTesting DynamicHashMap ({dynamic_hashmap.collision_type})...")
    for i in tqdm(range(num_elements), desc="Inserting key-value pairs into DynamicHashMap"):
        key, value = keys[i], values[i]
        dynamic_hashmap.insert((key, value))
        # Force rehash when the load factor is too high
      
    print("DynamicHashMap testing complete.")

# Check the integrity of the data after rehashing with progress bar
def check_dynamic_hashset(dynamic_hashset):
    print(f"\nChecking DynamicHashSet ({dynamic_hashset.collision_type}) integrity...")
    for key in tqdm(keys, desc="Verifying keys in DynamicHashSet"):
        if not dynamic_hashset.find(key):
            print(f"Key {key} missing after rehashing!")
            return False
    print("All keys are present in DynamicHashSet after rehashing!")
    return True

def check_dynamic_hashmap(dynamic_hashmap):
    print(f"\nChecking DynamicHashMap ({dynamic_hashmap.collision_type}) integrity...")
    for i in tqdm(range(num_elements), desc="Verifying key-value pairs in DynamicHashMap"):
        key, value = keys[i], values[i]
        stored_value = dynamic_hashmap.find(key)
        if stored_value != value:
            print(f"Mismatch for key {key}: Expected {value}, Found {stored_value}")
            return False
    print("All key-value pairs are correct in DynamicHashMap after rehashing!")
    return True

# Run tests
test_dynamic_hashset(dynamic_hashset_chain)
test_dynamic_hashset(dynamic_hashset_linear)
test_dynamic_hashset(dynamic_hashset_double)

check_dynamic_hashset(dynamic_hashset_chain)
check_dynamic_hashset(dynamic_hashset_linear)
check_dynamic_hashset(dynamic_hashset_double)

test_dynamic_hashmap(dynamic_hashmap_chain)
test_dynamic_hashmap(dynamic_hashmap_linear)
test_dynamic_hashmap(dynamic_hashmap_double)

check_dynamic_hashmap(dynamic_hashmap_chain)
check_dynamic_hashmap(dynamic_hashmap_linear)
check_dynamic_hashmap(dynamic_hashmap_double)
end_time = time.time()
print(f"Time for HashMap : {end_time - start_time:.3f} seconds")