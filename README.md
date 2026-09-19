<div align="center">

# ecomerce  

**A documented software project by [Bhuvaneshwaran S](https://github.com/bhuvanesh6566).**

[![GitHub](https://img.shields.io/badge/GitHub-bhuvanesh6566-181717?logo=github)](https://github.com/bhuvanesh6566)
[![Issues](https://img.shields.io/github/issues/bhuvanesh6566/ecomerce--)](https://github.com/bhuvanesh6566/ecomerce--/issues)

[Source Code](https://github.com/bhuvanesh6566/ecomerce--) · [Report a Bug](https://github.com/bhuvanesh6566/ecomerce--/issues)

</div>

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## About

This README uses a consistent project-documentation format while preserving the repository's existing technical documentation below.

## Features

- ✅ Project-specific functionality documented below
- ✅ Setup and usage information
- ✅ Extensible project structure

## Tech Stack

See the project documentation below for the technologies used by this repository.

## Getting Started

Clone the repository and follow the project-specific setup instructions below.

```bash
git clone https://github.com/bhuvanesh6566/ecomerce--.git
cd ecomerce--
```

## Usage

Use the project-specific commands documented below.

## Project Structure

Refer to the repository tree and the detailed documentation below.

## Roadmap

- [ ] Add screenshots or demo GIF
- [ ] Expand setup/troubleshooting documentation
- [ ] Add automated testing documentation

## Contributing

Open an issue for bugs or feature requests, then submit focused pull requests with clear descriptions.

## License

See [LICENSE](LICENSE) if present.

---

# Project Documentation

# E-Commerce Product Search and Recommendation System

A comprehensive product search and recommendation system implementing efficient data structures and algorithms for fast product lookups, dynamic sorting, and intelligent indexing.

## 🎯 Features

- **Hash Table Implementation**: Separate Chaining and Open Addressing for O(1) average lookup
- **Binary Search**: Fast O(log n) lookup in sorted arrays
- **Advanced Sorting**: Quick Sort and Merge Sort algorithms
- **Hybrid Search**: Combines hash table and binary search for optimal performance
- **Modern Web UI**: Beautiful, responsive interface for product browsing
- **Dynamic Sorting**: Sort by price, rating, popularity, name, or ID
- **Real-time Search**: Instant product search by name or ID

## 🏗️ Architecture

### Core Components

1. **Product Class** (`product.py`)
   - Product data structure with ID, name, price, rating, and popularity

2. **Hash Table** (`hash_table.py`)
   - Separate Chaining implementation
   - Open Addressing (Linear Probing) implementation
   - Automatic resizing when load factor exceeds 0.75

3. **Binary Search** (`binary_search.py`)
   - Search by ID (O(log n))
   - Search by name (exact and partial match)

4. **Sorting Algorithms** (`sorting.py`)
   - Quick Sort (fast average performance)
   - Merge Sort (stable sort, preserves order for equal values)

5. **Search Engine** (`search_engine.py`)
   - Combines hash table and binary search
   - Intelligent routing based on query type

6. **Backend API** (`app.py`)
   - Flask REST API
   - Endpoints for search, sort, and product management

7. **Frontend** (`templates/index.html`, `static/`)
   - Modern, responsive web interface
   - Real-time search and sorting

## 🚀 Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Search Products
- Enter a product name or ID in the search bar
- Click "Search" or press Enter
- Results are displayed instantly

### Sort Products
- Select sort criteria (Price, Rating, Popularity, Name, ID)
- Choose sort order (Ascending/Descending)
- Select algorithm (Merge Sort/Quick Sort)
- Click "Apply Sort"

### API Endpoints

- `GET /api/products` - Get all products (with optional sorting)
  - Query params: `sort_by`, `order`, `algorithm`
  
- `GET /api/products/search?q=<query>` - Search products
  
- `GET /api/products/<id>` - Get product by ID
  
- `POST /api/products` - Add new product
  - Body: `{product_id, name, price, rating, popularity}`
  
- `DELETE /api/products/<id>` - Delete product
  
- `GET /api/stats` - Get catalog statistics

## 🧮 Algorithm Complexity

| Operation | Hash Table | Binary Search | Sorting |
|-----------|-----------|---------------|---------|
| Search by ID | O(1) avg | O(log n) | - |
| Search by Name | O(n) | O(log n) | - |
| Insert | O(1) avg | - | - |
| Delete | O(1) avg | - | - |
| Sort | - | - | O(n log n) |

## 🧪 Example Usage (Python)

```python
from search_engine import SearchEngine
from product import Product

# Initialize search engine
engine = SearchEngine(hash_type='chaining')

# Add products
product = Product(1, "Laptop", 999.99, 4.5, 1000)
engine.add_product(product)

# Search by ID
result = engine.search_by_id(1)

# Search by name
results = engine.search_by_name("Laptop")

# Sort products
sorted_products = engine.sort_products(sort_by='price', order='asc', algorithm='merge')
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Instant search and sort results
- **Beautiful Cards**: Modern product card design
- **Statistics Display**: Total products and result count
- **Error Handling**: User-friendly error messages

## 🔧 Configuration

You can switch between hash table implementations in `app.py`:

```python
# Separate Chaining (default)
search_engine = SearchEngine(hash_type='chaining')

# Open Addressing
search_engine = SearchEngine(hash_type='open')
```

## 📊 Sample Data

The system comes pre-loaded with 15 sample products including:
- Laptops and computers
- Peripherals (mice, keyboards, monitors)
- Accessories (cables, stands, cases)
- Audio devices (headphones, speakers)

## 🚀 Possible Extensions

- [ ] Recommendation engine based on rating similarity
- [ ] Caching for frequently accessed searches
- [ ] Pagination for large result sets
- [ ] Database integration (MySQL/PostgreSQL)
- [ ] User authentication and favorites
- [ ] Product categories and filtering
- [ ] Advanced search with multiple criteria

## 👥 Team Roles

- **Catalog Engineer**: Hash table implementation
- **Search Engineer**: Binary search and indexing
- **Sorting Engineer**: Quick Sort and Merge Sort
- **Frontend Developer**: Web UI and user experience

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to extend this project with additional features and improvements!





