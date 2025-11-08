"""
Product class definition for the E-Commerce system.
"""

class Product:
    """Represents a product in the catalog."""
    
    def __init__(self, product_id, name, price, rating, popularity, image_url=None, category=None):
        """
        Initialize a product.
        
        Args:
            product_id: Unique identifier for the product
            name: Product name
            price: Product price
            rating: Product rating (0-5)
            popularity: Product popularity score
            image_url: URL to product image
            category: Product category
        """
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.rating = float(rating)
        self.popularity = int(popularity)
        self.image_url = image_url or "https://via.placeholder.com/300x300?text=No+Image"
        self.category = category or "General"
    
    def __str__(self):
        return f"Product(ID={self.product_id}, Name={self.name}, Price=${self.price:.2f}, Rating={self.rating}, Popularity={self.popularity})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.product_id == other.product_id
        return False
    
    def __hash__(self):
        return hash(self.product_id)
    
    def to_dict(self):
        """Convert product to dictionary for JSON serialization."""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'rating': self.rating,
            'popularity': self.popularity,
            'image_url': self.image_url,
            'category': self.category
        }


