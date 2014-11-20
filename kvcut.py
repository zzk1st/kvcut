import sys, getopt

def usage():
    print "USAGE: kvcut -f (filename) -k (key1,key2,key3...) -d (delimiter) -v"
    print "   -v: Print only values"
    return

delimiter="|"
value_only=False

opts, args = getopt.getopt(sys.argv[1:], "hf:k:d:v", ["help"])
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

f = open(filename)
lines = f.read().splitlines()
f.close()

sys.stdout.write("keys:")
print keys
print "delimiter: " + delimiter

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
    
    for key in keys:
        if key in dict.keys():
            if value_only:
                sys.stdout.write(dict[key] + '\t')
            else:
                sys.stdout.write(key + "=" + dict[key] + '\t')
    print

