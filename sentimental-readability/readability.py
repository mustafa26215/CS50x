from cs50 import get_string

text = get_string("Text: ")

letters = 0
words = len(text.split())
sentences = 0

for c in text:
    if c.isalpha() and c.isascii():
        letters += 1
    elif c in ".!?":
        sentences += 1

L = letters / words * 100
S = sentences / words * 100

index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
