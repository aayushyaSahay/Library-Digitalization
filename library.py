import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass

class Book:
    def __init__(self, title, words):
        # Sort words and keep only distinct ones in lexicographical order
        words = self.merge_sort(words)
        self.title = title
        self.words = self.get_distinct(words)

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        sorted_list = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                sorted_list.append(left[i])
                i += 1
            elif left[i] > right[j]:
                sorted_list.append(right[j])
                j += 1
            else:  # Duplicate case
                sorted_list.append(left[i])
                i += 1
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list

    def get_distinct(self, sorted_words):
        distinct_words = []
        last_word = None
        for word in sorted_words:
            if word != last_word:
                distinct_words.append(word)
                last_word = word
        return distinct_words

class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        # Initialize books with title and sorted, distinct words
        new_book_titles = book_titles
        self.books = []
        for title, words in zip(new_book_titles, texts):
            new_words = words
            book = Book(title, new_words)
            self.books.append(book)
        # Sort books lexicographically by title
        self.books = self.merge_sort(self.books, key=lambda b: b.title)
    
    def merge_sort(self, arr, key=lambda x: x):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key)
        right = self.merge_sort(arr[mid:], key)
        return self.merge(left, right, key)
    
    def merge(self, left, right, key):
        sorted_list = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) < key(right[j]):
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list
    
    def binary_search_books(self, title):
        left, right = 0, len(self.books) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.books[mid].title == title:
                return mid
            elif self.books[mid].title < title:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    def binary_search_words(self, words, keyword):
        left, right = 0, len(words) - 1
        while left <= right:
            mid = (left + right) // 2
            if words[mid] == keyword:
                return True
            elif words[mid] < keyword:
                left = mid + 1
            else:
                right = mid - 1
        return False
    
    def distinct_words(self, book_title):
        index = self.binary_search_books(book_title)
        if index != -1:
            return self.books[index].words
        return []
    
    def count_distinct_words(self, book_title):
        index = self.binary_search_books(book_title)
        if index != -1:
            return len(self.books[index].words)
        return 0
    
    def search_keyword(self, keyword):
        result = []
        for book in self.books:
            if self.binary_search_words(book.words, keyword):
                result.append(book.title)
        return result
    
    def print_books(self):
        for book in self.books:
            print(f"{book.title}: {' | '.join(book.words)}")

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.params = params
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        elif name == "Bezos":
            self.collision_type = "Double"
        self.books_map = ht.HashMap(self.collision_type, self.params)
    
    def add_book(self, book_title, text):
        word_set = ht.HashSet(self.collision_type, self.params)
        for word in text:
            word_set.insert(word)
        
        self.books_map.insert((book_title, word_set))
        # self.book_titles.append(book_title) #this work is being done by self.books_map.keys

    def distinct_words(self, book_title):
        # Fetch the HashSet of words and convert it to a list
        word_set = self.books_map.find(book_title)
        # print(word_set.table)
        dist_words = []
        if word_set is not None:
            for word in word_set.table:
                if self.books_map.collision_type == "Chain":
                    if word is not None:
                        for w in word:
                            dist_words.append(w)
                else:
                    if word is not None:
                        dist_words.append(word)
            return dist_words
        return []
    
    def count_distinct_words(self, book_title):
        # Fetch HashSet of words from the HashMap and return its length
        word_set = self.books_map.find(book_title)
        if word_set is not None:
            return len(word_set.keys) # Length of the HashSet of words
        return 0
    
    def search_keyword(self, keyword):
        # Search for the keyword in each book's HashSet of words
        result = []
        for title in self.books_map.keys:
            word_set = self.books_map.find(title)
            if word_set and word_set.find(keyword):  # If the keyword is in the word HashSet
                result.append(title)
        return result
    
    def print_books(self):
        # Print each book title and its corresponding words in the specified format
        if self.collision_type == "Chain":
            for slot in self.books_map.table:
                if slot is None:
                    continue
                for title, word_set in slot:
                    print(f"{title}: {word_set}")
        else:
            for slot in self.books_map.table:
                if slot is None:
                    continue
                print(f"{slot[0]}: {slot[1]}")