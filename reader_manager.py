from mongodb_connect import get_db

def show_colleges():
    db = get_db()
    colleges = db.readers.distinct("college")
    print("\n--- 学院分布 ---")
    for c in colleges:
        count = db.readers.count_documents({"college": c})
        print(f"{c}: {count} 人")

def show_levels():
    db = get_db()
    levels = db.readers.distinct("level")
    print("\n--- 等级分布 ---")
    for lv in levels:
        count = db.readers.count_documents({"level": lv})
        print(f"{lv}: {count} 人")

def find_reader():
    db = get_db()
    card = input("输入借阅证号: ")
    r = db.readers.find_one({"card_no": card})
    if r:
        print(f"姓名: {r.get('name')}, 学院: {r.get('college')}, 等级: {r.get('level')}")
    else:
        print("未找到该读者。")