"""
Binary Search implementation for fast product lookup.
"""

from product import Product


def binary_search_by_id(products, product_id):
    """
    Binary search for product by ID.
    
    Args:
        products: Sorted list of products (by ID)
        product_id: ID to search for
        
    Returns:
        Product object if found, None otherwise
    """
    left, right = 0, len(products) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if products[mid].product_id == product_id:
            return products[mid]
        elif products[mid].product_id < product_id:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def binary_search_by_name(products, name):
    """
    Binary search for products by name (exact match).
    
    Args:
        products: Sorted list of products (by name)
        name: Name to search for
        
    Returns:
        Product object if found, None otherwise
    """
    left, right = 0, len(products) - 1
    name_lower = name.lower()
    
    while left <= right:
        mid = (left + right) // 2
        mid_name_lower = products[mid].name.lower()
        
        if mid_name_lower == name_lower:
            return products[mid]
        elif mid_name_lower < name_lower:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def binary_search_partial_name(products, name):
    """
    Binary search for products with partial name match.
    Uses binary search to find starting position, then linear search.
    
    Args:
        products: Sorted list of products (by name)
        name: Partial name to search for
        
    Returns:
        List of matching products
    """
    results = []
    name_lower = name.lower()
    
    # Find starting position using binary search
    left, right = 0, len(products) - 1
    start_pos = -1
    
    while left <= right:
        mid = (left + right) // 2
        mid_name_lower = products[mid].name.lower()
        
        if name_lower in mid_name_lower:
            start_pos = mid
            right = mid - 1  # Continue searching left
        elif mid_name_lower < name_lower:
            left = mid + 1
        else:
            right = mid - 1
    
    if start_pos == -1:
        return results
    
    # Linear search from start_pos to find all matches
    i = start_pos
    while i < len(products) and name_lower in products[i].name.lower():
        results.append(products[i])
        i += 1
    
    # Also check backwards for matches that might have been missed
    i = start_pos - 1
    while i >= 0 and name_lower in products[i].name.lower():
        results.insert(0, products[i])
        i -= 1
    
    return results


