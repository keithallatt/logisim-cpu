# Assembly Compiler For 4-Bit CPU Designed by Keith Allatt, 2019

import sys
import json

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

output_str = "v2.0 raw\n"


def fromInputString(in_str):
    col = 0
    num_instructions = 0

    out_str = ""
    
    for row in in_str.split("\n"):
        if row.strip() == "" or row.strip().startswith("#"):
            continue        

        comm = row.split(" ")[0]
        arg = row.split(" ")[1]
        

        if comm in programming_codes:
            out_str += programming_codes[comm] + arg
            num_instructions += 1
            if num_instructions > 256:
                print("Failure: too many lines. (> 256)")
                print("Exited With Errors.")
                raise Exception()


            col += 1
            if col == 8:
                out_str += "\n"
                col = 0
            else:
                out_str += " "
        else:
            print("Failure: Unrecognized code -> "+comm)
            print("Exited With Errors.")
            raise Exception()

    return out_str


try:
    output_str += fromInputString(input_str)
except Exception:
    exit(1)

filename = filename[0:filename.rfind(".")]+"_Compiled"

f = open(filename, 'w+')

f.write(output_str)
f.close()

print("Success: "+ filename)
print("Exited Without Errors")
