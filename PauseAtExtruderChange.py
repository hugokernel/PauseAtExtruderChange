#Name: PauseAtExtruderChange
#Info: Allow filament change for printing multi material with a single extruder setup.
#Depend: GCode
#Type: postprocess
#Param: parkX(float:160) Head park X (mm)
#Param: parkY(float:20) Head park Y (mm)
#Param: parkZ(float:+15) Head park Z (mm)
#Param: retractAmount(float:5) Retraction amount (mm)

from __future__ import print_function
import sys, getopt, re

def usage():
    print("Todo !")

verbose = False
fileout = sys.stdout

inCura = 'filename' in globals()
if inCura:
    # Load file from filename variable
    with open(filename, "r") as f:
    	lines = f.readlines()

    #sys.stdout = open(filename, 'w')
    fileout = open(filename, 'w')
else:
    parkX = 160
    parkY = 20
    parkZ = '+15'
    retractAmount = 5

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:vx:y:z:r:o:", ["help", "output="])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-v":
            verbose = True
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-x':
            parkX = arg
        elif opt == '-y':
            parkY = arg
        elif opt == '-z':
            parkZ = arg
        elif opt == '-r':
            retractAmount = arg
        elif opt == '-o':
            fileout = open(arg, 'w')
        else:
            print("Unknow {} option".format(o))
            sys.exit(2)


    # Load file from arg
    with open(args[0], "r") as f:
    	lines = f.readlines()

def emit(g, *args):
    if args:
        print(g, end = ' ', file = fileout)
        for arg in args:
            if isinstance(arg, list):
                if isinstance(arg[1], float):
                    #print("%s%0.02f".format(arg[0], arg[1]), end = '', file = fileout)
                    print("{0}{1:0.02f}".format(arg[0], arg[1]), end = ' ', file = fileout)
                else:
                    print(arg[0] + str(arg[1]), end = ' ', file = fileout)
            else:
                print(arg, end = ' ', file = fileout)
        print(file = fileout)
    else:
        print(g, file = fileout)

inHeader, beginSkip, line, lastLine, fanValue = True, False, None, None, None

x, y, z = None, None, None

if verbose:
    print("Head park X: {0}, Y: {1}, Z: {2}".format(parkX, parkY, parkZ))
    print("Retract amount : {0}".format(retractAmount))

lines = iter(lines)
try:
    while True:
        lastLine = line
        line = lines.next()
        if not line:
            break

        if line[0:-1] == 'M117 Printing...':
            beginSkip = False
            inHeader = False

        # Skip header data
        if inHeader and line.strip() == 'T1':
            beginSkip = True
            emit("\n;TYPE:CUSTOM Begin PauseAtExtruderChange : Skip header")

        if beginSkip:
            line = ';' + line if line.strip()[0] != ';' else line

        if line[0:4] == 'M106':
            fanValue = line[4:].strip()
            continue

        if inHeader:
            emit(line.strip())

            if line.strip()[1:] == 'T0':
                beginSkip = False
                emit(";TYPE:CUSTOM End PauseAtExtruderChange : Skip header\n")
        else:
            m = re.match(".*Z([0-9\.\+-]+)[\s\n]?", line)
            if m:
                last_z = m.group(1).strip()

            if line[0] == 'T':
                currentExtruder = int(line[1])

                # Read next line
                lastLine = line
                #line = f.readline()
                line = lines.next()

                for c in str(line).split():
                    if c[0] == 'X':
                        x = c[1:]
                    elif c[0] == 'Y':
                        y = c[1:]
                    elif c[0] == 'Z':
                        z = c[1:]

                if not x or not y:
                    raise Exception("Unable to found x, y coordinate !")

                emit("\n;TYPE:CUSTOM Begin PauseAtExtruderChange %i" % currentExtruder)

                emit(";" + lastLine.strip());

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

                emit(";TYPE:CUSTOM End PauseAtExtruderChange %i\n" % currentExtruder)
            else:
                #pass
                #print line.strip()
                emit(line.strip())
except StopIteration:
    pass

sys.stdout.close()

