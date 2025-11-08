"""
Hash Table implementation with Separate Chaining and Open Addressing.
"""

from product import Product


class HashTableSeparateChaining:
    """Hash table using separate chaining for collision resolution."""
    
    def __init__(self, size=101):
        """
        Initialize hash table with separate chaining.
        
        Args:
            size: Initial size of the hash table (should be prime)
        """
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key):
        """Hash function using string folding."""
        if isinstance(key, int):
            key = str(key)
        
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def insert_product(self, product):
        """
        Insert a product into the hash table.
        
        Args:
            product: Product object to insert
        """
        key = product.product_id
        index = self._hash(key)
        
        # Check if product already exists
        for i, p in enumerate(self.table[index]):
            if p.product_id == key:
                self.table[index][i] = product  # Update existing
                return
        
        # Insert new product
        self.table[index].append(product)
        self.count += 1
        
        # Resize if load factor > 0.75
        if self.count > self.size * 0.75:
            self._resize()
    
    def _resize(self):
        """Resize the hash table when load factor is too high."""
        old_table = self.table
        old_size = self.size
        self.size = self._next_prime(self.size * 2)
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        # Rehash all elements
        for bucket in old_table:
            for product in bucket:
                self.insert_product(product)
    
    def _next_prime(self, n):
        """Find the next prime number >= n."""
        if n <= 2:
            return 2
        if n % 2 == 0:
            n += 1
        while not self._is_prime(n):
            n += 2
        return n
    
    def _is_prime(self, n):
        """Check if a number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def search_product_by_id(self, product_id):
        """
        Search for a product by ID.
        
        Args:
            product_id: ID of the product to search
            
        Returns:
            Product object if found, None otherwise
        """
        index = self._hash(product_id)
        for product in self.table[index]:
            if product.product_id == product_id:
                return product
        return None
    
    def search_product_by_name(self, name):
        """
        Search for products by name (partial match).
        
        Args:
            name: Name or partial name to search
            
        Returns:
            List of matching products
        """
        results = []
        name_lower = name.lower()
        for bucket in self.table:
            for product in bucket:
                if name_lower in product.name.lower():
                    results.append(product)
        return results
    
    def delete_product(self, product_id):
        """
        Delete a product from the hash table.
        
        Args:
            product_id: ID of the product to delete
            
        Returns:
            True if deleted, False if not found
        """
        index = self._hash(product_id)
        for i, product in enumerate(self.table[index]):
            if product.product_id == product_id:
                del self.table[index][i]
                self.count -= 1
                return True
        return False
    
    def get_all_products(self):
        """Get all products from the hash table."""
        products = []
        for bucket in self.table:
            products.extend(bucket)
        return products


class HashTableOpenAddressing:
    """Hash table using open addressing (linear probing) for collision resolution."""
    
    def __init__(self, size=101):
        """
        Initialize hash table with open addressing.
        
        Args:
            size: Initial size of the hash table (should be prime)
        """
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.DELETED = object()  # Marker for deleted entries
    
    def _hash(self, key):
        """Hash function using string folding."""
        if isinstance(key, int):
            key = str(key)
        
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def _probe(self, key, start_index):
        """
        Linear probing to find next available slot.
        
        Args:
            key: The key to hash
            start_index: Starting index from hash function
            
        Returns:
            Index of available slot
        """
        index = start_index
        attempts = 0
        while attempts < self.size:
            if self.table[index] is None or self.table[index] == self.DELETED:
                return index
            if isinstance(self.table[index], Product) and self.table[index].product_id == key:
                return index
            index = (index + 1) % self.size
            attempts += 1
        raise Exception("Hash table is full")
    
    def insert_product(self, product):
        """
        Insert a product into the hash table.
        
        Args:
            product: Product object to insert
        """
        key = product.product_id
        start_index = self._hash(key)
        index = self._probe(key, start_index)
        
        if self.table[index] is None or self.table[index] == self.DELETED:
            self.count += 1
        
        self.table[index] = product
        
        # Resize if load factor > 0.75
        if self.count > self.size * 0.75:
            self._resize()
    
    def _resize(self):
        """Resize the hash table when load factor is too high."""
        old_table = self.table
        old_size = self.size
        self.size = self._next_prime(self.size * 2)
        self.table = [None] * self.size
        self.count = 0
        
        # Rehash all elements
        for item in old_table:
            if item is not None and item != self.DELETED:
                self.insert_product(item)
    
    def _next_prime(self, n):
        """Find the next prime number >= n."""
        if n <= 2:
            return 2
        if n % 2 == 0:
            n += 1
        while not self._is_prime(n):
            n += 2
        return n
    
    def _is_prime(self, n):
        """Check if a number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def search_product_by_id(self, product_id):
        """
        Search for a product by ID.
        
        Args:
            product_id: ID of the product to search
            
        Returns:
            Product object if found, None otherwise
        """
        start_index = self._hash(product_id)
        index = start_index
        attempts = 0
        
        while attempts < self.size:
            if self.table[index] is None:
                return None
            if self.table[index] != self.DELETED and isinstance(self.table[index], Product):
                if self.table[index].product_id == product_id:
                    return self.table[index]
            index = (index + 1) % self.size
            attempts += 1
        
        return None
    
    def search_product_by_name(self, name):
        """
        Search for products by name (partial match).
        
        Args:
            name: Name or partial name to search
            
        Returns:
            List of matching products
        """
        results = []
        name_lower = name.lower()
        for item in self.table:
            if item is not None and item != self.DELETED:
                if name_lower in item.name.lower():
                    results.append(item)
        return results
    
    def delete_product(self, product_id):
        """
        Delete a product from the hash table.
        
        Args:
            product_id: ID of the product to delete
            
        Returns:
            True if deleted, False if not found
        """
        start_index = self._hash(product_id)
        index = start_index
        attempts = 0
        
        while attempts < self.size:
            if self.table[index] is None:
                return False
            if self.table[index] != self.DELETED and isinstance(self.table[index], Product):
                if self.table[index].product_id == product_id:
                    self.table[index] = self.DELETED
                    self.count -= 1
                    return True
            index = (index + 1) % self.size
            attempts += 1
        
        return False
    
    def get_all_products(self):
        """Get all products from the hash table."""
        products = []
        for item in self.table:
            if item is not None and item != self.DELETED:
                products.append(item)
        return products


