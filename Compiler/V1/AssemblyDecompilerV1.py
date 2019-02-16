# Assembly Compiler For 4-Bit CPU Designed by Keith Allatt, 2019

import sys
import json
import re

if len(sys.argv) == 1:
    print("Need Input File:")
    print("Usage:  \tpython3 [compiler script] [source code]")
    print("Output: \t[file name]_Compiled in same folder")
    print("Exited With Errors.")
    exit(1)


# holds the info, about each command.
assembly_json_file = sys.argv[0][0:sys.argv[0].rfind("/")] + \
                     "/CPU_ASSEMBLY_CODE.json"
programming_codes = json.loads(open(assembly_json_file, 'r').read())

filename = sys.argv[1]

input_str = open(filename, 'r').read()

output_str = "# Decompiled from \t"+filename+"\n"

def fromInputString(in_str):
    out_str = ""

    if in_str.startswith("v2.0 raw"):
        in_str = "\n".join(in_str.split("\n")[1:])

        machine_codes = dict([[v, k] for k, v in programming_codes.items()])

        for arg in re.compile("\s+").split(in_str):
            if len(arg) == 2: # valid command
                out_str += machine_codes[arg[0]] + " " + arg[1] + "\n"
    else:
        print("Not valid Format.")
        print("Exited with errors.")
        raise Exception()

    return out_str

try:
    output_str += fromInputString(input_str)
except Exception:
    exit(1)

filename = filename[0:filename.rfind("_")]+"_Decompiled.txt"

f = open(filename, 'w+')

f.write(output_str)
f.close()

print("Success: "+ filename)
print("Exited Without Errors")


