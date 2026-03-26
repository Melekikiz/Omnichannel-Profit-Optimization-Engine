import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:""@localhost:5432/profit_optimization')
df = pd.read_sql("SELECT * FROM v_master_profitability", engine)

df.to_csv('master_data.csv', index=False)