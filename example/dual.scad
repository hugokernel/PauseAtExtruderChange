
use <oshw.scad>;

/*
%translate([0, 0, 0]) {
    cube([10, 10, 1], center = true);
}

color("RED") translate([0, 0, 1]) {
    cube([10, 10, 1], center = true);
}

%translate([0, 0, 2]) {
    cube([10, 10, 1], center = true);
}
*/

difference() {
    translate([0, 0, 2.5]) {
        cube([20, 20, 5], center = true);
    }

    translate([0, 0, 4]) {
        linear_extrude(height=1)
	        oshw_logo_2d(15);
    }
}

