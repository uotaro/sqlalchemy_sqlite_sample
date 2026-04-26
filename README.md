# パン屋 DB サンプル — SQLAlchemy + Alembic

SQLAlchemy 2.x と Alembic を使ったパン屋の売上管理サンプルプロジェクト。

## ファイル構成

```
.
├── db/                  --- 共通DB層（どのスクリプトからも再利用可能）
│   ├── __init__.py      --- パッケージ公開 API + イベントリスナー登録
│   ├── base.py          --- DeclarativeBase のみ（循環 import 防止）
│   ├── engine.py        --- create_engine / SessionFactory
│   ├── models.py        --- Bread / Purchase モデル定義
│   ├── events.py        --- 在庫自動デクリメント（after_insert リスナー）
│   └── session.py       --- get_session コンテキストマネージャ
│
├── create_tables.py     --- テーブル作成（初回セットアップ用）
├── insert_data.py       --- サンプルデータ登録（冪等・毎回リセット）
├── query.py             --- データ確認・売上集計クエリ
│
├── alembic.ini          --- Alembic 設定ファイル
└── alembic/
    ├── env.py           --- db.models を参照して autogenerate 対応
    ├── script.py.mako   --- マイグレーションファイルのテンプレート
    └── versions/        --- 生成されたマイグレーションファイル置き場
```

## セットアップ

```bash
# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 依存パッケージのインストール
pip install sqlalchemy alembic
```

## 基本的な使い方

3つのスクリプトを順番に実行するだけです。

```bash
python create_tables.py   # 1. テーブル作成
python insert_data.py     # 2. サンプルデータ投入
python query.py           # 3. データ確認
```

### 各スクリプトの役割

| スクリプト | 役割 | 実行タイミング |
|---|---|---|
| `create_tables.py` | BREAD / PURCHASE テーブルを作成 | 初回のみ（Alembic 導入後は不要） |
| `insert_data.py` | サンプルデータを投入（毎回リセット） | テストデータを入れ直したいとき |
| `query.py` | テーブル内容・売上集計を表示 | データ確認時 |

> `insert_data.py` は冪等です。何度実行しても同じ結果になります。

## 在庫の自動更新

`Purchase`（売上）を INSERT するたびに `Bread.inventory`（在庫）が自動でデクリメントされます。

```
あんドーナツ  在庫: 5個
  → Purchase(quantity=1) を INSERT
あんドーナツ  在庫: 4個  ← 自動更新
```

仕組みは `db/events.py` の SQLAlchemy ORM イベントリスナー（`after_insert`）です。
アプリ側で在庫更新を書き忘れる心配がなく、同一トランザクション内で完結します。

## Alembic によるスキーマ管理

テーブルの変更（カラム追加など）は `create_tables.py` の代わりに Alembic で管理します。

```bash
# 現在の適用状況を確認
alembic current

# モデルを変更した後、差分からマイグレーションファイルを自動生成
alembic revision --autogenerate -m "add column X"

# マイグレーションを適用
alembic upgrade head

# 1つ前のバージョンに戻す
alembic downgrade -1
```

### 開発フロー（Alembic 導入後）

```
1. db/models.py を編集（カラム追加・型変更など）
2. alembic revision --autogenerate -m "変更内容のメモ"
3. alembic/versions/ に生成されたファイルを確認・必要なら手修正
4. alembic upgrade head
```

## db パッケージの再利用

`db` パッケージは他のスクリプトからそのまま流用できます。

```python
from db import get_session, Bread, Purchase

with get_session() as session:
    breads = session.query(Bread).all()
```

## テーブル定義

### BREAD（パン）

| カラム | 型 | 説明 |
|---|---|---|
| id | INTEGER PK | パン ID |
| name | VARCHAR | 商品名 |
| price | INTEGER | 単価（円） |
| inventory | INTEGER | 在庫数（売上 INSERT 時に自動更新） |

### PURCHASE（売上）

| カラム | 型 | 説明 |
|---|---|---|
| id | INTEGER PK | 売上 ID |
| bread_id | INTEGER FK | BREAD.id への外部キー |
| quantity | INTEGER | 数量 |
| date | DATETIME | 売上日時 |
