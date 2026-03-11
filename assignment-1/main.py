from fastapi import FastAPI

app = FastAPI(
    title="Intern Store API",
    description="Day 1 FastAPI Assignment",
    version="1.0"
)

# Product Data
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Bluetooth Speaker", "price": 1499, "category": "Electronics", "in_stock": False},

    # Newly Added Products (Q1)
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]


@app.get("/")
def welcome():
    return {"status": "Store API is running successfully 🚀"}


# Q1 – Show all products
@app.get("/products")
def list_products():
    return {
        "items": products,
        "total_products": len(products)
    }


# Q2 – Filter products by category
@app.get("/products/category/{category_name}")
def filter_by_category(category_name: str):
    filtered_items = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_items.append(product)

    if len(filtered_items) == 0:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_items,
        "count": len(filtered_items)
    }


# Q3 – Show only available products
@app.get("/products/instock")
def available_products():
    available_list = [item for item in products if item["in_stock"]]

    return {
        "available_products": available_list,
        "available_count": len(available_list)
    }


# Q4 – Store Summary
@app.get("/store/summary")
def store_overview():
    total_count = len(products)
    in_stock_count = sum(1 for item in products if item["in_stock"])
    out_of_stock_count = total_count - in_stock_count

    category_set = set()
    for item in products:
        category_set.add(item["category"])

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_count,
        "in_stock_products": in_stock_count,
        "out_of_stock_products": out_of_stock_count,
        "available_categories": list(category_set)
    }


# Q5 – Search products by keyword
@app.get("/products/search/{keyword}")
def search_items(keyword: str):
    matched_products = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "search_keyword": keyword,
        "matched_products": matched_products,
        "total_found": len(matched_products)
    }


# BONUS – Cheapest and Most Expensive
@app.get("/products/deals")
def best_and_premium():
    lowest_price_product = min(products, key=lambda x: x["price"])
    highest_price_product = max(products, key=lambda x: x["price"])

    return {
        "best_deal": lowest_price_product,
        "premium_pick": highest_price_product
    }







# Task 2 FastAPI 
from pydantic import BaseModel

# Q1 - Filter products by minimum price
@app.get("/products/filter")
def filter_products(min_price: int = None):
    result = products

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return {"products": result}


# Q2 - Get product price using product ID
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return {
                "name": p["name"],
                "price": p["price"]
            }

    return {"message": "Product not found"}


# Q3 - Customer feedback model
class CustomerFeedback(BaseModel):
    customer_name: str
    product_id: int
    rating: int
    comment: str


@app.post("/feedback")
def submit_feedback(feedback: CustomerFeedback):
    return {
        "message": "Feedback received successfully",
        "data": feedback
    }


# Q4 - Product summary
@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    most_expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive_product": most_expensive,
        "cheapest_product": cheapest,
        "categories": categories
    }


# Q5 - Bulk order models
class OrderItem(BaseModel):
    product_id: int
    quantity: int


class BulkOrder(BaseModel):
    items: list[OrderItem]


@app.post("/orders/bulk")
def create_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:
        for p in products:

            if p["id"] == item.product_id:

                if p["in_stock"]:

                    total = p["price"] * item.quantity
                    grand_total += total

                    confirmed.append({
                        "product_name": p["name"],
                        "quantity": item.quantity,
                        "total_price": total
                    })

                else:
                    failed.append(p["name"])

    return {
        "confirmed_orders": confirmed,
        "failed_orders": failed,
        "grand_total": grand_total
    }