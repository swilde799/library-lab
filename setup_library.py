import json
import datetime
from mongodb_connect import get_db, get_client


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_extended_json(obj):
    """
    将 {"$date": "..."} 转成 datetime。
    """
    if isinstance(obj, dict):
        if set(obj.keys()) == {"$date"}:
            s = obj["$date"]
            return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return {k: convert_extended_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_extended_json(x) for x in obj]
    return obj


def create_collections(db):
    names = set(db.list_collection_names())

    for name in ["books", "readers", "category_stats"]:
        if name not in names:
            db.create_collection(name)
            print("创建普通集合:", name)

    if "book_logs" not in names:
        db.create_collection(
            "book_logs",
            capped=True,
            size=1048576,
            max=1000
        )
        print("创建固定集合: book_logs")

    if "borrow_logs" not in names:
        # 第一步：创建时不带过期时间参数，先建成功
        db.create_collection(
            "borrow_logs",
            timeseries={
                "timeField": "borrow_date",
                "granularity": "hours"
            }
        )
        print("创建时间序列集合: borrow_logs")

        # 第二步：建好之后，单独修改它的 TTL（存活时间）
        db.command({
            "collMod": "borrow_logs",
            "expireAfterSeconds": 63072000
        })
        print("已为 borrow_logs 成功配置过期时间")

    if "borrow_logs_plain" not in names:
        db.create_collection("borrow_logs_plain")
        print("创建普通镜像集合: borrow_logs_plain")

    if "book_in_stock" not in names:
        db.create_collection(
            "book_in_stock",
            viewOn="books",
            pipeline=[{"$match": {"stock": {"$gt": 0}}}]
        )
        print("创建视图: book_in_stock")


def import_books(db, data):
    col = db["books"]
    if col.count_documents({}) > 0:
        print("books 已有数据，跳过导入")
        return

    data = convert_extended_json(data)
    if not data:
        return

    r1 = col.insert_one(data[0])
    print("books insertOne 返回 inserted_id:", r1.inserted_id)

    if len(data) > 1:
        r2 = col.insert_many(data[1:])
        print("books insertMany 返回条数:", len(r2.inserted_ids))


def import_many(db, name, data):
    col = db[name]
    if col.count_documents({}) > 0:
        print(f"{name} 已有数据，跳过导入")
        return
    data = convert_extended_json(data)
    r = col.insert_many(data)
    print(f"{name} insertMany 返回条数:", len(r.inserted_ids))


def main():
    db = get_db()
    create_collections(db)

    books = load_json("books.txt")
    readers = load_json("readers.txt")
    logs = load_json("borrow_logs.txt")

    import_books(db, books)
    import_many(db, "readers", readers)

    # 时间序列集合 borrow_logs
    if db["borrow_logs"].count_documents({}) == 0:
        logs_dt = convert_extended_json(logs)
        r = db["borrow_logs"].insert_many(logs_dt)
        print("borrow_logs 时间序列集合插入条数:", len(r.inserted_ids))
    else:
        print("borrow_logs 已有数据，跳过")

    # 普通镜像集合，用于 CRUD / 删除 / lookup
    import_many(db, "borrow_logs_plain", logs)

    print("\n文档数量核对：")
    for name in ["books", "readers", "borrow_logs", "borrow_logs_plain", "book_logs", "category_stats"]:
        print(name, db[name].count_documents({}))

    print("\n集合列表：", db.list_collection_names())
    get_client().close()


if __name__ == "__main__":
    main()