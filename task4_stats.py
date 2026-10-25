from mongodb_connect import get_db

def main():
    db = get_db()
    books = db["books"]
    borrow = db["borrow_logs_plain"] # 用普通集合操作最稳

    print("="*60)
    print("任务四：聚合管道统计 (A1-A9)")
    print("="*60)

    # A1 按类别统计数量与平均评分
    res1 = list(books.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}, "avg_rating": {"$avg": "$rating"}}}
    ]))
    print("A1 分类统计结果:", res1)

    # A2 统计出版社数量取前5
    res2 = list(books.aggregate([
        {"$group": {"_id": "$publisher", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]))
    print("A2 出版社前5:", res2)

    # A3 文档数最多的类别
    res3 = list(books.aggregate([{"$sortByCount": "$category"}]))
    print("A3 类别排行:", res3[:1]) # 只看第一名

    # A4 评分最高前3本
    res4 = list(books.aggregate([
        {"$sort": {"rating": -1}},
        {"$limit": 3},
        {"$project": {"_id": 0, "title": 1, "borrow_count": 1}}
    ]))
    print("A4 评分最高前3:", res4)

    # A5 计算销售额
    res5 = list(books.aggregate([
        {"$project": {"title": 1, "sales": {"$round": [{"$multiply": ["$price", "$borrow_count"]}, 2]}}}
    ]))
    print("A5 图书销售额(前2):", res5[:2])

    # A6 按年份统计借阅量
    res6 = list(borrow.aggregate([
        {"$group": {"_id": {"$dateToString": {"format": "%Y年", "date": "$borrow_date"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))
    print("A6 借阅趋势:", res6)

    # A7 借阅最多的前5名读者
    res7 = list(borrow.aggregate([
        {"$group": {"_id": "$reader_card", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]))
    print("A7 活跃读者前5:", res7)

    # A8 关联读者与借阅，产出学院排行榜
    res8 = list(borrow.aggregate([
        {"$lookup": {"from": "readers", "localField": "reader_card", "foreignField": "card_no", "as": "reader_info"}},
        {"$unwind": "$reader_info"},
        {"$group": {"_id": "$reader_info.college", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))
    print("A8 学院借阅排行:", res8)

    # A9 把 A1 结果写入 category_stats
    books.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}, "avg_rating": {"$avg": "$rating"}}},
        {"$merge": {"into": "category_stats", "whenMatched": "replace"}}
    ])
    print("A9 已执行 $merge，请去 Compass 查看 category_stats 集合。")

if __name__ == "__main__":
    main()