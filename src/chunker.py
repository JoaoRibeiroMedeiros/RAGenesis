
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


def chunk_quran(file_path):
    verses = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line at the first tab to separate the reference and the text
            reference1, text = line.split("|", 1)
            reference2, text = text.split("|", 1)
            verses.append(('Surate '+ reference1+ ' verse ' + reference2, text.strip()))
    return verses



