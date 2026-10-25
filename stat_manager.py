from mongodb_connect import get_db, get_borrow_collection

def category_stats():
    db = get_db()
    pipeline = [
        {"$group": {
            "_id": "$category",
            "total_stock": {"$sum": "$stock"},
            "avg_price": {"$avg": "$price"},
            "book_count": {"$sum": 1}
        }},
        {"$sort": {"total_stock": -1}}
    ]
    results = list(db.books.aggregate(pipeline))
    print("\n--- 分类统计 (按库存排序) ---")
    for r in results:
        print(f"类别: {r['_id']} | 库存总量: {r['total_stock']} | 均价: ￥{round(r['avg_price'], 2)} | 种类: {r['book_count']}")

def borrow_trend():
    col = get_borrow_collection()
    pipeline = [
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y年", "date": "$borrow_date"}},
            "borrow_count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    results = list(col.aggregate(pipeline))
    print("\n--- 借阅趋势分析 ---")
    for r in results:
        print(f"{r['_id']}: {r['borrow_count']} 次")

def bestsellers():
    db = get_db()
    results = list(db.books.find().sort("borrow_count", -1).limit(5))
    print("\n--- 畅销图书排行 ---")
    for b in results:
        print(f"{b.get('title')} - 累计借阅 {b.get('borrow_count')} 次")