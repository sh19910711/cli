#!/usr/bin/env python3
import sys
import makestack
from makestack.helpers import error


if __name__ == "__main__":
    try:
        makestack.main.main(sys.argv)
    except KeyboardInterrupt:
        error("\nmakestack: aborted")
