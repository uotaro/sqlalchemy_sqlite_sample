from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///bread_shop.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,    # SQL ログを標準出力に表示（デバッグ用）
    future=True,  # SQLAlchemy 2.x スタイルを有効化
)

SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,      # 明示的にコミットするまで変更を確定しない
    autoflush=True,        # クエリ前に自動フラッシュ
    expire_on_commit=True, # コミット後にオブジェクトを再ロード対象にする
)
