from Practice.book.book import Book
library = [
  Book("1984", "George Orwell"),
  Book("Красная шапочка", "Шарль Пьеро"),
  Book("Война и Мир", "Л.Н. Толстой")
]

for book in library:
  print(f"{book.title} - {book.author}")