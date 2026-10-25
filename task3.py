from mongodb_connect import get_db, get_borrow_collection


def main():
    db = get_db()
    books = db["books"]
    readers = db["readers"]
    borrow_logs = get_borrow_collection()  # 自动识别并选用 borrow_logs_plain 普通集合

    # 基础参数：从你的数据中提取的真实值
    TEST_ISBN = "9787115428028"  # Python编程：从入门到实践
    TEST_CARD = "R20240001"  # 张明

    print("=" * 60)
    print("任务三：基础检索 (Q1-Q6)")
    print("=" * 60)

    res = list(books.find({"price": {"$gt": 80}}))
    print(f"Q1 定价>80: db.books.find({{'price': {{'$gt': 80}}}}) -> 条数: {len(res)}")

    res = list(books.find({"stock": {"$lt": 10}}))
    print(f"Q2 库存<10: db.books.find({{'stock': {{'$lt': 10}}}}) -> 条数: {len(res)}")

    res = list(books.find({"isbn": {"$eq": TEST_ISBN}}))
    print(f"Q3 按ISBN精确查找: db.books.find({{'isbn': {{'$eq': '{TEST_ISBN}'}}}}) -> 条数: {len(res)}")

    res = list(readers.find({"email": None}))
    print(f"Q4 邮箱为空: db.readers.find({{'email': None}}) -> 条数: {len(res)}")

    res = list(books.find({"publisher": {"$ne": "人民邮电出版社"}}))
    print(f"Q5 排除人民邮电出版社: db.books.find({{'publisher': {{'$ne': '人民邮电出版社'}}}}) -> 条数: {len(res)}")

    res = list(books.find({"category": {"$in": ["计算机", "经济管理"]}}))
    print(
        f"Q6 类别为计算机或经管: db.books.find({{'category': {{'$in': ['计算机', '经济管理']}}}}) -> 条数: {len(res)}")

    print("\n" + "=" * 60)
    print("任务三：组合与高级检索 (Q7-Q12)")
    print("=" * 60)

    res = list(books.find({"$and": [{"rating": {"$gt": 4.0}}, {"category": "计算机"}]}))
    print(
        f"Q7 评分>4.0且计算机类: db.books.find({{'$and': [{{'rating': {{'$gt': 4.0}}}}, {{'category': '计算机'}}]}}) -> 条数: {len(res)}")

    res = list(books.find({"$or": [{"rating": {"$lt": 3.5}}, {"stock": 0}]}))
    print(
        f"Q8 评分<3.5或库存为0: db.books.find({{'$or': [{{'rating': {{'$lt': 3.5}}}}, {{'stock': 0}}]}}) -> 条数: {len(res)}")

    res = list(books.find({"title": {"$regex": "Python"}}))
    print(f"Q9 书名包含Python: db.books.find({{'title': {{'$regex': 'Python'}}}}) -> 条数: {len(res)}")

    res = list(books.find({"tags": {"$all": ["编程", "入门"]}}))
    print(f"Q10 标签同时有编程和入门: db.books.find({{'tags': {{'$all': ['编程', '入门']}}}}) -> 条数: {len(res)}")

    res = list(books.find({"tags": {"$size": 3}}))
    print(f"Q11 标签恰好3个: db.books.find({{'tags': {{'$size': 3}}}}) -> 条数: {len(res)}")

    res = list(books.find({"tags": {"$exists": True}}))
    print(f"Q12 包含tags字段: db.books.find({{'tags': {{'$exists': True}}}}) -> 条数: {len(res)}")

    print("\n" + "=" * 60)
    print("任务三：结果处理 (Q13-Q16)")
    print("=" * 60)

    res = list(books.find({"_id": {"$type": "string"}}))
    print(f"Q13 _id为字符串类型: db.books.find({{'_id': {{'$type': 'string'}}}}) -> 条数: {len(res)}")

    res = list(books.find().sort("rating", -1).limit(5))
    print(f"Q14 评分降序取前5: db.books.find().sort({{'rating': -1}}).limit(5) -> 条数: {len(res)}")

    res = list(books.find({}, {"_id": 0, "title": 1, "price": 1, "rating": 1}).limit(1))
    print(
        f"Q15 投影查询(去_id): db.books.find({{}}, {{'_id': 0, 'title': 1, 'price': 1, 'rating': 1}}) -> (仅展示1条样例)")
    if res: print("  样例数据:", res[0])

    res = books.distinct("category")
    print(f"Q16 获取所有类别清单: db.books.distinct('category') -> 结果: {res}")

    print("\n" + "=" * 60)
    print("任务三：更新与删除 (U1-U4, D1-D3)")
    print("=" * 60)

    r = books.update_one({"isbn": TEST_ISBN}, {"$inc": {"stock": -5}})
    print(
        f"U1 库存减5: db.books.updateOne({{'isbn': '{TEST_ISBN}'}}, {{'$inc': {{'stock': -5}}}}) -> 匹配:{r.matched_count}, 修改:{r.modified_count}")

    r = books.update_many({"category": "计算机"}, {"$mul": {"price": 0.9}})
    print(
        f"U2 计算机类打9折: db.books.updateMany({{'category': '计算机'}}, {{'$mul': {{'price': 0.9}}}}) -> 匹配:{r.matched_count}, 修改:{r.modified_count}")

    r = books.update_one({"isbn": TEST_ISBN}, {"$currentDate": {"last_updated": True}})
    print(
        f"U3 新增当前时间字段: db.books.updateOne({{'isbn': '{TEST_ISBN}'}}, {{'$currentDate': {{'last_updated': true}}}}) -> 匹配:{r.matched_count}, 修改:{r.modified_count}")

    r = books.update_one({"isbn": TEST_ISBN}, {"$unset": {"tags": ""}})
    print(
        f"U4 删除tags字段: db.books.updateOne({{'isbn': '{TEST_ISBN}'}}, {{'$unset': {{'tags': ''}}}}) -> 匹配:{r.matched_count}, 修改:{r.modified_count}")

    r = borrow_logs.delete_one({"status": "已归还"})
    print(f"D1 删除一条已归还记录: db.borrow_logs_plain.deleteOne({{'status': '已归还'}}) -> 删除:{r.deleted_count}")

    preview_count = borrow_logs.count_documents({"status": "逾期"})
    print(f"D2 逾期记录预览条数: {preview_count} 条")
    r = borrow_logs.delete_many({"status": "逾期"})
    print(f"D2 清理逾期记录: db.borrow_logs_plain.deleteMany({{'status': '逾期'}}) -> 删除:{r.deleted_count}")

    # D3 替换张明的信息
    new_reader = {
        "card_no": TEST_CARD,
        "name": "张明(已替换)",
        "college": "软件学院",
        "email": "zhangming_new@test.com",
        "phone": "13800000000",
        "level": "教师",
        "register_date": None,
        "fav_categories": ["计算机"]
    }
    r = readers.replace_one({"card_no": TEST_CARD}, new_reader)
    print(
        f"D3 整体替换读者信息: db.readers.replaceOne({{'card_no': '{TEST_CARD}'}}, ...) -> 匹配:{r.matched_count}, 修改:{r.modified_count}")

    print("\n" + "=" * 60)
    print("注意：你的数据库数据已被修改。如果想恢复初始状态，重新运行 python setup_library.py 即可。")
    print("=" * 60)


if __name__ == "__main__":
    main()