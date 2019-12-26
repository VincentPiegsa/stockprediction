'''
run.py -> Startet den Server (-d im Debug Mode)

> run.py -d
'''

from core import server
from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser()
    
    parser.add_argument('-d', '--debug', help='run server in debug mode', action='store_true')
    args = parser.parse_args()

    server.run(debug=args.debug, host='0.0.0.0', port=5000, threaded=True)
