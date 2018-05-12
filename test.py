from urllib.request import urlopen

test = urlopen("https://google.com")

print(test.read())

print("hello world.")