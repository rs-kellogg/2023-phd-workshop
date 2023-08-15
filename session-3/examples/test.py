import sys
import logging

logging.basicConfig(filename="test.log", encoding="utf-8", level=logging.INFO)

def main(argv):
    logging.info(argv)

if __name__ == "__main__":
    main(sys.argv)
