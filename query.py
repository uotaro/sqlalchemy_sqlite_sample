"""クエリ・データ確認スクリプト。"""

from sqlalchemy import text

from db import get_session, Bread, Purchase


def show_all_data() -> None:
    print("\n=== 登録データ確認 ===")

    with get_session() as session:
        # --- BREAD テーブル ---
        print("\n[BREAD テーブル]")
        print(f"{'ID':>8}  {'名前':<14}  {'価格':>6}  {'在庫':>6}")
        print("-" * 44)
        for b in session.query(Bread).order_by(Bread.id).all():
            print(f"{b.id:>8}  {b.name:<14}  {b.price:>5}円  {b.inventory:>5}個")

        # --- PURCHASE テーブル（リレーション経由で商品名も表示）---
        print("\n[PURCHASE テーブル]")
        print(f"{'ID':>8}  {'商品名':<14}  {'数量':>4}  {'日時'}")
        print("-" * 60)
        for p in session.query(Purchase).order_by(Purchase.id).all():
            print(f"{p.id:>8}  {p.bread.name:<14}  {p.quantity:>4}個  {p.date}")

        # --- 売上集計（商品別・合計数量・合計金額）---
        print("\n[売上集計 (商品別)]")
        print(f"{'商品名':<14}  {'合計数量':>8}  {'合計金額':>10}")
        print("-" * 40)
        sql = text("""
            SELECT b.name,
                   SUM(p.quantity)           AS total_qty,
                   SUM(p.quantity * b.price) AS total_sales
            FROM PURCHASE p
            JOIN BREAD b ON b.id = p.bread_id
            GROUP BY b.id, b.name
            ORDER BY total_sales DESC
        """)
        for row in session.execute(sql):
            print(f"{row.name:<14}  {row.total_qty:>7}個  {row.total_sales:>9}円")


if __name__ == "__main__":
    show_all_data()
