# Database access

The framework includes Flask-SQLAlchemy and makes an SQLAlchemy instance available as a variable `db` in the `app` package. You can, for example, use this to create a Pandas dataframe from an SQL query:

```python
# Pandas doesn't ship with this framework, but you can install it with
# pip install pandas
import pandas as pd

from app import db

sql = 'SELECT * FROM SomeTable'
df = pd.read_sql(sql, db.engine)
```

When using Pandas' `read_sql` function you should bear in mind that the MySQL wildcard % has to be escaped by another %, as the query is parsed as a Python format string.
