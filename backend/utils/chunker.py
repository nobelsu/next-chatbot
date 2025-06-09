from os import listdir
from markitdown import MarkItDown
from chonkie import RecursiveChunker
import duckdb

def chunkFiles():
    db = duckdb.connect("db/csv_db")
    chunks = []
    tableCnt = 0
    md = MarkItDown()
    for f in listdir("data"):
        if f[len(f)-3:] == "pdf":
            result = md.convert(f"data/{f}")
            markdown_doc = result.text_content
            chunker = RecursiveChunker.from_recipe("markdown", lang="en")
            chunks.append(chunker.chunk(markdown_doc))
        elif f[len(f)-3:] == "csv":
            table_name = f"table{tableCnt}"
            db.sql(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('data/{f}')")
            tableCnt += 1        

    return chunks, tableCnt