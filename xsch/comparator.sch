v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 940 -910 940 -730 {lab=#net1}
N 1160 -910 1160 -730 {lab=VPRE}
N 1160 -670 1160 -630 {lab=#net2}
N 940 -630 1160 -630 {lab=#net2}
N 940 -670 940 -630 {lab=#net2}
N 1060 -630 1060 -610 {lab=#net2}
N 980 -940 1120 -940 {lab=#net1}
N 940 -1010 940 -970 {lab=VDD}
N 940 -1010 1160 -1010 {lab=VDD}
N 1160 -1010 1160 -970 {lab=VDD}
N 1060 -550 1060 -520 {lab=VSS}
N 1160 -940 1240 -940 {lab=VDD}
N 850 -940 940 -940 {lab=VDD}
N 940 -700 990 -700 {lab=VSS}
N 1110 -700 1160 -700 {lab=VSS}
N 1060 -580 1130 -580 {lab=VSS}
N 1450 -970 1450 -910 {lab=VDD}
N 1450 -730 1450 -670 {lab=VSS}
N 1450 -760 1520 -760 {lab=VSS}
N 1520 -760 1520 -700 {lab=VSS}
N 1450 -700 1520 -700 {lab=VSS}
N 1450 -880 1520 -880 {lab=VDD}
N 1520 -940 1520 -880 {lab=VDD}
N 1450 -940 1520 -940 {lab=VDD}
N 1410 -880 1410 -760 {lab=VPRE}
N 1160 -820 1410 -820 {lab=VPRE}
N 1450 -850 1450 -790 {lab=VOUT}
N 1450 -820 1550 -820 {lab=VOUT}
N 1050 -1090 1050 -1010 {lab=VDD}
N 1050 -940 1050 -890 {lab=#net1}
N 940 -890 1050 -890 {lab=#net1}
N 1280 -840 1280 -820 {lab=VPRE}
N 560 -940 560 -900 {lab=VDD}
N 560 -840 560 -800 {lab=VBIAS}
N 560 -820 650 -820 {lab=VBIAS}
N 650 -820 650 -770 {lab=VBIAS}
N 600 -770 650 -770 {lab=VBIAS}
N 560 -740 560 -670 {lab=VSS}
N 480 -770 560 -770 {lab=VSS}
N 650 -770 700 -770 {lab=VBIAS}
C {sky130_fd_pr/nfet_01v8.sym} 920 -700 0 0 {name=M1
W=10
L=1
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1180 -700 0 1 {name=M2
W=10
L=1
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1140 -940 0 0 {name=M4
W=20
L=1
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 960 -940 0 1 {name=M3
W=20
L=1
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {ipin.sym} 230 -830 0 0 {name=p1 lab=VIP}
C {ipin.sym} 230 -800 0 0 {name=p2 lab=VIN}
C {ipin.sym} 230 -770 0 0 {name=p3 lab=VDD}
C {ipin.sym} 230 -740 0 0 {name=p4 lab=VSS}
C {lab_pin.sym} 1050 -1090 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1200 -700 0 1 {name=p6 sig_type=std_logic lab=VIP}
C {lab_pin.sym} 1060 -520 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 850 -940 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1240 -940 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {ipin.sym} 230 -860 0 0 {name=p11 lab=VBIAS}
C {lab_pin.sym} 1020 -580 0 0 {name=p12 sig_type=std_logic lab=VBIAS}
C {opin.sym} 270 -860 0 0 {name=p13 lab=VOUT}
C {lab_pin.sym} 1110 -700 0 0 {name=p15 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 990 -700 0 1 {name=p16 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1130 -580 0 1 {name=p17 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 1040 -580 0 0 {name=M5
W=10
L=1
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1430 -880 0 0 {name=M6
W=7
L=1
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1430 -760 0 0 {name=M7
W=3.5
L=1
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1450 -970 0 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1450 -670 0 0 {name=p18 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1550 -820 0 1 {name=p19 sig_type=std_logic lab=VOUT}
C {opin.sym} 270 -830 0 0 {name=p20 lab=VPRE}
C {lab_pin.sym} 1280 -840 0 0 {name=p21 sig_type=std_logic lab=VPRE}
C {lab_pin.sym} 900 -700 0 0 {name=p22 sig_type=std_logic lab=VIN}
C {sky130_fd_pr/nfet_01v8.sym} 580 -770 0 1 {name=M8
W=10
L=1
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 560 -940 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {res.sym} 560 -870 0 0 {name=R1
value=50k
footprint=1206
device=resistor
m=1}
C {lab_pin.sym} 560 -670 0 0 {name=p23 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 700 -770 0 1 {name=p26 sig_type=std_logic lab=VBIAS}
C {lab_pin.sym} 480 -770 0 0 {name=p28 sig_type=std_logic lab=VSS}
