# Recipe Tools

Recipe Tools is a comprehensive MCP food assistant that provides recipe queries, category browsing, intelligent recommendations, search functions, and more, helping users solve the "what to eat today" problem.

### Common Usage Scenarios

**Recipe Queries:**
- "I want to learn how to make Kung Pao Chicken"
- "How to make Braised Pork Belly"
- "Recipe for Scrambled Eggs with Tomatoes"
- "Look up the recipe for Mapo Tofu"

**Category Browsing:**
- "What Sichuan dishes do you recommend"
- "Show me some home-style dishes"
- "What vegetarian recipes are available"
- "Recommend some soup recipes"

**Intelligent Recommendations:**
- "What should I eat today"
- "Recommend some dishes suitable for 2 people for dinner"
- "Recommend some breakfast dishes for me"
- "Recipes for a 4-person gathering"

**Search Functions:**
- "Are there any dishes made with potatoes"
- "Search for recipes containing chicken"
- "Find some simple and easy-to-make dishes"
- "What spicy dishes do you recommend"

**Random Recommendations:**
- "Randomly recommend a dish"
- "Don't know what to make, recommend a few randomly"
- "Give me a surprise recipe"

### Usage Tips

1. **Clear Requirements**: You can specify preferences for cuisine, ingredients, difficulty, etc.
2. **Consider Number of People**: You can indicate the number of diners for more accurate recommendations
3. **Meal Time**: You can specify breakfast, lunch, dinner, etc.
4. **Ingredient Preferences**: You can mention liked or disliked ingredients
5. **Difficulty Selection**: You can request simple and easy recipes or challenging ones

The AI assistant will automatically call the recipe tools based on your needs and provide detailed cooking guidance.

## Feature Overview

### Recipe Query Function
- **Detailed Recipes**: Provide complete preparation steps and ingredient lists
- **Category Browsing**: View by cuisine, type, difficulty, etc.
- **Smart Search**: Supports fuzzy search and keyword matching
- **Recipe Details**: Includes preparation time, difficulty, nutritional information, etc.

### Intelligent Recommendation Function
- **Personalized Recommendations**: Recommend based on number of diners and time
- **Random Recommendations**: Solve choice paralysis with random dish recommendations
- **Scenario Recommendations**: Recipe recommendations for different dining scenarios
- **Nutritional Pairing**: Consider nutritionally balanced dish combinations

### Category Management Function
- **Cuisine Classification**: Sichuan, Cantonese, Hunan, and other regional cuisines
- **Type Classification**: Home-style, vegetarian, soups, etc.
- **Difficulty Classification**: Simple, medium, difficult, etc.
- **Time Classification**: Breakfast, lunch, dinner, late-night snacks, etc.

### Search Function
- **Ingredient Search**: Find related recipes based on ingredients
- **Keyword Search**: Supports dish names, features, and other keywords
- **Fuzzy Search**: Intelligent matching of similar recipes
- **Combination Search**: Multi-criteria combined search

## Tool List

### 1. Recipe Query Tools

#### get_all_recipes - Get All Recipes
Get recipe list with pagination support.

**Parameters:**
- `page` (optional): Page number, default 1
- `page_size` (optional): Items per page, default 10, maximum 50

**Usage Scenarios:**
- Browse recipe list
- Understand recipe overview
- View recipes by page

#### get_recipe_by_id - Get Recipe Details
Get detailed information based on recipe ID or name.

**Parameters:**
- `query` (required): Recipe name or ID

**Usage Scenarios:**
- View specific recipe details
- Get preparation steps
- Query ingredient list

### 2. Category Browsing Tools

#### get_recipes_by_category - Get Recipes by Category
Get recipe list based on category.

**Parameters:**
- `category` (required): Category name
- `page` (optional): Page number, default 1
- `page_size` (optional): Items per page, default 10, maximum 50

**Usage Scenarios:**
- Browse specific cuisine
- View categorized recipes
- Filter by type

### 3. Intelligent Recommendation Tools

#### recommend_meals - Recommend Dishes
Recommend suitable dishes based on number of diners and time.

**Parameters:**
- `people_count` (optional): Number of diners, default 2
- `meal_type` (optional): Meal type, default "dinner"
- `page` (optional): Page number, default 1
- `page_size` (optional): Items per page, default 10, maximum 50

**Usage Scenarios:**
- Recommend dishes based on number of people
- Recommend by meal time
- Personalized recipe recommendations

#### what_to_eat - Randomly Recommend Dishes
Randomly recommend dishes to solve choice paralysis.

**Parameters:**
- `meal_type` (optional): Meal type, default "any"
- `page` (optional): Page number, default 1
- `page_size` (optional): Items per page, default 10, maximum 50

**Usage Scenarios:**
- Random dish recommendations
- Solve choice paralysis
- Try new recipes

### 4. Search Tools

#### search_recipes_fuzzy - Fuzzy Search Recipes
Fuzzy search recipes based on keywords.

**Parameters:**
- `query` (required): Search keyword
- `page` (optional): Page number, default 1
- `page_size` (optional): Items per page, default 10, maximum 50

**Usage Scenarios:**
- Keyword search
- Ingredient search
- Fuzzy matching search

## Usage Examples

### Recipe Query Examples

```python
# Get recipe list
result = await mcp_server.call_tool("get_all_recipes", {
    "page": 1,
    "page_size": 10
})

# Get specific recipe details
result = await mcp_server.call_tool("get_recipe_by_id", {
    "query": "Kung Pao Chicken"
})

# Get recipes by category
result = await mcp_server.call_tool("get_recipes_by_category", {
    "category": "Sichuan Cuisine",
    "page": 1,
    "page_size": 10
})
```

### Intelligent Recommendation Examples

```python
# Recommend based on number of people and time
result = await mcp_server.call_tool("recommend_meals", {
    "people_count": 4,
    "meal_type": "dinner",
    "page": 1,
    "page_size": 5
})

# Randomly recommend dishes
result = await mcp_server.call_tool("what_to_eat", {
    "meal_type": "lunch",
    "page": 1,
    "page_size": 3
})
```

### Search Function Examples

```python
# Fuzzy search recipes
result = await mcp_server.call_tool("search_recipes_fuzzy", {
    "query": "potato",
    "page": 1,
    "page_size": 10
})

# Search specific cuisine
result = await mcp_server.call_tool("search_recipes_fuzzy", {
    "query": "home-style dishes",
    "page": 1,
    "page_size": 15
})
```

## Data Structure

### Recipe Information (Recipe)
```python
{
    "id": "recipe_123",
    "name": "Kung Pao Chicken",
    "category": "Sichuan Cuisine",
    "difficulty": "Medium",
    "cooking_time": "30 minutes",
    "serving": "2-3 people",
    "ingredients": [
        {
            "name": "Chicken breast",
            "amount": "300g",
            "note": "Diced"
        },
        {
            "name": "Peanuts",
            "amount": "50g",
            "note": "Fried"
        }
    ],
    "steps": [
        {
            "step": 1,
            "description": "Dice chicken breast, marinate with cooking wine, soy sauce, starch for 15 minutes"
        },
        {
            "step": 2,
            "description": "Heat oil in pan, stir-fry chicken until color changes, then remove"
        }
    ],
    "tips": "Control heat well during stir-frying to avoid overcooking",
    "nutrition": {
        "calories": "280kcal",
        "protein": "25g",
        "fat": "12g",
        "carbs": "15g"
    }
}
```

### Pagination Result (PagedResult)
```python
{
    "data": [
        {
            "id": "recipe_123",
            "name": "Kung Pao Chicken",
            "category": "Sichuan Cuisine",
            "difficulty": "Medium",
            "cooking_time": "30 minutes"
        }
    ],
    "pagination": {
        "page": 1,
        "page_size": 10,
        "total": 156,
        "total_pages": 16,
        "has_next": true,
        "has_prev": false
    }
}
```

### Recommendation Information (RecommendationInfo)
```python
{
    "recommendation_info": {
        "people_count": 4,
        "meal_type": "dinner",
        "message": "Recommended dishes for 4 people for dinner"
    }
}
```

## Supported Categories

### Cuisine Classification
- **Sichuan Cuisine**: Spicy and flavorful Sichuan dishes
- **Cantonese Cuisine**: Light and fresh Guangdong dishes
- **Hunan Cuisine**: Fragrant and spicy Hunan dishes
- **Shandong Cuisine**: Salty and fresh Shandong dishes
- **Jiangsu Cuisine**: Light and sweet Jiangsu dishes
- **Zhejiang Cuisine**: Fresh and crisp Zhejiang dishes
- **Fujian Cuisine**: Light and sweet Fujian dishes
- **Anhui Cuisine**: Fragrant and tasty Anhui dishes

### Type Classification
- **Home-style Dishes**: Daily family cooking
- **Vegetarian**: Vegetarian recipes
- **Soups**: Various soup dishes
- **Cold Dishes**: Appetizers and cold dishes
- **Noodles**: Noodles, dumplings, etc.
- **Desserts**: Sweets and pastries
- **Appetizers**: Dishes suitable with drinks

### Difficulty Classification
- **Simple**: Beginner-friendly, simple steps
- **Medium**: Requires some cooking skills
- **Difficult**: Requires extensive cooking experience

### Time Classification
- **Breakfast**: Breakfast recipes
- **Lunch**: Lunch recipes
- **Dinner**: Dinner recipes
- **Late-night Snacks**: Late-night snacks
- **Afternoon Tea**: Tea snacks

## Best Practices

### 1. Recipe Queries
- Use accurate dish names for best results
- Discover new recipes through category browsing
- Pay attention to recipe difficulty and time requirements

### 2. Intelligent Recommendations
- Accurately provide number of diners for appropriate portions
- Choose suitable dishes based on meal time
- Consider nutritional balance

### 3. Search Techniques
- Use ingredient names to search related recipes
- Try different keyword combinations
- Use fuzzy search to discover unexpected surprises

### 4. Pagination Usage
- Set appropriate items per page
- Browse page by page to avoid information overload
- Pay attention to total pages and current page position

## Precautions

1. **Fresh Ingredients**: Ensure using fresh ingredients
2. **Allergy Alerts**: Pay attention to food allergy issues
3. **Nutritional Balance**: Consider nutritional balance
4. **Cooking Safety**: Pay attention to kitchen safety operations
5. **Portion Adjustment**: Adjust quantities based on actual number of people

## Troubleshooting

### Common Issues
1. **No Search Results**: Try different keywords or category browsing
2. **Recipe Not Detailed**: Check recipe details page
3. **Recommendations Not Suitable**: Adjust recommendation parameters
4. **Pagination Error**: Check page number and page size

### Debugging Methods
1. Verify search keyword spelling
2. Check if category name is correct
3. Confirm page number parameter range
4. Check returned error messages

With Recipe Tools, you can easily solve the "what to eat today" problem, discover new cuisines, learn cooking skills, and enjoy the happiness that food brings.
