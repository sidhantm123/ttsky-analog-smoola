v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 330 -570 330 -390 {lab=#net1}
N 550 -570 550 -390 {lab=VPRE}
N 550 -330 550 -290 {lab=#net2}
N 330 -290 550 -290 {lab=#net2}
N 330 -330 330 -290 {lab=#net2}
N 450 -290 450 -270 {lab=#net2}
N 370 -600 510 -600 {lab=#net1}
N 330 -670 330 -630 {lab=VDD}
N 330 -670 550 -670 {lab=VDD}
N 550 -670 550 -630 {lab=VDD}
N 450 -210 450 -180 {lab=VSS}
N 550 -600 630 -600 {lab=VDD}
N 240 -600 330 -600 {lab=VDD}
N 330 -360 380 -360 {lab=VSS}
N 500 -360 550 -360 {lab=VSS}
N 450 -240 520 -240 {lab=VSS}
N 840 -630 840 -570 {lab=VDD}
N 840 -390 840 -330 {lab=VSS}
N 840 -420 910 -420 {lab=VSS}
N 910 -420 910 -360 {lab=VSS}
N 840 -360 910 -360 {lab=VSS}
N 840 -540 910 -540 {lab=VDD}
N 910 -600 910 -540 {lab=VDD}
N 840 -600 910 -600 {lab=VDD}
N 800 -540 800 -420 {lab=VPRE}
N 550 -480 800 -480 {lab=VPRE}
N 840 -510 840 -450 {lab=VOUT}
N 840 -480 940 -480 {lab=VOUT}
N 440 -750 440 -670 {lab=VDD}
N 440 -600 440 -550 {lab=#net1}
N 330 -550 440 -550 {lab=#net1}
N 670 -500 670 -480 {lab=VPRE}
C {sky130_fd_pr/nfet_01v8.sym} 310 -360 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} 570 -360 0 1 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} 530 -600 0 0 {name=M4
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
C {sky130_fd_pr/pfet_01v8.sym} 350 -600 0 1 {name=M3
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
C {ipin.sym} 110 -420 0 0 {name=p1 lab=VIP}
C {ipin.sym} 110 -390 0 0 {name=p2 lab=VIN}
C {ipin.sym} 110 -360 0 0 {name=p3 lab=VDD}
C {ipin.sym} 110 -330 0 0 {name=p4 lab=VSS}
C {lab_pin.sym} 440 -750 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 590 -360 0 1 {name=p6 sig_type=std_logic lab=VIP}
C {lab_pin.sym} 450 -180 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 240 -600 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 630 -600 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {ipin.sym} 110 -450 0 0 {name=p11 lab=VBIAS}
C {lab_pin.sym} 410 -240 0 0 {name=p12 sig_type=std_logic lab=VBIAS}
C {opin.sym} 150 -450 0 0 {name=p13 lab=VOUT}
C {lab_pin.sym} 500 -360 0 0 {name=p15 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 380 -360 0 1 {name=p16 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 -240 0 1 {name=p17 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 430 -240 0 0 {name=M5
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
C {sky130_fd_pr/pfet_01v8.sym} 820 -540 0 0 {name=M6
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
C {sky130_fd_pr/nfet_01v8.sym} 820 -420 0 0 {name=M7
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
C {lab_pin.sym} 840 -630 0 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 840 -330 0 0 {name=p18 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 940 -480 0 1 {name=p19 sig_type=std_logic lab=VOUT}
C {opin.sym} 150 -420 0 0 {name=p20 lab=VPRE}
C {lab_pin.sym} 670 -500 0 0 {name=p21 sig_type=std_logic lab=VPRE}
C {lab_pin.sym} 290 -360 0 0 {name=p22 sig_type=std_logic lab=VIN}
