

"""
Flask backend server for the E-Commerce Product Search and Recommendation System.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from search_engine import SearchEngine
from product import Product
from recommendation_engine import RecommendationEngine
import json

app = Flask(__name__)
CORS(app)

# Initialize search engine
search_engine = SearchEngine(hash_type='chaining')

# Initialize recommendation engine
recommendation_engine = RecommendationEngine(search_engine)

# Sample products data with images and categories
sample_products = [
    # Original 15 products with fixed images
    Product(1, "Laptop Pro 15", 1299.99, 4.5, 1500, 
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop&q=80", "Laptops"),
    Product(2, "Wireless Mouse", 29.99, 4.2, 800,
            "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(3, "Mechanical Keyboard", 89.99, 4.7, 1200,
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(4, "Gaming Laptop", 1999.99, 4.8, 2000,
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop&q=80", "Laptops"),
    Product(5, "USB-C Cable", 19.99, 4.0, 600,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Cables"),
    Product(6, "Monitor 27 inch", 349.99, 4.6, 900,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Monitors"),
    Product(7, "Webcam HD", 79.99, 4.3, 700,
            "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(8, "Laptop Stand", 49.99, 4.4, 500,
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(9, "External SSD 1TB", 129.99, 4.7, 1100,
            "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=400&h=400&fit=crop&q=80", "Storage"),
    Product(10, "Noise Cancelling Headphones", 299.99, 4.9, 1800,
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(11, "Smartphone Case", 24.99, 4.1, 400,
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(12, "Tablet 10 inch", 449.99, 4.5, 750,
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop&q=80", "Tablets"),
    Product(13, "Bluetooth Speaker", 59.99, 4.3, 650,
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(14, "Power Bank 20000mAh", 39.99, 4.2, 550,
            "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c8?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(15, "Wireless Charger", 34.99, 4.0, 450,
            "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400&h=400&fit=crop&q=80", "Accessories"),
    
    # Additional 50 products
    Product(16, "Ultrabook 14 inch", 1199.99, 4.6, 1400,
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop&q=80", "Laptops"),
    Product(17, "Gaming Mouse RGB", 59.99, 4.5, 950,
            "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(18, "RGB Gaming Keyboard", 129.99, 4.8, 1300,
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(19, "4K Monitor 32 inch", 599.99, 4.7, 1100,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Monitors"),
    Product(20, "USB Hub 7-Port", 34.99, 4.3, 600,
            "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(21, "HDMI Cable 2m", 14.99, 4.1, 500,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Cables"),
    Product(22, "Gaming Headset", 149.99, 4.6, 1200,
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(23, "External HDD 2TB", 79.99, 4.4, 800,
            "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=400&h=400&fit=crop&q=80", "Storage"),
    Product(24, "Tablet Stand Adjustable", 39.99, 4.2, 550,
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(25, "Smartphone 128GB", 699.99, 4.7, 1600,
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&q=80", "Smartphones"),
    Product(26, "Smartwatch Pro", 249.99, 4.5, 1100,
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&q=80", "Wearables"),
    Product(27, "Wireless Earbuds", 89.99, 4.4, 900,
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(28, "Laptop Cooling Pad", 29.99, 4.1, 450,
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(29, "USB Flash Drive 64GB", 19.99, 4.0, 400,
            "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=400&h=400&fit=crop&q=80", "Storage"),
    Product(30, "Monitor Stand Dual", 69.99, 4.3, 650,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(31, "Mechanical Keyboard TKL", 99.99, 4.6, 1150,
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(32, "Gaming Chair Ergonomic", 299.99, 4.5, 1300,
            "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400&h=400&fit=crop&q=80", "Furniture"),
    Product(33, "Desk Lamp LED", 49.99, 4.2, 600,
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop&q=80", "Furniture"),
    Product(34, "Webcam 1080p", 89.99, 4.4, 750,
            "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(35, "Microphone USB", 79.99, 4.3, 700,
            "https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(36, "Graphics Tablet", 199.99, 4.6, 1000,
            "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(37, "Laptop Sleeve 15 inch", 24.99, 4.1, 450,
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(38, "Screen Protector Pack", 12.99, 3.9, 350,
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(39, "Cable Management Kit", 19.99, 4.0, 400,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(40, "Desk Mat Large", 34.99, 4.2, 550,
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(41, "Monitor Arm VESA", 79.99, 4.4, 700,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(42, "Thunderbolt 3 Cable", 39.99, 4.3, 600,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Cables"),
    Product(43, "Ethernet Cable Cat6", 9.99, 4.0, 300,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Cables"),
    Product(44, "WiFi Router AC1900", 129.99, 4.5, 900,
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop&q=80", "Networking"),
    Product(45, "Network Switch 8-Port", 49.99, 4.2, 500,
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop&q=80", "Networking"),
    Product(46, "Surge Protector 8-Outlet", 24.99, 4.1, 450,
            "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(47, "Laptop Bag Backpack", 59.99, 4.3, 750,
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(48, "USB-C to HDMI Adapter", 29.99, 4.2, 550,
            "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(49, "SD Card Reader", 14.99, 4.0, 400,
            "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(50, "Laptop Lock Cable", 19.99, 3.9, 350,
            "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(51, "Monitor Light Bar", 69.99, 4.4, 650,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(52, "Desk Organizer", 34.99, 4.1, 500,
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop&q=80", "Furniture"),
    Product(53, "Ergonomic Mouse Pad", 24.99, 4.2, 450,
            "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(54, "USB-C Dock Station", 149.99, 4.6, 1100,
            "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(55, "Wireless Presenter", 39.99, 4.1, 500,
            "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(56, "Laptop Privacy Screen", 49.99, 4.0, 450,
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(57, "Tablet Keyboard Case", 79.99, 4.3, 700,
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(58, "Smartphone Gimbal", 99.99, 4.5, 850,
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(59, "Action Camera 4K", 199.99, 4.6, 1200,
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop&q=80", "Cameras"),
    Product(60, "DSLR Camera Bag", 69.99, 4.3, 650,
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(61, "Tripod Stand", 49.99, 4.2, 600,
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop&q=80", "Cameras"),
    Product(62, "Ring Light LED", 59.99, 4.4, 700,
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(63, "Green Screen Backdrop", 39.99, 4.1, 500,
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop&q=80", "Accessories"),
    Product(64, "Microphone Boom Arm", 34.99, 4.2, 550,
            "https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop&q=80", "Audio"),
    Product(65, "Pop Filter Microphone", 14.99, 4.0, 400,
            "https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop&q=80", "Audio"),
]

# Load sample products
for product in sample_products:
    search_engine.add_product(product)


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional sorting."""
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    algorithm = request.args.get('algorithm', 'merge')
    
    products = search_engine.sort_products(sort_by=sort_by, order=order, algorithm=algorithm)
    
    return jsonify({
        'success': True,
        'count': len(products),
        'products': [p.to_dict() for p in products]
    })


@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search for products by name or ID."""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400
    
    results = []
    
    # Try ID search first
    try:
        product_id = int(query)
        product = search_engine.search_by_id(product_id)
        if product:
            results.append(product)
    except ValueError:
        pass
    
    # Search by name (if ID search didn't find anything or query is not numeric)
    if not results:
        results = search_engine.search_by_name(query, use_binary=True)
    
    return jsonify({
        'success': True,
        'count': len(results),
        'products': [p.to_dict() for p in results]
    })


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID."""
    product = search_engine.search_by_id(product_id)
    
    if product:
        return jsonify({
            'success': True,
            'product': product.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404


@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product."""
    try:
        data = request.json
        product = Product(
            product_id=data['product_id'],
            name=data['name'],
            price=data['price'],
            rating=data['rating'],
            popularity=data['popularity'],
            image_url=data.get('image_url'),
            category=data.get('category')
        )
        search_engine.add_product(product)
        
        return jsonify({
            'success': True,
            'product': product.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product by ID."""
    success = search_engine.remove_product(product_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get catalog statistics."""
    return jsonify({
        'success': True,
        'total_products': search_engine.get_product_count()
    })


@app.route('/api/products/<int:product_id>/recommendations', methods=['GET'])
def get_recommendations(product_id):
    """Get product recommendations for a specific product."""
    limit = int(request.args.get('limit', 12))
    recommendations = recommendation_engine.get_recommendations(product_id, limit=limit)
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'count': len(recommendations),
        'recommendations': [p.to_dict() for p in recommendations]
    })


@app.route('/api/recommendations/trending', methods=['GET'])
def get_trending():
    """Get trending products."""
    limit = int(request.args.get('limit', 5))
    trending = recommendation_engine.get_trending_products(limit=limit)
    
    return jsonify({
        'success': True,
        'count': len(trending),
        'products': [p.to_dict() for p in trending]
    })


@app.route('/api/recommendations/category/<category>', methods=['GET'])
def get_category_recommendations(category):
    """Get recommendations by category."""
    limit = int(request.args.get('limit', 5))
    recommendations = recommendation_engine.get_recommendations_by_category(category, limit=limit)
    
    return jsonify({
        'success': True,
        'category': category,
        'count': len(recommendations),
        'products': [p.to_dict() for p in recommendations]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)


