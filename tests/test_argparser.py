import argparse

parser = argparse.ArgumentParser(prog='Program Test', description='testing')
parser.add_argument('--foo', action='store_true', help='foo help')
#parser.add_argument('bar', type=int, help='bar help')
subparsers = parser.add_subparsers(help='class help')

parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('--baz', type=int, help='baz help')

args = parser.parse_args()

if __name__ == '__main__':
    print(f'k {args.foo}')