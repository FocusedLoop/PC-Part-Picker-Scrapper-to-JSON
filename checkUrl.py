from collections import Counter

with open(r"pcpartPickerDataFomat\buildURLS.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

url_counts = Counter(urls)
duplicates = [url for url, count in url_counts.items() if count > 1]
print(duplicates)