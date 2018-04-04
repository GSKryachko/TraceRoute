import argparse

from traceRoute import *

parser = argparse.ArgumentParser(
    description='Shows path of packet to specified host.'
                ' Host should be either IP or hostname')
parser.add_argument('address', type=str, help='address')
args = parser.parse_args()

if __name__ == '__main__':
    table = get_tracert_table(args.address)
    table = complete_tracert_table(table)
    print_tracert_table(table)
