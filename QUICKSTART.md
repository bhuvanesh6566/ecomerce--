# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 🧪 Test the System

Run the test suite to verify all components:
```bash
python test_system.py
```

## 📋 What You'll See

1. **15 Sample Products** pre-loaded in the catalog
2. **Search Bar** - Search by product name or ID
3. **Sort Controls** - Sort by Price, Rating, Popularity, Name, or ID
4. **Algorithm Selection** - Choose between Merge Sort (stable) or Quick Sort (fast)
5. **Product Cards** - Beautiful display of product information

## 🔍 Try These Searches

- Search for "Laptop" to see multiple results
- Search for "1" to find product by ID
- Sort by Price (Descending) to see most expensive first
- Sort by Rating (Descending) to see highest rated products

## 🎯 Key Features Demonstrated

- ✅ Hash Table lookup (O(1) average)
- ✅ Binary Search (O(log n))
- ✅ Quick Sort and Merge Sort algorithms
- ✅ Hybrid search combining multiple techniques
- ✅ Modern, responsive web interface

## 🐛 Troubleshooting

**Port already in use?**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Module not found?**
- Make sure you're in the project directory
- Verify all Python files are present
- Check that Flask is installed: `pip install Flask flask-cors`

**Frontend not loading?**
- Check browser console for errors
- Verify Flask is running on port 5000
- Make sure `templates/` and `static/` directories exist

## 📚 Next Steps

- Read the full `README.md` for detailed documentation
- Explore the code to understand the algorithms
- Add your own products via the API
- Extend the system with new features!




