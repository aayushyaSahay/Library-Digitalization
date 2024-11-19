import time
import random
import string
import gc
from typing import List, Tuple, Iterator
import library
from prime_generator import set_primes
from typing import List

def get_primes(num_books: int, wordperbook: int) -> List[int]:
    def sieve_of_atkin(limit: int) -> List[bool]:
        sieve = [False] * (limit + 1)
        sieve[2] = sieve[3] = True
        
        for x in range(1, int(limit**0.5) + 1):
            for y in range(1, int(limit**0.5) + 1):
                n = 4 * x**2 + y**2
                if n <= limit and n % 12 in (1, 5):
                    sieve[n] = not sieve[n]
                n = 3 * x**2 + y**2
                if n <= limit and n % 12 == 7:
                    sieve[n] = not sieve[n]
                n = 3 * x**2 - y**2
                if x > y and n <= limit and n % 12 == 11:
                    sieve[n] = not sieve[n]
        
        for n in range(5, int(limit**0.5) + 1):
            if sieve[n]:
                sieve[n*n::n*n] = [False] * len(sieve[n*n::n*n])
        
        return sieve

    # Dynamic start point based on max(num_books, wordperbook)
    limit = 10**6  # Upper limit for primes (can be increased if needed)
    start = 2*max(num_books, wordperbook)
    
    # Ensure start is not too low to avoid small primes
    start = max(1000, start)

    sieve = sieve_of_atkin(limit)
    
    # Return the primes in reverse order, starting from the first prime greater than or equal to 'start'
    primes = [p for p in range(start, limit + 1) if sieve[p]]
    return primes[::-1]



def generate_unique_book_titles(num_titles: int, min_words: int = 1, max_words: int = 5) -> List[str]:
    word_list = [''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))) for _ in range(num_titles * max_words)]
    titles = set()
    while len(titles) < num_titles:
        title = ''.join(random.sample(word_list, random.randint(min_words, max_words)))
        titles.add(title)
    return list(titles)

def create_book(word_count: int) -> List[str]:
    return random.choices(string.ascii_letters, k=word_count)

def generate_test_case(num_books: int, words_per_book: int) -> Tuple[List[str], Iterator[List[str]]]:
    titles = generate_unique_book_titles(num_books)
    books = (create_book(words_per_book) for _ in range(num_books))
    return titles, books


def measure_method_time_for_all_books(lib, method_name, book_titles, word_to_books):
    start_time = time.time()
    
    if method_name == 'distinct_words' or method_name == 'count_distinct_words':
        for title in book_titles:
            getattr(lib, method_name)(title)
    elif method_name == 'search_keyword':
        for word in word_to_books:
            lib.search_keyword(word)
    
    return time.time() - start_time

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n: int) -> int:
    prime = n
    while not is_prime(prime):
        prime += 1
    return prime
def prev_prime(n: int) -> int:
    prime = n - 1
    while prime > 2 and not is_prime(prime):
        prime -= 1
    return prime

# In generate_params:

def generate_params(name: str, num_books: int, avg_words_per_book: int) -> Tuple[int, int, int, int]:
    # Dynamically choose a prime table size based on the larger of num_books or avg_words_per_book
    table_size = next_prime(max(num_books, avg_words_per_book))

    if name == "Bezos":
        # Bezos uses 4 parameters:
        # - z1: A prime number, dynamically chosen as roughly half of the table size
        # - z2: A smaller prime number (based on z1), dynamically chosen to be slightly smaller than z1
        # - c2: A prime number, used for the second hash function (for double hashing), smaller than z1 and table_size
        # - table_size: The size of the hash table, should be prime
        
        z1 = next_prime(table_size // 2)  # Primary hash multiplier
        z2 = prev_prime(z1)         # Secondary hash multiplier, should be distinct from z1
        c2 = next_prime(table_size // 3)
        while c2 >= table_size:
            c2 = prev_prime(c2 - 1) # A prime number smaller than table_size for secondary hash compression

        return (z1, z2, c2, table_size)
    
    else:
        # For Jobs and Gates:
        # - z_value: A prime number used for polynomial accumulation (z1 equivalent)
        # - table_size: The size of the hash table, should be prime
        
        z_value = next_prime(table_size // 2)  # Primary hash multiplier
        return (z_value, table_size)
# def generate_params(name: str, num_books: int, avg_words_per_book: int) -> Tuple[int, int, int, int]:   
#     if name == "Bezos":

#         return (10,37,7,13)
#     elif name == "Jobs":
#         # For Jobs and Gates, where params are (z, table_size)  # Cap table_size as well
#         return (10, 29)
#     elif name == "Gates":
#         # For Jobs and Gates, where params are (z, table_size)
#         return (10,37)
def check_lib(lib, book_titles, unique_words, word_to_books, is_jgb=False):
    for i, book_title in enumerate(book_titles):
        book_words = lib.distinct_words(book_title)

        if is_jgb:
            if set(book_words) == set(unique_words[i]):
                pass
            else:
                print(f"DISTINCT WORDS FAILED for {book_title}!")
        else:
            if book_words == unique_words[i]:
                pass
            else:
                print(f"DISTINCT WORDS FAILED for {book_title}!")

        if lib.count_distinct_words(book_title) == len(unique_words[i]):
            pass
        else:
            print(f"COUNT DISTINCT WORDS FAILED for {book_title}!",lib.name)

    if is_jgb:
        for word in word_to_books:
            search_results = lib.search_keyword(word)
            if set(search_results) == set(word_to_books[word]):
                pass
            else:
                print(f"SEARCH KEYWORD '{word}' FAILED!")
    else:
        for word in word_to_books:
            search_results = lib.search_keyword(word)
            if search_results == sorted(word_to_books[word]):
                pass
            else:
                print(f"SEARCH KEYWORD '{word}' FAILED!")

    print("\n\n")
    
def run_test_case(num_books: int, words_per_book: int) -> List[Tuple[str, str, int, int, float]]:
    results = []
    prime_list = get_primes(num_books, words_per_book)

    book_titles, texts = generate_test_case(num_books, words_per_book)
    texts_list = list(texts)  # Convert generator to list for multiple use

    # Generate unique words and word_to_books like KJ_V3.2
    unique_words = []
    for text in texts_list:
        unique = []
        for word in text:
            if word not in unique:
                unique.append(word)
        unique_words.append(sorted(unique))

    word_to_books = {}
    for book, text in zip(book_titles, texts_list):
        for word in text:
            if word not in word_to_books:
                word_to_books[word] = [book]
            else:
                if book not in word_to_books[word]:
                    word_to_books[word].append(book)

    # Test MuskLibrary
    init_start_time = time.time()
    musk_lib = library.MuskLibrary(book_titles, texts_list)
    init_time = time.time() - init_start_time
    results.append(("MuskLibrary", "__init__", num_books, words_per_book, init_time))

    # Measure time for all books and words for MuskLibrary methods
    for method in ['distinct_words', 'count_distinct_words', 'search_keyword']:
        method_time = measure_method_time_for_all_books(musk_lib, method, book_titles, word_to_books)
        results.append(("MuskLibrary", method, num_books, words_per_book, method_time))

    # Check correctness for MuskLibrary
    check_lib(musk_lib, book_titles, unique_words, word_to_books)

    del musk_lib
    gc.collect()

    # Test JGBLibraries
    set_primes(prime_list)
    for name in ["Jobs", "Gates", "Bezos"]:
        lib = library.JGBLibrary(name, generate_params(name, num_books, words_per_book))
        obj = zip(book_titles, texts_list)
        
        # Measure time for adding all books to JGB library
        add_book_start_time = time.time()
        for book, text in obj:
            lib.add_book(book, text)
        add_book_time = time.time() - add_book_start_time
        results.append((name, "add_book", num_books, words_per_book, add_book_time))

        # Measure time for all books and words for JGBLibrary methods
        for method in ['distinct_words', 'count_distinct_words', 'search_keyword']:
            method_time = measure_method_time_for_all_books(lib, method, book_titles, word_to_books)
            results.append((name, method, num_books, words_per_book, method_time))

        # Check correctness for JGBLibraries
        check_lib(lib, book_titles, unique_words, word_to_books, is_jgb=True)

        del lib
        gc.collect()

    del book_titles, texts_list
    gc.collect()
    return results


def run_tests() -> None:
    all_results = []
    test_cases = [
        (100, 10000),
        (200, 10000),
        (400, 10000),
        (800, 10000)
        # More cases can be added here
    ]

    for num_books, words_per_book in test_cases:
        print(f"\nRunning Test Case: {num_books} books, {words_per_book} words per book")
        results = run_test_case(num_books, words_per_book)
        all_results.extend(results)
        gc.collect()

    print_time_complexity_table(all_results)
    
def print_time_complexity_table(results: List[Tuple[str, str, int, int, float]]) -> None:
    print("\nTime Complexity Results")
    print(f"{'Library':<20}{'Operation':<30}{'Books':<10}{'Avg Words/Book':<20}{'Time (s)':<15}")
    print("=" * 95)
    for result in results:
        library_name, operation, books, avg_words_per_book, time_taken = result
        print(f"{library_name:<20}{operation:<30}{books:<10}{avg_words_per_book:<20.2f}{time_taken:.6f}")
    print("=" * 95)

if __name__ == "__main__":
    run_tests()

