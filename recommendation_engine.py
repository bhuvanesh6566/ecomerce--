"""
Recommendation Engine for product recommendations based on similarity.
"""

from product import Product
import math
import re


class RecommendationEngine:
    """Engine for generating product recommendations."""
    
    # Complementary product categories (products that go well together)
    COMPLEMENTARY_CATEGORIES = {
        'Laptops': ['Accessories', 'Monitors', 'Cables', 'Storage'],
        'Monitors': ['Laptops', 'Accessories', 'Cables'],
        'Accessories': ['Laptops', 'Monitors', 'Cables'],
        'Audio': ['Accessories', 'Smartphones', 'Tablets'],
        'Smartphones': ['Accessories', 'Audio', 'Storage'],
        'Tablets': ['Accessories', 'Audio', 'Storage'],
        'Storage': ['Laptops', 'Smartphones', 'Tablets', 'Accessories'],
        'Cables': ['Laptops', 'Monitors', 'Accessories', 'Smartphones'],
        'Cameras': ['Accessories', 'Storage'],
        'Networking': ['Accessories', 'Cables'],
    }
    
    def __init__(self, search_engine):
        """
        Initialize recommendation engine.
        
        Args:
            search_engine: SearchEngine instance with product catalog
        """
        self.search_engine = search_engine
    
    def extract_keywords(self, text):
        """Extract keywords from product name."""
        # Convert to lowercase and split by common separators
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return [w for w in words if w not in stop_words and len(w) > 2]
    
    def name_similarity(self, name1, name2):
        """Calculate name similarity based on common keywords."""
        keywords1 = set(self.extract_keywords(name1))
        keywords2 = set(self.extract_keywords(name2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def price_tier_similarity(self, price1, price2):
        """Calculate price similarity based on price tiers."""
        # Define price tiers
        def get_price_tier(price):
            if price < 20:
                return 'budget'
            elif price < 50:
                return 'low'
            elif price < 100:
                return 'mid-low'
            elif price < 300:
                return 'mid'
            elif price < 800:
                return 'mid-high'
            elif price < 1500:
                return 'high'
            else:
                return 'premium'
        
        tier1 = get_price_tier(price1)
        tier2 = get_price_tier(price2)
        
        # Same tier = 1.0, adjacent tiers = 0.7, 2 tiers away = 0.4, else 0.1
        tiers = ['budget', 'low', 'mid-low', 'mid', 'mid-high', 'high', 'premium']
        idx1 = tiers.index(tier1)
        idx2 = tiers.index(tier2)
        tier_diff = abs(idx1 - idx2)
        
        if tier_diff == 0:
            return 1.0
        elif tier_diff == 1:
            return 0.7
        elif tier_diff == 2:
            return 0.4
        else:
            return 0.1
    
    def category_relationship_score(self, cat1, cat2):
        """Calculate category relationship score."""
        if cat1 == cat2:
            return 1.0  # Same category - highest score
        
        # Check if categories are complementary
        if cat1 in self.COMPLEMENTARY_CATEGORIES:
            if cat2 in self.COMPLEMENTARY_CATEGORIES[cat1]:
                return 0.6  # Complementary categories
        
        # Check reverse relationship
        if cat2 in self.COMPLEMENTARY_CATEGORIES:
            if cat1 in self.COMPLEMENTARY_CATEGORIES[cat2]:
                return 0.6
        
        # Related categories (both are tech/electronics)
        tech_categories = {'Laptops', 'Monitors', 'Accessories', 'Smartphones', 'Tablets', 
                          'Storage', 'Cables', 'Networking', 'Audio', 'Cameras'}
        if cat1 in tech_categories and cat2 in tech_categories:
            return 0.3  # Both tech but not directly related
        
        return 0.1  # Unrelated categories
    
    def calculate_similarity(self, product1, product2):
        """
        Calculate improved similarity score between two products.
        Uses enhanced weighted combination with keyword matching and category relationships.
        
        Args:
            product1: First product (target)
            product2: Second product (candidate)
            
        Returns:
            Similarity score (0-1, higher is more similar)
        """
        # 1. Category relationship (highest priority - 35%)
        category_score = self.category_relationship_score(product1.category, product2.category)
        
        # 2. Name/Keyword similarity (25%)
        name_sim = self.name_similarity(product1.name, product2.name)
        
        # 3. Price tier similarity (20%)
        price_tier_sim = self.price_tier_similarity(product1.price, product2.price)
        
        # 4. Rating similarity (15%)
        rating_diff = abs(product1.rating - product2.rating)
        rating_similarity = max(0, 1 - (rating_diff / 2.5))  # More sensitive to rating differences
        
        # 5. Popularity similarity (5%) - bonus for popular products
        all_products = self.search_engine.get_all_products()
        if all_products:
            max_pop = max(p.popularity for p in all_products)
            min_pop = min(p.popularity for p in all_products)
            pop_range = max_pop - min_pop if max_pop > min_pop else 1
            
            # Normalize both popularities
            norm_pop1 = (product1.popularity - min_pop) / pop_range
            norm_pop2 = (product2.popularity - min_pop) / pop_range
            
            pop_similarity = 1 - abs(norm_pop1 - norm_pop2)
        else:
            pop_similarity = 0.5
        
        # Weighted combination with improved weights
        similarity = (
            category_score * 0.35 +      # 35% - Category is most important
            name_sim * 0.25 +            # 25% - Name/keyword matching
            price_tier_sim * 0.20 +      # 20% - Price tier matching
            rating_similarity * 0.15 +   # 15% - Rating similarity
            pop_similarity * 0.05        # 5% - Popularity bonus
        )
        
        # Boost score if same category AND similar price
        if category_score == 1.0 and price_tier_sim >= 0.7:
            similarity = min(1.0, similarity * 1.1)
        
        return similarity
    
    def get_recommendations(self, product_id, limit=12):
        """
        Get improved product recommendations based on a given product.
        Uses diversity to ensure recommendations aren't too similar to each other.
        
        Args:
            product_id: ID of the product to get recommendations for
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommended products sorted by similarity with diversity
        """
        target_product = self.search_engine.search_by_id(product_id)
        
        if not target_product:
            return []
        
        all_products = self.search_engine.get_all_products()
        recommendations = []
        
        for product in all_products:
            # Skip the product itself
            if product.product_id == product_id:
                continue
            
            similarity = self.calculate_similarity(target_product, product)
            recommendations.append((product, similarity))
        
        # Sort by similarity (descending)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        # Apply diversity filter to avoid too many similar products
        diverse_recommendations = self._apply_diversity_filter(recommendations, limit)
        
        return diverse_recommendations
    
    def _apply_diversity_filter(self, recommendations, limit):
        """Apply diversity filter to recommendations."""
        if not recommendations:
            return []
        
        selected = []
        used_categories = {}
        used_price_tiers = {}
        
        for product, similarity in recommendations:
            # Get price tier
            price_tier = 'budget' if product.price < 20 else \
                        'low' if product.price < 50 else \
                        'mid-low' if product.price < 100 else \
                        'mid' if product.price < 300 else \
                        'mid-high' if product.price < 800 else \
                        'high' if product.price < 1500 else 'premium'
            
            # Check diversity constraints
            category_count = used_categories.get(product.category, 0)
            tier_count = used_price_tiers.get(price_tier, 0)
            
            # Allow up to 3 products from same category, 2 from same price tier
            if category_count < 3 and tier_count < 2:
                selected.append(product)
                used_categories[product.category] = category_count + 1
                used_price_tiers[price_tier] = tier_count + 1
                
                if len(selected) >= limit:
                    break
            
            # If we haven't filled the limit, be more lenient
            elif len(selected) < limit * 0.7:
                selected.append(product)
                used_categories[product.category] = category_count + 1
                used_price_tiers[price_tier] = tier_count + 1
        
        # If we still don't have enough, fill with remaining top recommendations
        if len(selected) < limit:
            for product, similarity in recommendations:
                if product not in selected:
                    selected.append(product)
                    if len(selected) >= limit:
                        break
        
        return selected
    
    def get_recommendations_by_category(self, category, limit=5):
        """
        Get recommendations based on category.
        
        Args:
            category: Product category
            limit: Maximum number of recommendations
            
        Returns:
            List of products in the same category, sorted by rating
        """
        all_products = self.search_engine.get_all_products()
        category_products = [
            p for p in all_products 
            if p.category.lower() == category.lower()
        ]
        
        # Sort by rating (descending)
        category_products.sort(key=lambda p: p.rating, reverse=True)
        
        return category_products[:limit]
    
    def get_trending_products(self, limit=5):
        """
        Get trending products based on popularity and rating.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of trending products
        """
        all_products = self.search_engine.get_all_products()
        
        # Calculate trending score: (rating * 0.6) + (normalized_popularity * 0.4)
        trending_scores = []
        max_popularity = max(p.popularity for p in all_products) if all_products else 1
        
        for product in all_products:
            normalized_pop = product.popularity / max_popularity
            trending_score = (product.rating * 0.6) + (normalized_pop * 0.4)
            trending_scores.append((product, trending_score))
        
        # Sort by trending score
        trending_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [product for product, score in trending_scores[:limit]]
    
    def get_similar_price_range(self, price, tolerance=0.3, limit=5):
        """
        Get products in similar price range.
        
        Args:
            price: Target price
            tolerance: Price tolerance (0.3 = 30% above/below)
            limit: Maximum number of products
            
        Returns:
            List of products in similar price range
        """
        all_products = self.search_engine.get_all_products()
        min_price = price * (1 - tolerance)
        max_price = price * (1 + tolerance)
        
        similar_products = [
            p for p in all_products
            if min_price <= p.price <= max_price
        ]
        
        # Sort by rating
        similar_products.sort(key=lambda p: p.rating, reverse=True)
        
        return similar_products[:limit]

