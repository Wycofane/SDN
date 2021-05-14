from datetime import datetime


# Log function to write actions permanently to a text file
def logger(entry):
    log = open("logSDN.txt", "a+")

    now = str(datetime.now())

    entry = str(entry)

    log.write(now + ":   " + entry + "\n")
