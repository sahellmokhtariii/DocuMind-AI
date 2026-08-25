from backend.crawler.parser import HTMLParser

sample_html = """
<html>
<head>
<title>Python Tutorial</title>
</head>

<body>

<h1>Welcome</h1>

<p>Hello World</p>

<script>
alert("hello")
</script>

</body>

</html>
"""

print("Title:")
print(HTMLParser.extract_title(sample_html))

print()

print("Text:")
print(HTMLParser.extract_text(sample_html))