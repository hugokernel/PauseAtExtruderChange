#Name: FilamentCHange
#Info: Allow filament change for printing multi material with a single extruder setup.
#Depend: GCode
#Type: postprocess
#Param: parkX(float:160) Head park X (mm)
#Param: parkY(float:20) Head park Y (mm)
#Param: parkZ(float:+15) Head park Z (mm)
#Param: retractAmount(float:5) Retraction amount (mm)

import sys, getopt, re

def usage():
    print "Todo !"

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help", "output="])
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

'''
parkX = 160 if parkX is None else parkX
parkY = 20 if parkY is None else parkY
parkX = '+15' if parkZ is None else parkZ
retractAmount = 5 if retractAmount is None else retractAmount
'''

try:
    parkX
    parkY
    parkZ
    retractAmount
except:
    parkX = 160
    parkY = 20
    parkZ = '+15'
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
                print arg,
        print
    else:
        print g

filename = args[0]
fanValue = None

inHeader = True
beginSkip = False

#emit('G', ['X', 10])
#emit('G', 100)
#gdasas

with open(filename, "r") as f:
    x, y, z = None, None, None
    while True:
        line = f.readline()
        if not line:
            break

        if line[0:-1] == 'M117 Printing...':
            beginSkip = False
            inHeader = False

        # Skip header data
        if inHeader and line.strip() == 'T1':
            beginSkip = True
            emit("\n;Begin FilamentChange : Skip header")

        if beginSkip:
            line = ';' + line 

        if line[0:4] == 'M106':
            fanValue = line[4:].strip()
            continue

        if inHeader:
            emit(line.strip())

            if line.strip()[1:] == 'T0':
                beginSkip = False
                emit(";End FilamentChange : Skip header\n")
        else:
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
                currentExtruder = int(line[1])

                # Read next line
                line = f.readline()

                for c in str(line).split():
                    if c[0] == 'X':
                        x = c[1:]
                    elif c[0] == 'Y':
                        y = c[1:]
                    elif c[0] == 'Z':
                        z = c[1:]

                if not x or not y:
                    raise Exception("Unable to found x, y coordinate !")

                emit("\n;Begin FilamentChange %i" % currentExtruder)

                
                emit('M83', "; Extruder to relative mode")
                emit('G1', ['Z+', float(parkZ)], "; Park Z")
                emit('G1', ['E-', retractAmount], ['F', 6000], "; Retract")
                emit('G0', ['X', float(parkX)], ['Y', float(parkY)], "# Park X, Y")
                emit('M107', "; Stop fan")
                emit('M117', 'Filament', "; Message, wait user")
                emit('M0')

                # Push the filament back, and retract again, the properly primes the nozzle when changing filament.
                emit('G1', ['E', retractAmount], ['F', 6000])
                emit('G1', ['E', -retractAmount], ['F', 6000])

                emit('G1', ['X', float(x)], ['Y', float(y)], "; Restore X, Y") #, ['F', 9000])

                emit('G1', ['E', retractAmount], ['F', 6000])
                #emit('G1', ['F', 9000])

                emit('M82', "; Extruder to absolute mode")

                if fanValue:
                    emit('M106', fanValue, "; Restart fan")

                if z:
                    emit('G0', ['Z', z], "; Restore Z")
                else:
                    emit('G0', ['Z', last_z], "; Restore Z")
                #emit('G1', ['Z-', float(parkZ)])

                emit(";End FilamentChange %i\n" % currentExtruder)
            else:
                #pass
                print line.strip()

