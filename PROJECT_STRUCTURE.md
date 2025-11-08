# Project Structure

```
ecomerce app/
│
├── Core Modules
│   ├── product.py              # Product class definition
│   ├── hash_table.py           # Hash table implementations (Separate Chaining & Open Addressing)
│   ├── binary_search.py        # Binary search algorithms
│   ├── sorting.py              # Quick Sort and Merge Sort implementations
│   └── search_engine.py        # Main search engine combining all components
│
├── Web Application
│   ├── app.py                  # Flask backend server and API
│   ├── templates/
│   │   └── index.html          # Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css       # Modern, responsive styling
│       └── js/
│           └── app.js          # Frontend JavaScript logic
│
├── Testing & Documentation
│   ├── test_system.py          # Comprehensive test suite
│   ├── README.md               # Full documentation
│   ├── QUICKSTART.md           # Quick start guide
│   └── PROJECT_STRUCTURE.md    # This file
│
└── Configuration
    └── requirements.txt        # Python dependencies

```

## Module Responsibilities

### `product.py`
- Defines the `Product` class
- Handles product data structure
- Provides serialization methods

### `hash_table.py`
- **HashTableSeparateChaining**: Uses linked lists for collision resolution
- **HashTableOpenAddressing**: Uses linear probing for collision resolution
- Both support insert, search, and delete operations
- Automatic resizing when load factor > 0.75

### `binary_search.py`
- `binary_search_by_id()`: O(log n) search by product ID
- `binary_search_by_name()`: O(log n) exact name search
- `binary_search_partial_name()`: Partial name matching

### `sorting.py`
- `quick_sort()`: Fast average-case sorting
- `merge_sort()`: Stable sorting (preserves order for equal values)
- `sort_products()`: Unified interface for sorting

### `search_engine.py`
- Combines hash table and binary search
- Intelligent routing based on query type
- Manages product catalog
- Provides unified search interface

### `app.py`
- Flask REST API server
- Endpoints for CRUD operations
- Search and sorting endpoints
- Pre-loaded with 15 sample products

### Frontend (`templates/` & `static/`)
- Modern, responsive UI
- Real-time search and sorting
- Beautiful product cards
- Statistics display

## Data Flow

```
User Input (Search/Sort)
    ↓
Frontend (app.js)
    ↓
API Request (Flask)
    ↓
Search Engine
    ↓
Hash Table / Binary Search / Sorting
    ↓
Results
    ↓
JSON Response
    ↓
Frontend Display
```

## Algorithm Usage

| Operation | Algorithm | Complexity |
|-----------|-----------|------------|
| Search by ID | Hash Table | O(1) avg |
| Search by Name | Binary Search | O(log n) |
| Insert Product | Hash Table | O(1) avg |
| Delete Product | Hash Table | O(1) avg |
| Sort Products | Quick/Merge Sort | O(n log n) |

## Extension Points

1. **Recommendation Engine**: Add to `search_engine.py`
2. **Database Integration**: Replace in-memory storage in `app.py`
3. **Caching**: Add caching layer in `search_engine.py`
4. **Pagination**: Modify API endpoints in `app.py`
5. **Categories**: Extend `Product` class in `product.py`




