v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 650 -630 1450 -230 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=10e-6
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
autoload=0}
B 2 650 -1080 1450 -680 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=10e-6
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 1560 -1070 2360 -670 {flags=graph
y1=-0.0339895
y2=1.966011
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=10e-6
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 1560 -640 2360 -240 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=10e-6
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
}
C {/foss/designs/xsch/comparator.sym} 310 -200 0 0 {name=x1}
C {lab_pin.sym} 160 -240 0 0 {name=p1 lab=VBIAS}
C {lab_pin.sym} 460 -240 0 1 {name=p2 lab=VOUT}
C {lab_pin.sym} 160 -220 0 0 {name=p3 lab=VIP}
C {lab_pin.sym} 460 -220 0 1 {name=p4 lab=VPRE}
C {lab_pin.sym} 160 -200 0 0 {name=p5 lab=VIN}
C {lab_pin.sym} 160 -180 0 0 {name=p6 lab=VDD}
C {lab_pin.sym} 160 -160 0 0 {name=p7 lab=VSS}
C {sky130_fd_pr/corner.sym} 20 -470 0 0 {name=CORNER only_toplevel=true corner=tt_mm}
C {code.sym} 180 -470 0 0 {name=STIMULI only_toplevel=false value=".option method=gear
.option wnflag=1

.param VDDGAUSS = agauss(1.8, 0.05, 1)
.param VDD = 'VDDGAUSS'

.param VBIASGAUSS = agauss(0.7, 0.05, 1)
.param VBIAS = 'VBIASGAUSS'

.param TEMPGAUSS = agauss(40, 30, 1)
.option temp = 'TEMPGAUSS'

.include stimuli_comparator.cir

.control
  option seed=9
  let run = 0
  
  dowhile run<=30
    save all
    tran 100n 1100u uic
    remzerovec
    set appendwrite
    reset
    let run = run + 1
.endc
"}
C {launcher.sym} 710 -170 0 0 {name=h5
descr="load waves"
tclcommand="xschem raw_read $netlist_dir/tb_comparator.raw tran"
}
