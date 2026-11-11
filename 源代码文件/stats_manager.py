from db_config import DBConfig
db = DBConfig.get_db()

def stats_by_category():
    return list(db.books.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}, "avg_price": {"$avg": "$price"}}}
    ]))

def stats_college_top5():
    return list(db.borrow_logs.aggregate([
        {"$lookup": {"from": "readers", "localField": "reader_card", "foreignField": "card_no", "as": "r"}},
        {"$unwind": "$r"}, {"$group": {"_id": "$r.college", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}, {"$limit": 5}
    ]))

def stats_borrow_trend():
    return list(db.borrow_logs.aggregate([
        {"$group": {"_id": {"y": {"$year": "$borrow_date"}, "m": {"$month": "$borrow_date"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id.y": 1, "_id.m": 1}}
    ]))

def stats_top10_borrowed():
    return list(db.books.find({}, {"title": 1, "borrow_count": 1, "location.shelf": 1, "_id": 0}).sort("borrow_count", -1).limit(10))

def export_category_stats():
    db.books.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$out": "category_stats"}
    ])
    DBConfig.log_action("export", "category_stats")
