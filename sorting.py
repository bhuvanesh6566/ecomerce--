"""
Sorting algorithms: Quick Sort and Merge Sort for product ranking.
"""

from product import Product


def quick_sort(products, key='price', reverse=False):
    """
    Quick Sort implementation for products.
    
    Args:
        products: List of products to sort
        key: Sort key ('price', 'rating', 'popularity', 'name', 'id')
        reverse: If True, sort in descending order
        
    Returns:
        Sorted list of products
    """
    if len(products) <= 1:
        return products
    
    products = products.copy()  # Don't modify original
    
    def get_value(product):
        if key == 'price':
            return product.price
        elif key == 'rating':
            return product.rating
        elif key == 'popularity':
            return product.popularity
        elif key == 'name':
            return product.name.lower()
        elif key == 'id':
            return product.product_id
        else:
            return product.price
    
    def partition(arr, low, high):
        pivot = get_value(arr[high])
        i = low - 1
        
        for j in range(low, high):
            if reverse:
                if get_value(arr[j]) >= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            else:
                if get_value(arr[j]) <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)
    
    quick_sort_helper(products, 0, len(products) - 1)
    return products


def merge_sort(products, key='price', reverse=False):
    """
    Merge Sort implementation for products (stable sort).
    
    Args:
        products: List of products to sort
        key: Sort key ('price', 'rating', 'popularity', 'name', 'id')
        reverse: If True, sort in descending order
        
    Returns:
        Sorted list of products
    """
    if len(products) <= 1:
        return products
    
    products = products.copy()  # Don't modify original
    
    def get_value(product):
        if key == 'price':
            return product.price
        elif key == 'rating':
            return product.rating
        elif key == 'popularity':
            return product.popularity
        elif key == 'name':
            return product.name.lower()
        elif key == 'id':
            return product.product_id
        else:
            return product.price
    
    def compare(a, b):
        """Compare two values based on reverse flag."""
        val_a = get_value(a)
        val_b = get_value(b)
        
        if isinstance(val_a, str) and isinstance(val_b, str):
            if reverse:
                return val_a >= val_b
            return val_a <= val_b
        else:
            if reverse:
                return val_a >= val_b
            return val_a <= val_b
    
    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if compare(left[i], right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        
        return merge(left, right)
    
    return merge_sort_helper(products)


def sort_products(products, sort_by='price', order='asc', algorithm='merge'):
    """
    Sort products using specified algorithm and criteria.
    
    Args:
        products: List of products to sort
        sort_by: Sort criteria ('price', 'rating', 'popularity', 'name', 'id')
        order: Sort order ('asc' or 'desc')
        algorithm: Sorting algorithm ('quick' or 'merge')
        
    Returns:
        Sorted list of products
    """
    reverse = (order == 'desc')
    
    if algorithm == 'quick':
        return quick_sort(products, key=sort_by, reverse=reverse)
    else:  # merge sort (default, stable)
        return merge_sort(products, key=sort_by, reverse=reverse)


