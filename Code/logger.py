from datetime import datetime


# Log function to write actions permanently to a text file
def logger(entry):
    # open file or create a file if not existing
    log = open("logSDN.txt", "a+")

    # get the time as a String
    now = str(datetime.now())

    # convert the parameter variable to a string
    entry = str(entry)

    # add the entry to the log file
    log.write(now + ":   " + entry + "\n")
