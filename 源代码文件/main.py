from pymongo import MongoClient
from gridfs import GridFSBucket
db = MongoClient("mongodb://localhost:27017")["library"]
fs = GridFSBucket(db, bucket_name="fs")

while True:
    print("\n=== 智慧图书馆数字资源平台 ===")
    print("1. 查看图书总数")
    print("2. 按类别检索")
    print("3. 按书名模糊检索")
    print("4. 查询缺少tags的图书")
    print("5. 查看评分Top10")
    print("6. 查看借阅Top10")
    print("7. 查看学院借阅Top5")
    print("8. 查看GridFS电子书清单")
    print("0. 退出系统")
    
    c = input("请选择功能: ")
    
    if c == "1":
        print("馆藏图书总数:", db.books.count_documents({}))
    elif c == "2":
        cat = input("输入类别(如:计算机): ")
        print(f"{cat}类数量:", db.books.count_documents({"category": cat}))
    elif c == "3":
        kw = input("输入书名关键字: ")
        res = list(db.books.find({"title": {"$regex": kw}}))
        print("查找到:", [x["title"] for x in res])
    elif c == "4":
        print("缺tags的书数量:", db.books.count_documents({"tags": {"$exists": False}}))
    elif c == "5":
        for x in db.books.find().sort("rating", -1).limit(10):
            print(f"《{x.get('title')}》 评分:{x.get('rating')}")
    elif c == "6":
        for x in db.books.find().sort("borrow_count", -1).limit(10):
            print(f"《{x.get('title')}》 借阅:{x.get('borrow_count')}次")
    elif c == "7":
        res = db.borrow_logs.aggregate([
            {"$lookup": {"from": "readers", "localField": "reader_card", "foreignField": "card_no", "as": "r"}},
            {"$unwind": "$r"}, {"$group": {"_id": "$r.college", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}}, {"$limit": 5}
        ])
        for x in res: print(f"学院: {x['_id']} | 借阅量: {x['total']}")
    elif c == "8":
        for f in db.fs.files.find():
            print(f"文件: {f.get('filename')} | 大小: {f.get('length')} bytes")
    elif c == "0":
        print("退出系统，再见！")
        break
    else:
        print("输入无效，请重新选择！")
