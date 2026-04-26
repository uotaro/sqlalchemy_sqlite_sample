from contextlib import contextmanager

from sqlalchemy.orm import Session

from .engine import SessionFactory


@contextmanager
def get_session():
    """トランザクション付きセッションを提供するコンテキストマネージャ。

    with get_session() as session:
        session.add(...)
    # ブロックを抜けると自動コミット or ロールバック
    """
    session: Session = SessionFactory()
    try:
        yield session
        session.commit()
        print("[INFO] トランザクションをコミットしました。")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] ロールバックしました: {e}")
        raise
    finally:
        session.close()
        print("[INFO] セッションをクローズしました。")
