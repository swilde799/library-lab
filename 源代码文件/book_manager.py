from datetime import datetime
from db_config import DBConfig

db = DBConfig.get_db()

def search_by_category_price(category, min_p, max_p):
    return db.books.count_documents({"category": category, "price": {"$gte": min_p, "$lte": max_p}})

def search_by_tags(tags_list):
    return db.books.count_documents({"tags": {"$all": tags_list}})

def search_by_title(kw):
    return list(db.books.find({"title": {"$regex": kw, "$options": "i"}}, {"title": 1, "_id": 0}))

def search_by_year(start_y, end_y):
    return db.books.count_documents({"publish_date": {"$gte": datetime(start_y,1,1), "$lt": datetime(end_y,1,1)}})

def missing_tags():
    return db.books.count_documents({"tags": {"$exists": False}})

def get_top_ratings(n=10):
    return list(db.books.find({}, {"title": 1, "rating": 1, "_id": 0}).sort("rating", -1).limit(n))

def add_book(book_dict):
    db.books.insert_one(book_dict)
    DBConfig.log_action("insert", "books", book_dict.get("title"))
