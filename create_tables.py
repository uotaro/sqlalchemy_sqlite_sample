"""テーブル作成スクリプト。

初回セットアップ時に実行する。既存テーブルはスキップされる。
Alembic を使う場合は代わりに `alembic upgrade head` を使用すること。
"""

from db import engine, Base
from db import models  # noqa: F401 — モデルをメタデータに登録


def create_tables() -> None:
    print("\n=== テーブル作成 ===")
    Base.metadata.create_all(engine)
    print("[INFO] テーブルを作成しました（既存の場合はスキップ）。")


if __name__ == "__main__":
    create_tables()
