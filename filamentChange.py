#Name: Multi material
#Info: Pause the printer at a certain height
#Depend: GCode
#Type: postprocess
#Param: pauseLevel(float:5.0) Pause height (mm)
#Param: parkX(float:190) Head park X (mm)
#Param: parkY(float:190) Head park Y (mm)
#Param: retractAmount(float:5) Retraction amount (mm)

import sys, getopt, re

def usage():
    print "Todo !"

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help", "output="])
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

park_x = 160
park_y = 20
park_z = '+15'
#park_z = 15
retractAmount = 5

'''
output = None
verbose = False

for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-o", "--output"):
        output = a
    else:
        print("Option {} inconnue".format(o))
        sys.exit(2)
'''

def emit(g, *args):
    if args:
        print g,
        for arg in args:
            if isinstance(arg, list):
                if isinstance(arg[1], float):
                    print "%s%0.02f" % (arg[0], arg[1]),
                else:
                    print arg[0] + str(arg[1]),
            else:
                print arg
        print
    else:
        print g

filename = args[0]
fanValue = None

#emit('G', ['X', 10])
#emit('G', 100)
#gdasas

with open(filename, "r") as f:
    x, y, z = None, None, None
    while True:
        line = f.readline()
        if not line:
            break

        if line[0:4] == 'M106':
            fanValue = line[4:].strip()

        m = re.match(".*Z([0-9\.\+-]+)[\s\n]?", line)
        if m:
            last_z = m.group(1).strip()
            #print m.groups()
            #print "--"

        '''
        continue
        pos = line.find('Z')
        if pos > 0:
            blank = line.find(' ', pos)
            if blank < 0:
                blank = len(line)
            last_z = line[pos:blank]
            print "Found:" + last_z
        '''

        if line[0] == 'T':
            # Read next line
            line = f.readline()

            for c in str(line).split():
                if c[0] == 'X':
                    x = c[1:]
                elif c[0] == 'Y':
                    y = c[1:]
                elif c[0] == 'Z':
                    z = c[1:]

            emit(';MULTIEX BEGIN')

            # Extruder to relative mode
            emit('M83')

            # Park Z
            emit('G1', ['Z+', float(park_z)])

            # Retract
            emit('G1', ['E-', retractAmount], ['F', 6000])

            # Park X, Y
            emit('G0', ['X', float(park_x)], ['Y', float(park_y)])

            # Stop fan
            emit('M107')

            # Message, wait user
            emit('M117', 'Filament')
            emit('M0')

            # Push the filament back, and retract again, the properly primes the nozzle when changing filament.
            emit('G1', ['E', retractAmount], ['F', 6000])
            emit('G1', ['E', -retractAmount], ['F', 6000])

            # Restore X, Y
            emit('G1', ['X', float(x)], ['Y', float(y)]) #, ['F', 9000])

            emit('G1', ['E', retractAmount], ['F', 6000])
            #emit('G1', ['F', 9000])

            # Extruder to absolute mode
            emit('M82')

            # Restart fan
            if fanValue:
                emit('M106', fanValue)

            # Restore Z
            if z:
                emit('G0', ['Z', z])
            else:
                emit('G0', ['Z', last_z])
            #emit('G1', ['Z-', float(park_z)])

            emit(';MULTIEX END')
        else:
            #pass
            print line.strip()

