import wikipedia
import time

def random_wiki_summary():
    # title of a random wiki page
    random = wikipedia.random(1)
    try:
        result = wikipedia.summary(random)
    except Exception as e:
        # try again if you get an error
        result = random_wiki_summary()
    return result

while True:
    time.sleep(1.0)

    # open and read file
    f = open("random_wiki_service.txt", "r")
    line = f.readline()
    f.close()

    if line == "run":
        result = random_wiki_summary()
        # erase file and write random wikipedia page summary
        f = open("random_wiki_service.txt", "w")
        f.write(result)
        f.close()
        print("summary written to text file")
