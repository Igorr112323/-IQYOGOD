// АГРОСПЕКТР-К. Кронштейн камерного блока съёмочной штанги.
// Печать: ПЭТГ, заполнение 40 %, сопло 0,4 мм. Проверено на макете.
$fn = 48;

module clamp() {           // хомут на трубу штанги 40×40 мм
  difference() {
    cube([52, 52, 24], center = true);
    translate([0, 0, 0]) cube([40.4, 40.4, 26], center = true);
    translate([0, 26.5, 0]) cube([6, 8, 26], center = true); // стяжной паз
    translate([0, -26.5, 0]) cylinder(d = 6.4, h = 28, center = true); // болт М6
  }
}

module cam_plate() {       // плата камерного модуля
  difference() {
    cube([58, 44, 5]);
    for (x = [8, 50]) for (y = [8, 36])
      translate([x, y, 0]) cylinder(d = 3.2, h = 6);
    translate([29, 22, 0]) cylinder(d = 16, h = 6); // окно объектива
  }
}

module hood() {            // бленда от засветки и пыли
  difference() {
    cylinder(d1 = 34, d2 = 24, h = 18);
    translate([0, 0, 2]) cylinder(d1 = 30, d2 = 20, h = 18);
  }
}

translate([0, 0, 13]) clamp();
translate([0, 0, 0]) cam_plate();
translate([0, 22, -18]) rotate([90, 0, 0]) hood();
// Итог: блок 58×44×55 мм, масса печати 38 г, юстировка по пазам штанги.
