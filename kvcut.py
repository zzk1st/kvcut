import sys, getopt

def usage():
    print """kvcut: Cut-style command used to cut key-value style lines
Usage: python kvcut.py [-f FILE] -k key1,key2... [OPTION]
Search for keys in each line of the FILE or standard input.

Example: 
test.txt:
    a=1|b=2|c=3
    a=4|b=5
    c=6
python kvcut.py -f test.txt -k a,c
result:
    a=1 c=3
    a=4
    c=6

Regexp selection and interpretation:
  -f FILENAME           input file
  -a                    only print when all keys exist in the line
  -k key1,key2,key3 ... the key(s) to extract
  -d DELIMITER          the delimiter, by default is "|"
  -v                    output only the values"""
  
    return

delimiter="|"
value_only=False
only_print_all_keys=False
print_line_num=False
filename=""

opts, args = getopt.getopt(sys.argv[1:], "hf:k:d:van", ["help"])
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt == '-f':
        filename=arg
    elif opt == '-k':
        keys=arg.split(',')
    elif opt == '-d':
        delimiter=arg
    elif opt == '-v':
        value_only=True
    elif opt == '-a':
        only_print_all_keys=True
    elif opt == '-n':
        print_line_num=True

# read from file or pipe
if filename == "":
    lines = sys.stdin.read().splitlines()
else:
    f = open(filename)
    lines = f.read().splitlines()
    f.close()

# print the setting of kvcut
#sys.stdout.write("keys:")
#print keys
#print "delimiter: " + delimiter

line_number = 0
for line in lines:
    line_number += 1
    dict={}
    kv_pairs=line.split(delimiter)
    for kv_pair in kv_pairs:
        strs=kv_pair.split("=")
        key=strs[0]
        value=strs[-1]
        dict[key]=value
    
    # if in "a" mode, check if all keys exist in the line
    if only_print_all_keys:
        all_exist=True
        for key in keys:
            if not key in dict.keys():
                all_exist=False
        if not all_exist:
            continue

    # if none of the keys exists in the line, skip the line
    none_exist=True
    for key in keys:
        if key in dict.keys():
            none_exist=False
            break;
    if none_exist:
        break;

    # print the key and values
    if print_line_num:
        sys.stdout.write(str(line_number) + ":")

    for key in keys:
        if key in dict.keys():
            if value_only:
                sys.stdout.write(dict[key] + '\t')
            else:
                sys.stdout.write(key + "=" + dict[key] + '\t')
    print

