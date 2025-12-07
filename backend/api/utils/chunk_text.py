#### chunking the text into pieces for embeded
def chunk_text(text,chunk_size=500,overlap=100): 
### setting the chunk size to set the size of a chunk(in characters), 
#overlap is used to go back 100 chars so we don't lose to much context if we chunk in the middle of a sentence.
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end_of_chunk = start + chunk_size
        chunk = text[start:end_of_chunk]
        chunks.append(chunk)

        start += (chunk_size - overlap)
    return chunks
