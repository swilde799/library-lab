from mongodb_connect import get_db, get_borrow_collection
from datetime import datetime

def borrow_book():
    db = get_db()
    col = get_borrow_collection()
    card = input("借阅证号: ")
    isbn = input("图书ISBN: ")
    doc = {
        "borrow_date": datetime.now(),
        "reader_card": card,
        "book_isbn": isbn,
        "status": "借出"
    }
    res = col.insert_one(doc)
    print(f"借阅登记成功，影响记录数: 1 (ID: {res.inserted_id})")

def return_book():
    col = get_borrow_collection()
    card = input("借阅证号: ")
    isbn = input("图书ISBN: ")
    res = col.update_many(
        {"reader_card": card, "book_isbn": isbn, "status": "借出"},
        {"$set": {"status": "已归还", "return_date": datetime.now()}}
    )
    print(f"归还处理完成，受影响的文档数: {res.modified_count}")

def check_overdue():
    col = get_borrow_collection()
    results = list(col.find({"status": "逾期"}).limit(10))
    if not results:
        print("当前没有逾期记录。")
        return
    print(f"\n--- 逾期记录 (前{len(results)}条) ---")
    for r in results:
        print(f"读者: {r.get('reader_card')}, ISBN: {r.get('book_isbn')}")