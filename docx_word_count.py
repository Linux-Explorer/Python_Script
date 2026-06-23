from docx import Document

def count_words_in_docx(file_path):
    # Open the document
    doc = Document(file_path)

    word_count = 0
    # Loop through all the paragraphs in the document
    for para in doc.paragraphs:
        # Split the paragraph text into words and count them
        word_count += len(para.text.split())

    return word_count

# Path to your Word document
file_path ='C:\\Users\\itsupport\\Downloads\\Lamp Setup On Ubuntu 20.docx'
print(f"Total word count: {count_words_in_docx(file_path)}")
