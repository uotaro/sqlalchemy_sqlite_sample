"""サンプルデータ登録スクリプト。

毎回リセットしてから挿入するため冪等に実行できる。
Purchase の INSERT 時に events.py のリスナーが BREAD.inventory を自動デクリメントする。
"""

from datetime import datetime

from sqlalchemy import delete

from db import get_session, Bread, Purchase


def insert_sample_data() -> None:
    print("\n=== サンプルデータ登録 ===")

    breads = [
        Bread(id=10001, name="クルミパン",   price=120, inventory=15),
        Bread(id=10002, name="あんドーナツ", price=130, inventory=5),
        Bread(id=10003, name="明太フランス", price=180, inventory=8),
    ]

    purchases = [
        Purchase(id=100001, bread_id=10002, quantity=1,
                 date=datetime(2026, 4, 1, 11, 45, 12, 111000)),
        Purchase(id=100002, bread_id=10003, quantity=3,
                 date=datetime(2026, 4, 1, 11, 53, 22, 222000)),
        Purchase(id=100003, bread_id=10001, quantity=2,
                 date=datetime(2026, 4, 1, 12,  1, 33, 333000)),
        Purchase(id=100004, bread_id=10003, quantity=4,
                 date=datetime(2026, 4, 2, 11, 44, 44, 444000)),
    ]

    with get_session() as session:
        # 既存データをリセット（FK 制約があるので Purchase → Bread の順）
        session.execute(delete(Purchase))
        session.execute(delete(Bread))

        # パンを追加（在庫は初期値）
        session.add_all(breads)
        session.flush()  # Bread の PK を確定してから Purchase を追加

        # 売上を追加 → after_insert イベントで在庫が自動デクリメントされる
        session.add_all(purchases)

    print("[INFO] サンプルデータを登録しました。")
    print("[INFO] Purchase INSERT のたびに BREAD.inventory が自動デクリメントされました。")


if __name__ == "__main__":
    insert_sample_data()
