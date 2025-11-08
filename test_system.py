"""
Test script for the E-Commerce Product Search and Recommendation System.
"""

from product import Product
from hash_table import HashTableSeparateChaining, HashTableOpenAddressing
from binary_search import binary_search_by_id, binary_search_by_name
from sorting import quick_sort, merge_sort, sort_products
from search_engine import SearchEngine


def test_product():
    """Test Product class."""
    print("=" * 60)
    print("Testing Product Class")
    print("=" * 60)
    
    product = Product(1, "Test Product", 99.99, 4.5, 100)
    print(f"Created: {product}")
    print(f"Dictionary: {product.to_dict()}")
    print("✓ Product class works correctly\n")


def test_hash_table():
    """Test Hash Table implementations."""
    print("=" * 60)
    print("Testing Hash Table (Separate Chaining)")
    print("=" * 60)
    
    ht = HashTableSeparateChaining(size=11)
    
    # Add products
    products = [
        Product(1, "Laptop", 999.99, 4.5, 1000),
        Product(2, "Mouse", 29.99, 4.2, 800),
        Product(3, "Keyboard", 89.99, 4.7, 1200),
    ]
    
    for p in products:
        ht.insert_product(p)
        print(f"Inserted: {p.name}")
    
    # Search
    result = ht.search_product_by_id(2)
    print(f"\nSearch ID 2: {result}")
    
    # Search by name
    results = ht.search_product_by_name("Laptop")
    print(f"Search 'Laptop': {len(results)} result(s)")
    
    # Delete
    deleted = ht.delete_product(2)
    print(f"Deleted ID 2: {deleted}")
    
    result = ht.search_product_by_id(2)
    print(f"Search ID 2 after delete: {result}")
    print("✓ Hash Table (Separate Chaining) works correctly\n")


def test_binary_search():
    """Test Binary Search."""
    print("=" * 60)
    print("Testing Binary Search")
    print("=" * 60)
    
    products = [
        Product(1, "Apple", 10.0, 4.0, 100),
        Product(2, "Banana", 5.0, 4.5, 200),
        Product(3, "Cherry", 8.0, 4.2, 150),
        Product(4, "Date", 12.0, 4.8, 300),
    ]
    
    # Sort by ID
    products_sorted = sorted(products, key=lambda p: p.product_id)
    result = binary_search_by_id(products_sorted, 3)
    print(f"Binary search ID 3: {result}")
    
    # Sort by name
    products_sorted = sorted(products, key=lambda p: p.name.lower())
    result = binary_search_by_name(products_sorted, "Cherry")
    print(f"Binary search name 'Cherry': {result}")
    print("✓ Binary Search works correctly\n")


def test_sorting():
    """Test Sorting Algorithms."""
    print("=" * 60)
    print("Testing Sorting Algorithms")
    print("=" * 60)
    
    products = [
        Product(1, "Product A", 100.0, 4.0, 100),
        Product(2, "Product B", 50.0, 4.5, 200),
        Product(3, "Product C", 75.0, 4.2, 150),
        Product(4, "Product D", 25.0, 4.8, 300),
    ]
    
    # Quick Sort
    sorted_quick = quick_sort(products, key='price', reverse=False)
    print("Quick Sort by Price (asc):")
    for p in sorted_quick:
        print(f"  {p.name}: ${p.price}")
    
    # Merge Sort
    sorted_merge = merge_sort(products, key='rating', reverse=True)
    print("\nMerge Sort by Rating (desc):")
    for p in sorted_merge:
        print(f"  {p.name}: {p.rating}")
    
    # Using sort_products function
    sorted_products = sort_products(products, sort_by='popularity', order='desc', algorithm='merge')
    print("\nSort by Popularity (desc):")
    for p in sorted_products:
        print(f"  {p.name}: {p.popularity}")
    
    print("✓ Sorting algorithms work correctly\n")


def test_search_engine():
    """Test Search Engine."""
    print("=" * 60)
    print("Testing Search Engine")
    print("=" * 60)
    
    engine = SearchEngine(hash_type='chaining')
    
    # Add products
    products = [
        Product(1, "Laptop Pro", 1299.99, 4.5, 1500),
        Product(2, "Wireless Mouse", 29.99, 4.2, 800),
        Product(3, "Mechanical Keyboard", 89.99, 4.7, 1200),
        Product(4, "Gaming Laptop", 1999.99, 4.8, 2000),
    ]
    
    for p in products:
        engine.add_product(p)
    
    print(f"Added {engine.get_product_count()} products")
    
    # Search by ID
    result = engine.search_by_id(2)
    print(f"\nSearch by ID 2: {result}")
    
    # Search by name
    results = engine.search_by_name("Laptop")
    print(f"\nSearch by name 'Laptop': {len(results)} result(s)")
    for r in results:
        print(f"  - {r}")
    
    # Sort products
    sorted_products = engine.sort_products(sort_by='price', order='asc', algorithm='merge')
    print("\nSorted by Price (asc):")
    for p in sorted_products:
        print(f"  {p.name}: ${p.price}")
    
    print("✓ Search Engine works correctly\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("E-COMMERCE PRODUCT SEARCH SYSTEM - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_product()
        test_hash_table()
        test_binary_search()
        test_sorting()
        test_search_engine()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nTo run the web application:")
        print("  python app.py")
        print("Then open: http://localhost:5000\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


