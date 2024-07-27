
# %%

def chunk_bible(file_path):

    verses = []
    with open(file_path, 'r') as file:
        i=0
        for line in file:
            if i > 1:    
                # Split the line at the first tab to separate the reference and the text
                reference, text = line.split("\t", 1)
                verses.append((reference.strip(), text.strip()))
            i+=1
    return verses

# %%
