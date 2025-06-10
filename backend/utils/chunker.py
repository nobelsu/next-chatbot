from os import listdir
from markitdown import MarkItDown
from chonkie import RecursiveChunker
import duckdb

def chunkFiles():
    db = duckdb.connect("db/csv_db")
    chunks = []
    chunksSQL = []
    tableCnt = 0
    md = MarkItDown()
    for f in listdir("data"):
        if f[len(f)-3:] == "pdf":
            result = md.convert(f"data/{f}")
            markdown_doc = result.text_content
            chunker = RecursiveChunker.from_recipe("markdown", lang="en")
            chunks.extend(chunker.chunk(markdown_doc))
        elif f[len(f)-3:] == "csv":
            table_name = f"table{tableCnt}"
            if not db.sql(f"SELECT * FROM information_schema.tables WHERE table_name = '{table_name}'").fetchone():
                db.sql(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('data/{f}')")
            df = db.sql(f"DESCRIBE {table_name}").df()
            schema_text = "\n".join(
                f"{row['column_name']} {row['column_type']}" for _, row in df.iterrows()
            )
            schema_chunker = RecursiveChunker.from_recipe("markdown", lang="en")
            table_chunks = schema_chunker.chunk(schema_text)
            for chunk in table_chunks:
                chunk.metadata = {"table_name": table_name}
            chunksSQL.extend(table_chunks)
            tableCnt += 1
    return chunks, chunksSQL

chunkFiles()