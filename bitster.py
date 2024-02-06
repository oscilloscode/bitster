#!/usr/bin/env python
import sys
from pathlib import Path

BIT_COUNT = 32


def vert_box(string, start, stop):
    return (
        string[: (BIT_COUNT - stop_bit - 1) * 3]
        + "| "
        + string[(BIT_COUNT - stop_bit - 1) * 3 : (BIT_COUNT - start_bit) * 3]
        + "| "
        + string[(BIT_COUNT - start_bit) * 3 :]
    )


def hor_box(start_bit, stop_bit):
    return (
        " " * ((BIT_COUNT - stop_bit - 1) * 3)
        + "+"
        + "-" * ((stop_bit - start_bit + 1) * 3 + 1)
        + "+"
        + " " * (start_bit * 3)
    )


def box(strings, start_bit, stop_bit):
    boxed_strings = []

    hor_box_string = hor_box(start_bit, stop_bit)

    boxed_strings.append(hor_box_string)
    boxed_strings.extend(map(lambda s: vert_box(s, start_bit, stop_bit), strings))
    boxed_strings.append(hor_box_string)

    return boxed_strings


def usage():
    filename = Path(__file__).name
    print("\nUSAGE:")
    print(f"\t{filename} DATA")
    print(f"\t{filename} DATA [BIT]")
    print(f"\t{filename} DATA [START_BIT] [START_BIT]")

    print("\nARGS:")
    print(
        "\t<DATA>         Data in bin, oct, dec, or hex notation determined by prefix (e.g. 0b1011, 0o23, 13, 0x4d)"
    )
    print("\t<BIT>          Bit to be highlighted. ")
    print("\t<START_BIT>    First bit to be highlighted. ")
    print("\t<STOP_BIT>     Last bit to be highlighted. ")


match len(sys.argv):
    case 2:
        boxing = False
    case 3:
        start_bit = int(sys.argv[2])
        stop_bit = start_bit
        boxing = True
    case 4:
        start_bit = int(sys.argv[2])
        stop_bit = int(sys.argv[3])
        if start_bit > stop_bit:
            temp = start_bit
            start_bit = stop_bit
            stop_bit = temp
        boxing = True
    case _:
        print("ERROR: invalid amount of arguments")
        usage()
        sys.exit(0)

num = int(sys.argv[1], 0)

if num >= 2**BIT_COUNT:
    print(f"ERROR: DATA larger than unsigned {BIT_COUNT} bits.")
    usage()
    sys.exit(0)

if boxing:
    if not ((BIT_COUNT > start_bit >= 0) and (BIT_COUNT > stop_bit >= 0)):
        print("ERROR: Bit(s) out of range")
        usage()
        sys.exit(0)

print(f"Input: {num} | 0x{num:X} | 0b{num:b}\n")

bit_string = " " + "  ".join(f"{num:0{BIT_COUNT}b}") + " "
indices_string = " ".join(map(lambda b: f"{b:2}", range(BIT_COUNT - 1, -1, -1))) + " "
output = [indices_string, " " * BIT_COUNT * 3, bit_string]

if boxing:
    output = box(output, start_bit, stop_bit)

for s in output:
    print(s)
