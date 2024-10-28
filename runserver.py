# !/usr/bin/env python

# -----------------------------------------------------------------------
# runserver.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# Starts the server for the Portfolio Website

# -----------------------------------------------------------------------

import sys
import argparse
import app

# -----------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="runserver.py",
        description="The program which starts the server",
        allow_abbrev=False
    )

    parser.add_argument('port', type=int,
                        help="the port at which the server " + 
                        "should listen")
    return parser

def main():
    try:
        parser = parse_args()
        args = parser.parse_args()
        port = args.port

        try: 
            app.app.run(host='0.0.0.0', port=port, debug=True)
        except Exception as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

# -----------------------------------------------------------------------

if __name__ == '__main__':
    main()
