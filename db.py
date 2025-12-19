import psycopg2
from psycopg2 import sql
from typing import Dict, Any, Tuple, List

# DB 連線設定
DB_NAME = "my_class_db"
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# ------------------------------
# 工具：把 dict 轉成 SQL set/where
# ------------------------------
def _dict_to_set_parts(data: Dict[str, Any], separator: str = ' AND '):
    if data is None or data == 1:
        return sql.SQL("1=1"), []

    parts = []
    values = []
    for key, val in data.items():
        parts.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
        values.append(val)

    return sql.SQL(separator).join(parts), values

# ------------------------------
# INSERT
# ------------------------------
def ins(table: str, data: dict,where='id'):
    columns = list(data.keys())
    cols_sql = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
    placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in columns)
    values = list(data.values())

    query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING {}").format(
        sql.Identifier(table), cols_sql, placeholders,sql.Identifier(where)
    )

    cursor.execute(query, values)
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

# ------------------------------
# SELECT
# ------------------------------
def sel(table: str, where_data=1, order_by='id', desc="ASC"):
    where_clause, values = _dict_to_set_parts(where_data)
    
    query = sql.SQL("SELECT * FROM {} WHERE {}").format(
        sql.Identifier(table), where_clause
    )
    
   
    if order_by:
        query += sql.SQL(" ORDER BY {} {}").format(
            sql.Identifier(order_by),
            sql.SQL(desc.upper())  
        )

    cursor.execute(query, values)
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    dict_rows = [dict(zip(columns, r)) for r in rows]
    return dict_rows



# ------------------------------
# UPDATE
# ------------------------------
def upd(table: str, set_dict: dict, where_dict: dict):
    set_clause, set_vals = _dict_to_set_parts(set_dict, separator=", ")
    where_clause, where_vals = _dict_to_set_parts(where_dict)

    query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
        sql.Identifier(table), set_clause, where_clause
    )

    cursor.execute(query, set_vals + where_vals)
    conn.commit()
    return cursor.rowcount

# ------------------------------
# DELETE
# ------------------------------
def delete(table: str, where_dict: dict):
    where_clause, values = _dict_to_set_parts(where_dict)

    query = sql.SQL("DELETE FROM {} WHERE {}").format(
        sql.Identifier(table), where_clause
    )

    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount

def create_table(table: str, columns: Dict[str, str]):
    if not cursor:
        print("資料庫連線或游標物件無效，無法執行操作。")
        return

    col_definitions = []
    for name, typ in columns.items():
        col_definitions.append(
            sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(typ))
        )

    cols_sql = sql.SQL(",\n    ").join(col_definitions)

    query = sql.SQL("CREATE TABLE {} (\n    {}\n)").format(
        sql.Identifier(table), cols_sql
    )

    try:
        cursor.execute(query)
        conn.commit()
        print(f"成功建立資料表: {table}")
    except psycopg2.Error as e:
        print(f"建立資料表 {table} 失敗: {e}")
        conn.rollback()

def selTables(search_name=None):
    # 先抓所有 table 名稱
    if search_name:
        query = """
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname='public' AND tablename ILIKE %s
            ORDER BY tablename;
        """
        cursor.execute(query, (f"%{search_name}%",))
    else:
        query = """
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname='public'
            ORDER BY tablename;
        """
        cursor.execute(query)
    
    tables = cursor.fetchall()
    result = []

    for t in tables:
        table_name = t[0]

        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = cursor.fetchall()
        col_list = [{"name": c[0], "type": c[1]} for c in columns]
        result.append({"name": table_name, "columns": col_list})
    
    return result



# ------------------------------
# DROP TABLE (刪除資料表)
# ------------------------------
def drop_table(table: str, if_exists: bool = True):
    if not cursor:
        print("資料庫連線或游標物件無效，無法執行操作。")
        return
        
    if if_exists:
        query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table))
    else:
        query = sql.SQL("DROP TABLE {}").format(sql.Identifier(table))

    try:
        cursor.execute(query)
        conn.commit()
        print(f"成功刪除資料表: {table} (或該表不存在)")
    except psycopg2.Error as e:
        print(f"刪除資料表 {table} 失敗: {e}")
        conn.rollback()
    
def alert(content, where=""):
    safe_content = content.replace("'", "\\'")
    return f"""
    <script>
        alert('{safe_content}');
        window.location.href = '{where}';
    </script>
    """