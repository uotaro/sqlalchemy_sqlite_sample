from sqlalchemy import event, text

from .models import Purchase


@event.listens_for(Purchase, "after_insert")
def decrement_inventory(mapper, connection, target: Purchase) -> None:
    """売上（Purchase）が INSERT されるたびに在庫を自動デクリメントする。

    SQLAlchemy の ORM イベント after_insert はフラッシュ中に発火するため、
    connection を直接使って同一トランザクション内で UPDATE を実行できる。
    """
    connection.execute(
        text("UPDATE BREAD SET inventory = inventory - :qty WHERE id = :id"),
        {"qty": target.quantity, "id": target.bread_id},
    )
