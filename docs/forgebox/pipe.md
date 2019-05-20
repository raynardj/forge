# ForgeBox Data Pipeline For Pandas Structured Data

## Define a DataNode
A datanode can be a pandas dataframe or pandas dataframe generator (if the datasource is too huge for RAM), it's the starting/stopping point of structured data

```python
import pandas as pd
from sqlalchemy import create_engine
from forgebox.ftorch.pipe import DF_Node, DF_Chunk_Node

# Using pandas to load structured DataFrame, or generator for DataFrame
small_df = pd.read_csv("small_data.csv")
huge_df_generator = pd.read_sql("huge_sql_table", 
            con = create_engine("pymysql://someuser:weakpasswd@host:3306"), # sqldatabase connection
            chunk_size = 5000, # batch size for the generator
            )

# Define DataNode
small_node = DF_Dode(small_df)
huge_node = DF_Chunk_Node(huge_df_generator)
```

## Define Edge
Edge is what will happen between nodes

Suppose in your dataset, there are 2 columns ```["title","content"]``` are in forms of text. You want to tokenize them and count how many tokens in total for a row.

```python
from forgebox.ftorch.pipe.edge import eng_twt_tk
from forgebox.ftorch.pipe import Col_Edge, DF_Edge

count_tokens = DF_Edge("count_tokens")

@count_tokens.define
def ct(df):
    df = df.apply(lambda x:len(x["title"]+len(x["content"])),axis=1)
    return df
```
## Construct the PipeLine
### First, we try the small dataframe
```python
# eng_twt_tk is an out-of-box, tweet tokenization edge, 
# it apply to a specific column, so we can do:
# edge*[pandas_series1, pandas_series2]
small_tokened_node = small_node|eng_twt_tk*["title","content"] 
small_result_node = small_tokened_node|count_tokens

# Now run
# No edge process will be calculated until we hit run
small_result_df = small_result_node.run()
```

### Then, we try the dataframe generator

In this case, we don't have to rewrite any "edge" we've already created
```python
# Notice, for dataframe generator node, the "run" function does not return dataframe.
# This is on consideration of the dataset might be huge, since it's the reason you choose to use a generator
# For this situation, we have "edges" like "SaveSQL" and "SaveCSV" to save some result at any step you want
from forgebox.ftorch.pipe.edge import SaveSQL
save_sql = (table_name = "huge_sql_table_new",
            con = create_engine("pymysql://someuser:weakpasswd@host:3306"),)

huge_tokened_node = huge_node|eng_twt_tk*["title","content"] 
huge_result_node = huge_tokened_node|count_tokens|save_sql

# Excute the <function "run"> of the pipline, beware this does not return a dataframe
huge_result_node.run()
```
## DF_Edge and Col_edge
As you've experienced, so far there are 2 kinds of edges, they all inhereted from DF_Edge or Col_Edge
* DF_Edge and its sub-classes are edges processing dataframes
To define a dataframe edge we can define a function takes in a dataframe and spit out a dataframe
```python
df_preprocess_1 = DF_Edge("df_preprocess_[1]")
@df_preprocess_1.define
def pp1(df):
    df = dosomething(df)
    return df
```
* Col_Edge and its sub-classes are edges processing columns
To define a column edge we can define a function takes in a column and spit out a column
```python
col_preprocess_1 = DF_Edge("col_preprocess_[1]")
@col_preprocess_1.define
def colpp1(col):
    col = dosomething(col)
    return col
```

To use the edges in the pipeline
```python
new_data_node = old_data_node|df_preprocess_1|col_preprocess_1*["col1","col2","col3"]
```
