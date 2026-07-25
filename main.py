import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/db")

data = pd.read_csv("data/HR-Employee-Attrition-Raw.csv")
data.columns = map(str.lower, data.columns)

data.to_sql(name='hr_raw',
          con=engine,
          if_exists='replace',
          index=False)

with engine.begin() as con:
    con.execute(text("DROP TABLE IF EXISTS hr_clean;"))
    con.execute(text("""CREATE TABLE hr_clean AS
                        SELECT *
                        FROM hr_raw
                        WHERE employeenumber IS NOT NULL
                        ORDER BY employeenumber;"""))
    con.execute(text("ALTER TABLE hr_clean DROP COLUMN employeecount, DROP COLUMN over18, DROP COLUMN standardhours;"))
    con.execute(text("DELETE FROM hr_clean WHERE employeenumber IN (SELECT employeenumber FROM hr_clean GROUP BY employeenumber HAVING COUNT(*) > 1);"))
    con.execute(text("ALTER TABLE hr_clean ADD PRIMARY KEY (\"employeenumber\");"))

sql = "SELECT * FROM hr_clean;"

df = pd.read_sql(sql, con=engine)

df.to_csv("data/HR-Employee-Attrition-Clean.csv", index=False)