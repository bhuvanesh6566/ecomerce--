// E-Commerce Product Search and Recommendation System - Frontend

const API_BASE = 'http://localhost:5000/api';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const clearBtn = document.getElementById('clearBtn');
const sortBy = document.getElementById('sortBy');
const sortOrder = document.getElementById('sortOrder');
const algorithm = document.getElementById('algorithm');
const applySortBtn = document.getElementById('applySortBtn');
const productsGrid = document.getElementById('productsGrid');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const totalProducts = document.getElementById('totalProducts');
const resultCount = document.getElementById('resultCount');
const trendingProducts = document.getElementById('trendingProducts');
const productsSectionTitle = document.getElementById('productsSectionTitle');
const productDetailsModal = document.getElementById('productDetailsModal');
const productDetailsContent = document.getElementById('productDetailsContent');
const productDetailsRecommendationsGrid = document.getElementById('productDetailsRecommendationsGrid');

let currentProducts = [];
let isSearchMode = false;
let selectedProductId = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadAllProducts();
    loadStats();
    loadTrendingProducts();
    
    // Event listeners
    searchBtn.addEventListener('click', handleSearch);
    clearBtn.addEventListener('click', handleClear);
    applySortBtn.addEventListener('click', handleSort);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
});

// Load all products
async function loadAllProducts() {
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE}/products?sort_by=id&order=asc`);
        const data = await response.json();
        
        if (data.success) {
            currentProducts = data.products;
            displayProducts(currentProducts);
            updateResultCount(currentProducts.length);
            isSearchMode = false;
            if (productsSectionTitle) {
                productsSectionTitle.textContent = 'All Products';
            }
        } else {
            showError('Failed to load products');
        }
    } catch (err) {
        showError(`Error: ${err.message}`);
    } finally {
        hideLoading();
    }
}

// Search products
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        loadAllProducts();
        return;
    }
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE}/products/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success) {
            currentProducts = data.products;
            displayProducts(currentProducts);
            updateResultCount(currentProducts.length);
            isSearchMode = true;
            if (productsSectionTitle) {
                productsSectionTitle.textContent = `Search Results (${currentProducts.length})`;
            }
        } else {
            showError(data.error || 'Search failed');
            currentProducts = [];
            displayProducts([]);
            if (productsSectionTitle) {
                productsSectionTitle.textContent = 'Search Results';
            }
        }
    } catch (err) {
        showError(`Error: ${err.message}`);
        currentProducts = [];
        displayProducts([]);
    } finally {
        hideLoading();
    }
}

// Clear search
function handleClear() {
    searchInput.value = '';
    loadAllProducts();
}

// Sort products
async function handleSort() {
    if (currentProducts.length === 0) {
        return;
    }
    
    showLoading();
    hideError();
    
    const sortByValue = sortBy.value;
    const orderValue = sortOrder.value;
    const algorithmValue = algorithm.value;
    
    try {
        let url = `${API_BASE}/products?sort_by=${sortByValue}&order=${orderValue}&algorithm=${algorithmValue}`;
        
        // If in search mode, we need to sort the current results
        if (isSearchMode) {
            // Sort locally for search results
            const sorted = sortProductsLocally(currentProducts, sortByValue, orderValue);
            displayProducts(sorted);
            hideLoading();
            return;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            currentProducts = data.products;
            displayProducts(currentProducts);
        } else {
            showError('Failed to sort products');
        }
    } catch (err) {
        showError(`Error: ${err.message}`);
    } finally {
        hideLoading();
    }
}

// Sort products locally (for search results)
function sortProductsLocally(products, sortBy, order) {
    const sorted = [...products];
    const reverse = order === 'desc';
    
    sorted.sort((a, b) => {
        let aVal, bVal;
        
        switch (sortBy) {
            case 'price':
                aVal = a.price;
                bVal = b.price;
                break;
            case 'rating':
                aVal = a.rating;
                bVal = b.rating;
                break;
            case 'popularity':
                aVal = a.popularity;
                bVal = b.popularity;
                break;
            case 'name':
                aVal = a.name.toLowerCase();
                bVal = b.name.toLowerCase();
                break;
            case 'id':
                aVal = a.product_id;
                bVal = b.product_id;
                break;
            default:
                return 0;
        }
        
        if (typeof aVal === 'string') {
            return reverse ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
        } else {
            return reverse ? bVal - aVal : aVal - bVal;
        }
    });
    
    return sorted;
}

// Display products
function displayProducts(products, container = productsGrid) {
    if (products.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h2>No products found</h2>
                <p>Try adjusting your search or filters</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card" onclick="handleProductClick(${product.product_id})">
            <div class="product-image-container">
                <img src="${escapeHtml(product.image_url)}" alt="${escapeHtml(product.name)}" class="product-image" 
                     onerror="this.src='https://via.placeholder.com/300x300?text=No+Image'">
            </div>
            <div class="product-info">
                <div class="product-id">ID: ${product.product_id}</div>
                <div class="product-category">${escapeHtml(product.category || 'General')}</div>
                <div class="product-name">${escapeHtml(product.name)}</div>
                <div class="product-details">
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <div class="product-rating">
                        <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                        <span>${product.rating.toFixed(1)}</span>
                    </div>
                    <div class="product-popularity">Popularity: ${product.popularity}</div>
                </div>
            </div>
        </div>
    `).join('');
}

// Handle product click - show product details modal (global function for onclick)
window.handleProductClick = async function(productId) {
    selectedProductId = productId;
    await showProductDetails(productId);
};

// Show product details in modal
async function showProductDetails(productId) {
    try {
        // Fetch product details
        const productResponse = await fetch(`${API_BASE}/products/${productId}`);
        const productData = await productResponse.json();
        
        if (!productData.success) {
            showError('Product not found');
            return;
        }
        
        const product = productData.product;
        
        // Display product details
        if (!productDetailsContent) {
            console.error('productDetailsContent element not found');
            return;
        }
        
        productDetailsContent.innerHTML = `
            <div class="product-details-container">
                <div class="product-details-header">
                    <div>
                        <img src="${escapeHtml(product.image_url)}" alt="${escapeHtml(product.name)}" 
                             class="product-details-image"
                             onerror="this.src='https://via.placeholder.com/500x500?text=No+Image'">
                    </div>
                    <div class="product-details-info">
                        <div class="product-details-category">${escapeHtml(product.category || 'General')}</div>
                        <h1>${escapeHtml(product.name)}</h1>
                        <div class="product-details-price">$${product.price.toFixed(2)}</div>
                        <div class="product-details-rating">
                            <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                            <span>${product.rating.toFixed(1)} / 5.0</span>
                        </div>
                        <div class="product-details-popularity">
                            <strong>Popularity Score:</strong> ${product.popularity}
                        </div>
                        <div class="product-details-id">Product ID: ${product.product_id}</div>
                    </div>
                </div>
            </div>
        `;
        
        // Load recommendations
        if (productDetailsRecommendationsGrid) {
            productDetailsRecommendationsGrid.innerHTML = '<div class="loading">Loading recommendations...</div>';
            
            const recommendationsResponse = await fetch(`${API_BASE}/products/${productId}/recommendations?limit=12`);
            const recommendationsData = await recommendationsResponse.json();
            
            if (recommendationsData.success && recommendationsData.recommendations.length > 0) {
                displayProducts(recommendationsData.recommendations, productDetailsRecommendationsGrid);
            } else {
                productDetailsRecommendationsGrid.innerHTML = '<div class="empty-state"><p>No recommendations available for this product</p></div>';
            }
        }
        
        // Show modal
        if (productDetailsModal) {
            productDetailsModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        }
        
    } catch (err) {
        console.error('Failed to load product details:', err);
        showError(`Error: ${err.message}`);
    }
}

// Close product details modal
window.closeProductDetails = function() {
    if (productDetailsModal) {
        productDetailsModal.classList.add('hidden');
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
};

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target === productDetailsModal) {
        closeProductDetails();
    }
};

// Load trending products
async function loadTrendingProducts() {
    if (!trendingProducts) {
        console.error('trendingProducts element not found');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/recommendations/trending?limit=5`);
        const data = await response.json();
        
        if (data.success && data.products.length > 0) {
            displayProducts(data.products, trendingProducts);
        } else {
            trendingProducts.innerHTML = '<p>No trending products available</p>';
        }
    } catch (err) {
        console.error('Failed to load trending products:', err);
        trendingProducts.innerHTML = '<p>Failed to load trending products</p>';
    }
}

// Load product recommendations (for old section, kept for compatibility)
async function loadProductRecommendations(productId) {
    // This function is kept for compatibility but not used anymore
    // Recommendations are now shown in the modal
    console.log('loadProductRecommendations called for product:', productId);
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        if (data.success) {
            totalProducts.textContent = data.total_products;
        }
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

// Update result count
function updateResultCount(count) {
    resultCount.textContent = count;
}

// Utility functions
function showLoading() {
    if (loading) {
        loading.classList.remove('hidden');
    }
}

function hideLoading() {
    if (loading) {
        loading.classList.add('hidden');
    }
}

function showError(message) {
    if (error) {
        error.textContent = message;
        error.classList.remove('hidden');
    }
}

function hideError() {
    if (error) {
        error.classList.add('hidden');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


