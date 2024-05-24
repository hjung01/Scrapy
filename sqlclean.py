import sqlite3

import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect(f'D:\SQLite DB\scrape_data.db')
cursor = conn.cursor()

days_ago_28 = datetime.now() - timedelta(days=28)
date_cutoff = days_ago_28.strftime('%Y-%m-%d')
delete_query = f"DELETE FROM NL_product_data WHERE date_collected < '{date_cutoff}'"
cursor.execute(delete_query)
conn.commit()
conn.close()