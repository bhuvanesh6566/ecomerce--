"""
Search and Indexing Module combining Hash Table and Binary Search.
"""

from hash_table import HashTableSeparateChaining, HashTableOpenAddressing
from binary_search import binary_search_by_id, binary_search_by_name, binary_search_partial_name
from sorting import sort_products
from product import Product


class SearchEngine:
    """Search engine combining hash table and binary search for efficient lookups."""
    
    def __init__(self, hash_type='chaining'):
        """
        Initialize the search engine.
        
        Args:
            hash_type: 'chaining' or 'open' for hash table type
        """
        if hash_type == 'chaining':
            self.hash_table = HashTableSeparateChaining()
        else:
            self.hash_table = HashTableOpenAddressing()
        
        self.products_list = []  # For binary search
        self.sorted_by_id = False
        self.sorted_by_name = False
    
    def add_product(self, product):
        """
        Add a product to both hash table and list.
        
        Args:
            product: Product object to add
        """
        self.hash_table.insert_product(product)
        self.products_list.append(product)
        self.sorted_by_id = False
        self.sorted_by_name = False
    
    def remove_product(self, product_id):
        """
        Remove a product from both hash table and list.
        
        Args:
            product_id: ID of product to remove
            
        Returns:
            True if removed, False otherwise
        """
        success = self.hash_table.delete_product(product_id)
        if success:
            self.products_list = [p for p in self.products_list if p.product_id != product_id]
            self.sorted_by_id = False
            self.sorted_by_name = False
        return success
    
    def search_by_id(self, product_id):
        """
        Search for product by ID using hash table (O(1) average).
        
        Args:
            product_id: ID to search for
            
        Returns:
            Product if found, None otherwise
        """
        return self.hash_table.search_product_by_id(product_id)
    
    def search_by_name_hash(self, name):
        """
        Search for products by name using hash table.
        
        Args:
            name: Name or partial name to search
            
        Returns:
            List of matching products
        """
        return self.hash_table.search_product_by_name(name)
    
    def search_by_name_binary(self, name, exact=False):
        """
        Search for products by name using binary search.
        Requires products to be sorted by name first.
        
        Args:
            name: Name to search for
            exact: If True, search for exact match only
            
        Returns:
            List of matching products
        """
        if not self.sorted_by_name:
            self.products_list = sort_products(self.products_list, sort_by='name', order='asc')
            self.sorted_by_name = True
        
        if exact:
            product = binary_search_by_name(self.products_list, name)
            return [product] if product else []
        else:
            return binary_search_partial_name(self.products_list, name)
    
    def search_by_name(self, name, use_binary=True):
        """
        Hybrid search: Try binary search first, fallback to hash table.
        
        Args:
            name: Name or partial name to search
            use_binary: If True, prefer binary search (faster for sorted data)
            
        Returns:
            List of matching products
        """
        if use_binary and len(self.products_list) > 10:
            # Use binary search for larger datasets
            return self.search_by_name_binary(name, exact=False)
        else:
            # Use hash table search (linear scan, but simpler)
            return self.search_by_name_hash(name)
    
    def get_all_products(self):
        """Get all products from the catalog."""
        return self.products_list.copy()
    
    def sort_products(self, sort_by='price', order='asc', algorithm='merge'):
        """
        Sort all products by specified criteria.
        
        Args:
            sort_by: Sort criteria ('price', 'rating', 'popularity', 'name', 'id')
            order: Sort order ('asc' or 'desc')
            algorithm: Sorting algorithm ('quick' or 'merge')
            
        Returns:
            Sorted list of products
        """
        return sort_products(self.products_list, sort_by=sort_by, order=order, algorithm=algorithm)
    
    def get_product_count(self):
        """Get total number of products."""
        return len(self.products_list)


