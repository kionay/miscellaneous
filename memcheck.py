import ctypes
import collections
import argparse
import sys
from sys import getsizeof, stdout

class MyParser(argparse.ArgumentParser):
        def error(self, message):
                sys.stderr.write('error: {}\n'.format(message))
                self.print_help()
                sys.exit(2)

parser = MyParser(description='Gives memory details for different data types.')
parser.add_argument('--int', action='store_true',
                    help='Assumes the input is a number.')
#parser.add_argument('--float', action='store_true',
#                    help='Assumes the input is a floating point integer.')
parser.add_argument('input', action='store',
                    default=max,
                    help='Default input of numbers or characters. Assumes a string unless --int is provided.')

args = parser.parse_args()

def mem_check(check_var):
	if type(check_var) in [str]:
                for char in check_var:
                        # Utilize namereplace and standard output's encoding to ensure we either print the character, or it's name.
                        print("letter {}".format(char.encode(stdout.encoding,"namereplace").decode(stdout.encoding)))
                        # Recurse with this character's code.
                        mem_check(ord(char))
                        print() # for styling output
	elif type(check_var) is int:
                # Get the minimum number of bytes needed to hold this number.
                bitlength = (check_var.bit_length()//8)+(0 if check_var.bit_length() % 8 == 0 else 1)
                # Utilize the built-in to_bytes method to not re-interpret the number as a binary string, but get the byte string in memory of the number.
                # The difference in these is that if we use the string formatting trick to conver the integer to a binary string
                # the addresses of that new binary string will not be the same as the bytes that made up the number in memory.
                byte_string = check_var.to_bytes(bitlength, byteorder='big')
                binary_list = []
                address_list = []
                for byte in byte_string:
                        address = hex(id(byte))
                        address_list.append(address)
                        # Binary representation of our given number, padded with 0s to 8 digits to have a more visible byte object.
                        binary = "{0:b}".format(byte).zfill(8)
                        binary_list.append(binary)
                        print("a({})\tb({})\tn({})".format(address,binary,byte)) # an output format I thought was friendly
                return {"address":address_list,"binary":binary_list} # Return as dictionary to make it more re-usable. Could be zipped.
        # The following are just recurses for containers and each of their sub-items.
	elif type(check_var) in [list, set, tuple]:
		for sub_item in check_var:
                        mem_check(sub_item)
        # Slightly different from the lists and sets, the dictionaries iterate over their values, not their keys.
        # The design choice of values and not keys was exactly "eh, that sounds about right."
	elif type(check_var) in [dict, collections.OrderedDict]:
                for key, value in check_var.items():
                        print("dictionary key: {}. value: {}:".format(key,value))
                        mem_check(value)
	else:
                print("object ({}) @ address {}\ntype not yet supported: {}".format(check_var,str(hex(id(check_var))),str(type(check_var))))

this_input = args.input
if args.int or args.float:
        try:
                this_input = int(this_input) if args.int else float(this_input)
        except ValueError:
                print("ERROR: Improperly formatted number with --int flag.")
                exit()

mem_check(this_input)
