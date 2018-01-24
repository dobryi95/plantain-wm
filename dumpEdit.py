#!/usr/bin/env python3
import argparse
from sys import exit

parser = argparse.ArgumentParser(description="This script edits Plaintain's(./dumps/dumpIn.mfd) wallet balance. \n NOT FOR USE IN SUBWAY!")
parser.add_argument('-a', '--amount', type=int, default=4500, help='set balance amount')
parser.add_argument('-u', '--unlimited', action='store_true', help='ignore 20k restriction (physical max is 2^32)')
args = parser.parse_args()
if args.amount<4294967295:
		if (args.amount>20000 and not args.unlimited):
			print("Are you sure you want this much? Use -h")
			exit(10)
else:
	print("Too much.")
	exit(11)


def encode_money(amount: int):
	amount = amount * 100
	amount_straight = int.to_bytes(amount, 4, 'little')  # straight code (s)
	amount_compl = int.to_bytes((1 << 32)-amount-1, 4, 'little')  # twos-complement code (c)
	k = b'\x00\xff\x00\xff'  # kopeck(k) amount = 0 (scsc)
	amount_encoded = amount_straight + amount_compl + amount_straight + k + \
									 amount_straight + amount_compl + amount_straight + k  # (32 bytes: scsk scsk)
	return amount_encoded


def write4k(content: bytearray, amount_encoded: bytes):
	content[256:288] = amount_encoded
	f = open('dumps/dumpOut.mfd', 'wb')
	f.write(content)
	f.close()


f = open('dumps/dumpIn.mfd', 'rb')
content = bytearray(f.read())
f.close()
# 1k/4k branching?
write4k(content, encode_money(args.amount))
print('Dump ready')
