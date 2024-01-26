from parser import *
import sys

if __name__ == "__main__":
    with open(sys.argv[-1]) as f:
        data = f.read()
    result: n = make_parser().parse(data)
    with open("test.txt", "w") as file:
        file.write(str(result))
    print(result)
