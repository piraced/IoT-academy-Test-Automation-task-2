import os

#supposedly needs to be called to make color codes work on Windows terminal, havent checked it though
def CallOs():
    os.system("")


def PopulateTerminal(productTested, test, success, fail, total):
    green = '\33[92m'
    red = '\33[91m'
    normal = '\33[0m'
    CallOs()

    print("Product being tested: " + productTested)
    print("Event type: " + test["response"]["eventType"])
    print("Event subtype: " + test["response"]["eventSubtype"])
    print(f"Results so far: PASS: {green}{success}{normal} FAIL: {red}{fail}{normal} OUT OF: {total}")