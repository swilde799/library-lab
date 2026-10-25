import sys
from mongodb_connect import get_db, close
import book_manager
import reader_manager
import borrow_manager
import stat_manager


def show_status():
    """程序启动时打印数据库连接状态与集合文档总数 (ST-5.5)"""
    try:
        db = get_db()
        print("=" * 40)
        print("✅ 数据库连接成功！")
        print(f"图书总数: {db.books.count_documents({})} 本")
        print(f"读者总数: {db.readers.count_documents({})} 人")
        print(f"借阅流水: {db.borrow_logs_plain.count_documents({})} 条")
        print("=" * 40)
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        sys.exit(1)


def main():
    show_status()
    while True:
        print("\n==== 图书情报检索与统计平台 ====")
        print("1. 检索图书 (书名)")
        print("2. 图书评分排行")
        print("3. 查看学院分布")
        print("4. 查看读者等级分布")
        print("5. 借阅登记")
        print("6. 归还处理")
        print("7. 查看逾期记录")
        print("8. 分类统计报表")
        print("9. 借阅趋势分析")
        print("10. 畅销榜")
        print("0. 退出系统")
        print("===============================")

        choice = input("请选择功能 (0-10): ")

        if choice == '1':
            book_manager.search_books()
        elif choice == '2':
            book_manager.top_rated_books()
        elif choice == '3':
            reader_manager.show_colleges()
        elif choice == '4':
            reader_manager.show_levels()
        elif choice == '5':
            borrow_manager.borrow_book()
        elif choice == '6':
            borrow_manager.return_book()
        elif choice == '7':
            borrow_manager.check_overdue()
        elif choice == '8':
            stat_manager.category_stats()
        elif choice == '9':
            stat_manager.borrow_trend()
        elif choice == '10':
            stat_manager.bestsellers()
        elif choice == '0':
            print("正在关闭数据库连接...")
            close()
            print("已退出系统。再见！")
            break
        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()