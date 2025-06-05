from os import listdir
from markitdown import MarkItDown
from chonkie import RecursiveChunker

def chunkFiles():
    chunks = []
    md = MarkItDown()
    for f in listdir("data"):
        result = md.convert(f"data/{f}")
        markdown_doc = result.text_content
        chunker = RecursiveChunker.from_recipe("markdown", lang="en")
        chunks.append(chunker.chunk(markdown_doc))
    return chunks