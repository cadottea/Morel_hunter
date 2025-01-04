from bs4 import BeautifulSoup

# Sample HTML to parse
html_doc = """
<html>
<head><title>Test Document</title></head>
<body>
<p class="content">This is a test paragraph.</p>
<a href="https://example.com">Example Link</a>
</body>
</html>
"""

# Parse the HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Extract title
title = soup.title.string
print("Title:", title)

# Extract paragraph text
paragraph = soup.find('p', class_='content').text
print("Paragraph:", paragraph)

# Extract link
link = soup.find('a')['href']
print("Link:", link)
