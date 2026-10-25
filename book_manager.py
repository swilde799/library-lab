from mongodb_connect import get_db
from datetime import datetime

def add_book():
    db = get_db()
    title = input("书名: ")
    isbn = input("ISBN: ")
    price = float(input("价格: "))
    stock = int(input("库存: "))
    doc = {"isbn": isbn, "title": title, "price": price, "stock": stock, "category": "其他", "rating": 5.0, "borrow_count": 0}
    res = db.books.insert_one(doc)
    print(f"添加成功，文档ID: {res.inserted_id}")

def search_books():
    db = get_db()
    keyword = input("输入书名关键词: ")
    results = list(db.books.find({"title": {"$regex": keyword}}).limit(5))
    if not results:
        print("未找到相关图书。")
        return
    for b in results:
        print(f"[{b.get('isbn')}] {b.get('title')} - ￥{b.get('price')} (库存:{b.get('stock')})")

def top_rated_books():
    db = get_db()
    results = list(db.books.find().sort("rating", -1).limit(5))
    print("\n--- 评分排行前5 ---")
    for b in results:
        print(f"评分: {b.get('rating')} | {b.get('title')}")