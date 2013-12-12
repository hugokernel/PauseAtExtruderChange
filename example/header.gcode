;Generated with Cura_SteamEngine 13.11.2
;Sliced at: Tue 10-12-2013 11:04:29
;Basic settings: Layer height: 0.25 Walls: 0.8 Fill: 100
;Print time: #P_TIME#
;Filament used: #F_AMNT#m #F_WGHT#g
;Filament cost: #F_COST#
G21        ;metric values
G90        ;absolute positioning
M107       ;start with the fan off
G28 X0 Y0  ;move X/Y to min endstops
G28 Z0     ;move Z to min endstops
G1 Z15.0 F9000 ;move the platform down 15mm
T1
G92 E0                  ;zero the extruded length
G1 F200 E10             ;extrude 10mm of feed stock
G92 E0                  ;zero the extruded length again
G1 F200 E-16.5
T0
G92 E0                  ;zero the extruded length
G1 F200 E10              ;extrude 10mm of feed stock
G92 E0                  ;zero the extruded length again
G1 F9000
M117 Printing...

;Layer count: 4
;LAYER:0
M107
G0 F3600 X49.30 Y47.80 Z0.30
;TYPE:SKIRT
G0 F3600 X53.00 Y49.53

;LAYER:3
G92 E0
G1 F2400 E-16.5000
T1
G0 F9000 X79.57 Y128.51 Z1.05
;TYPE:WALL-INNER
G1 F2400 E0.00000
G1 F2520 X73.11 Y122.06 E0.13921
G1 X78.57 Y114.74 E0.27840
G1 X78.58 Y114.35 E0.28442
G1 X76.96 Y112.13 E0.32621
G1 X74.71 Y105.20 E0.43725
