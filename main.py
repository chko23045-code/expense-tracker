import sqlite3
import sys

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()


def add_expense(date, category, amount, memo):
    cur.execute(
        "INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?)",
        (date, category, amount, memo)
    )
    conn.commit()
    print("支出を追加しました")

def show_all():
    rows = cur.execute("SELECT * FROM expenses").fetchall()
    for row in rows:
        print(row)

def month_total(month):
    cur.execute(
        "SELECT SUM(amount) FROM expenses WHERE date LIKE ?",
        (month + "%",)
    )
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    print(f"{month} の合計: {total} 円")

def category_total():
    cur.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )
    rows = cur.fetchall()
    if not rows:
        print("登録された支出がありません")
    else:
        for row in rows:
            print(f"{row[0]}: {row[1]} 円")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python main.py add 日付 カテゴリ 金額 メモ")
        print("      python main.py list")
        print("      python main.py month YYYY-MM")
        print("      python main.py category")
        sys.exit()

    if sys.argv[1] == "add":
        add_expense(
            sys.argv[2],
            sys.argv[3],
            int(sys.argv[4]),
            sys.argv[5]
        )
    elif sys.argv[1] == "list":
        show_all()
    elif sys.argv[1] == "month":
        month_total(sys.argv[2])
    elif sys.argv[1] == "category":
        category_total()


