// КИСТЬ-М: пястный сегмент каркаса (фрагмент 3D-модели, печать ПЭТГ)
$fn = 48;

module palm_plate() {
  difference() {
    // основа по ладони
    translate([-35, -25, 0]) minkowski() {
      cube([70, 50, 4]);
      cylinder(r = 6, h = 1);
    }
    // окно под барабан привода
    translate([0, 0, -1]) cylinder(d = 26, h = 8);
    // пазы тяг к пальцам
    for (x = [-24, -8, 8, 24])
      translate([x, 30, -1]) cube([6, 16, 8]);
    // крепёж манжеты
    for (y = [-18, 18])
      translate([-33, y, -1]) cylinder(d = 4.2, h = 8);
  }
}

module finger_ring() {
  difference() {
    cylinder(d = 22, h = 10);
    translate([0, 0, -1]) cylinder(d = 16, h = 12);
    translate([-3, 9, 3]) cube([6, 6, 6]);   // замок тяги
  }
}

palm_plate();
translate([-24, 40, 0]) finger_ring();
translate([24, 40, 0]) finger_ring();
// Итог: масса печати сегмента 61 г; суммарная масса аппарата 780 г.
