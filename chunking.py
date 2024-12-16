import re

def chunk_law_text(file_path):
    """
    Chunk a law text file into individual articles.
    
    Args:
        file_path (str): Path to the .txt file containing the law text
    
    Returns:
        list: A list of strings, each representing an individual article
    """
    # Read the entire file
    with open(file_path, 'r', encoding='utf-8') as file:
        full_text = file.read()
    
    # Use regex to split the text into articles
    # This pattern looks for 'Член' followed by a number at the start of a line
    # The (?=\n|\s) ensures it's followed by a newline or whitespace to avoid 
    # catching references within the text
    articles = re.split(r'\n(Член \d+)\n', full_text)[1:]
    
    # Reconstruct the articles 
    # The split will alternate between article headers and content
    chunked_articles = []
    for i in range(0, len(articles), 2):
        # Combine the article header with its content
        if i+1 < len(articles):
            article = articles[i] + '\n' + articles[i+1]
            chunked_articles.append(article.strip())
    
    return chunked_articles

# Example usage
# articles = chunk_law_text('path/to/your/law_text.txt')
# for article in articles:
#     print(article)
#     print('-' * 50)  # Separator between articles