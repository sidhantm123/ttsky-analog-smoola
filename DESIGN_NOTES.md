# EMG ADC — Design Notes
## Project: tt_um_sidhantm123_neural_adc
**Repo:** https://github.com/sidhantm123/ttsky-analog-smoola  
**Platform:** Tiny Tapeout SKY130A shuttle  
**Submission type:** Mixed-signal analog  
**Tile size:** 1×2 analog tile (~36,000 µm²)  
**Analog pins used:** 2  
**Estimated shuttle cost:** ~220€  

---

## Target Shuttle
- **Shuttle:** TTSKY26a (SkyWater SKY130A)
- **Submission deadline:** May 11, 2026
- **Estimated chip delivery:** 16 December 2026
- **Time available:** 40 days from april 1st 2026

## What This Chip Does

A single-channel surface EMG (electromyography) front end. It accepts a pre-amplified analog EMG signal from patch electrodes via an external PCB, passes it through switchable filters, digitizes it with a 6-bit SAR ADC, detects motor unit action potential (MUAP) threshold crossings, enforces a refractory period to prevent double-counting, and outputs either the raw digital sample or a running 8-bit MUAP count — selectable at runtime.

---

## Architecture

The design is split into two halves with fundamentally different workflows:

```
ua[0] ──→ [ HPF 30Hz ]──→ [ LPF 500Hz ]──→ [ Cap DAC (64 unit caps) ]
ua[1] ──→ Vref                                       ↓
ui_in[0] → HPF on/off                        [ Comparator ]
ui_in[1] → LPF on/off                               ↓
                                            [ SAR FSM (6 cycles) ]
                                                     ↓
                                          [ 6-bit ADC result ]
                                                     ↓
                             ui_in[7:2] ──→ [ Threshold Detector ]
                                                     ↓
                                          [ Refractory Counter ]
                                                     ↓
                                          [ 8-bit Spike Counter ]
                                                     ↓
                             uio[0] ──────→ [ Output Mux ]
                                                     ↓
                                            uo_out[7:0]
```

### Analog Front End
Hand-laid-out in Magic VLSI using Xschem schematics and ngspice simulation. NOT synthesized from Verilog.

- **High-pass filter (30 Hz):** Blocks DC electrode offset and low-frequency motion artefacts. SENIAM-compliant lower cutoff for surface EMG. RC time constant ≈ 5.3 ms. Bypassable via `ui_in[0]`. Pseudo-resistor PMOS topology. Cutoff frequency fixed in silicon.
- **Low-pass filter (500 Hz):** Anti-aliasing filter; EMG signal energy is concentrated below 500 Hz per SENIAM guidelines. RC time constant ≈ 318 µs. Bypassable via `ui_in[1]`. Cutoff frequency fixed in silicon.
- **Comparator:** Simple differential comparator. Sits at the heart of the SAR ADC, comparing the input voltage against the capacitor DAC output on each conversion cycle. ~20–30 transistors.
- **6-bit Capacitor DAC:** Binary-weighted array of 64 unit capacitors (~25 µm² each, ~5×5 µm). Switch transistors connect each cap to either Vref or GND under control of the SAR FSM. Total cap array area ~3,200 µm² including routing and spacing overhead.

### Digital Back End
Written in Verilog, synthesized via OpenLane/LibreLane, standard Tiny Tapeout HDL flow.

- **SAR Control FSM:** Sequences 6 conversion cycles. On each cycle: sets a DAC bit high, reads comparator output, keeps or clears the bit (successive approximation). Assembles the final 6-bit result after all cycles complete.
- **Threshold Detector:** Compares 6-bit ADC output to the 6-bit threshold loaded from `ui_in[7:2]`. Asserts spike signal when `adc_out >= threshold`.
- **Refractory Counter:** Enforces a 75 ms dead-time after each detected MUAP. Motor unit inter-discharge intervals range from 20–200 ms; 75 ms corresponds to a firing rate of ~13 Hz typical of moderate voluntary contraction (Farina et al. 2014). Implemented as an 11-bit down-counter (1500 cycles at 20 kHz) that blocks new detections while nonzero.
- **Spike Counter:** 8-bit counter, increments on each validated spike event (i.e., threshold crossed AND refractory period expired).
- **Output Mux:** Selects between raw 6-bit ADC value (zero-padded to 8 bits on `uo_out[7:0]`) and 8-bit spike count, controlled by `uio[0]`.

---

## Pin Assignment

### Analog Pins
| Pin | Function |
|-----|----------|
| `ua[0]` | Analog EMG signal input (pre-amplified by external PCB, expected range ~100mV–1V) |
| `ua[1]` | External reference voltage (Vref) for the capacitor DAC |
| `ua[2]`–`ua[5]` | Not connected (not paid for) |

### Digital Inputs
| Pin | Function |
|-----|----------|
| `ui_in[0]` | High-pass filter enable (1 = 30 Hz HPF active, 0 = bypassed) |
| `ui_in[1]` | Low-pass filter enable (1 = 500 Hz LPF active, 0 = bypassed) |
| `ui_in[2]` | Spike threshold bit 0 (LSB) |
| `ui_in[3]` | Spike threshold bit 1 |
| `ui_in[4]` | Spike threshold bit 2 |
| `ui_in[5]` | Spike threshold bit 3 |
| `ui_in[6]` | Spike threshold bit 4 |
| `ui_in[7]` | Spike threshold bit 5 (MSB) |
| `clk` | System clock (20 kHz, 50 µs period — gives 2857 SPS, 4× Nyquist above 500 Hz LPF) |
| `rst_n` | Active-low reset |

### Digital Outputs
| Pin | Function |
|-----|----------|
| `uo_out[7:0]` | 8-bit data output — raw ADC sample (bits [5:0], [7:6] = 0) or 8-bit spike count depending on mode |

### Bidirectional Pins
| Pin | Direction | Function |
|-----|-----------|----------|
| `uio[0]` | Input | Mode select (0 = raw ADC output, 1 = spike count output) |
| `uio[1]` | Output | Spike event pulse (goes high for exactly 1 clock cycle on each validated spike) |
| `uio[2]`–`uio[7]` | — | Unused — tied to GND as required by analog submission rules |

---

## Key Design Decisions & Rationale

### Why 6-bit ADC and not 8-bit?
- 6-bit = 64 unit capacitors, 8-bit = 256 unit capacitors. The capacitor array is the dominant area block.
- Unit cap size also scales: 6-bit needs ~25 µm² per cap for matching, 8-bit needs ~100 µm² per cap. This gives ~16× total area difference for the cap array alone.
- 6-bit ADC fits in 1×2 tile. 8-bit ADC needs 2×2 tiles and is still tight.
- Neural spike detection does not require 8-bit precision — you're detecting threshold crossings, not measuring waveform amplitudes with high fidelity. 6 bits (64 levels) is sufficient.
- 6-bit is significantly more forgiving of process variation and capacitor mismatch.

### Why fixed filter cutoffs?
- Filter cutoff frequency is set by RC component values baked into silicon — cannot be changed post-fabrication without switchable component banks.
- Switchable resistor/capacitor banks would consume most of the remaining `ui_in` pins, forcing removal of the programmable threshold.
- Programmable threshold is more valuable for the application than tunable filter frequencies.
- 30 Hz HPF and 500 Hz LPF follow SENIAM guidelines for surface EMG and cover the vast majority of use cases (Merletti et al. 2004, De Luca et al. 2010).

### Why no on-chip amplifier?
- A low-noise amplifier (LNA) is the most impactful upgrade but also the hardest analog block to design and the most sensitive to process variation.
- Decision: assume input signal is pre-amplified externally (~100mV–1V at the pin) for first silicon.
- The filters (especially the HPF) are more critical to basic function than the LNA — a chip without HPF will immediately saturate with a real electrode due to DC offset.
- LNA can be added in a future revision once the core ADC and digital flow is validated.

### Why `uses_3v3: false`?
- Standard 1.8V digital supply is sufficient for the comparator and filter topologies being used.
- 3.3V requires a different DEF template and adds power FET overhead that reduces usable area.
- Keeping to 1.8V simplifies the flow considerably.

### Clock frequency
- 20 kHz (50 µs period). SAR ADC performs 6 conversion cycles per sample → ~2857 SPS.
- EMG signal bandwidth is DC–500 Hz per SENIAM; 2857 SPS is 4× above Nyquist (satisfied).
- 20 kHz also gives refractory period of exactly 1500 cycles = 75 ms (clean round number).
- CLOCK_PERIOD in config.json = 50000 ns.

---

## Workflow Overview

### Analog blocks (comparator, filters, cap DAC)
Tools: **Xschem** (schematic) → **ngspice** (simulation) → **Magic VLSI** (layout) → **netgen** (LVS)

Recommended environment: Harald Pretl's **IIC-OSIC-TOOLS Docker image** — ships all tools pre-configured with SKY130A PDK.

```bash
docker pull hpretl/iic-osic-tools
```

Order of development:
1. Comparator — schematic + sim → layout → LVS → post-layout sim
2. Filters (HPF then LPF) — same flow
3. Capacitor DAC — layout only (switches + binary-weighted cap array)
4. Full analog integration

### Digital blocks (SAR FSM, threshold, counter)
Tools: Standard Tiny Tapeout Verilog flow — **iverilog/verilator + cocotb** for testing, **LibreLane** for hardening.

```bash
# Testing
brew install icarus-verilog
pip install cocotb pytest

# Local hardening
export PDK_ROOT=~/ttsetup/pdk
export PDK=sky130A
export LIBRELANE_TAG=2.4.2
pip install librelane==$LIBRELANE_TAG
./tt/tt_tool.py --create-user-config
./tt/tt_tool.py --harden
```

Order of development:
1. SAR FSM — write and test with a simulated 1-bit comparator input
2. Threshold detector — test independently
3. Refractory counter — test independently
4. Spike counter — test independently
5. Top-level digital integration and full cocotb test

### Integration
1. Synthesize digital blocks → get gate-level netlist
2. Place hardened digital macro inside Magic layout
3. Connect analog outputs to digital inputs through metal routing
4. Full-chip DRC + LVS
5. Export GDS → `gds/tt_um_sidhantm123_neural_adc.gds`
6. Export LEF (pinonly) → `lef/tt_um_sidhantm123_neural_adc.lef`

---

## Repository Structure

```
ttsky-analog-smoola/
├── src/
│   └── project.v             ← Verilog blackbox stub (NOT synthesized)
│   └── digital/              ← (to be created) Verilog source for digital blocks
├── test/                     ← cocotb testbenches for digital blocks
├── gds/                      ← Final GDS file goes here before submission
├── lef/                      ← Final LEF file goes here before submission
├── xschem/                   ← (to be created) Xschem schematics
├── mag/                      ← (to be created) Magic layout files
├── sim/                      ← (to be created) ngspice simulation files
├── docs/
│   └── info.md               ← Project documentation for Tiny Tapeout website
├── info.yaml                 ← Project metadata (tiles, pins, pinout)
└── DESIGN_NOTES.md           ← This file
└── setup_log.txt             ← Instructions to setup dependencies and softwares (IGNORE THIS)
└── working_instructions.txt  ← Instructions to run softwares and tools
```

---

## info.yaml Status
- `top_module`: `tt_um_sidhantm123_neural_adc` ✓
- `tiles`: `1x2` ✓
- `analog_pins`: `2` ✓
- `uses_3v3`: `false` ✓
- `clock_hz`: `20000` ✓
- `pinout`: filled in ✓
- `src/project.v` module name updated to match `top_module` ✓

---

## Still To Do
- [ ] Update `src/project.v` module name from template default to `tt_um_sidhantm123_neural_adc`
- [ ] Enable GitHub Pages (Settings → Pages → Source → GitHub Actions)
- [ ] Enable GitHub Actions (Actions tab → Enable)
- [ ] Set up IIC-OSIC-TOOLS Docker environment
- [ ] Work through a simple Xschem/ngspice/Magic/netgen tutorial before touching actual design
- [ ] Write SAR FSM Verilog + cocotb tests
- [ ] Write threshold detector Verilog + tests
- [ ] Write refractory counter Verilog + tests
- [ ] Write spike counter Verilog + tests
- [ ] Design and simulate comparator in Xschem
- [ ] Lay out comparator in Magic, run LVS
- [ ] Design HPF and LPF
- [ ] Design capacitor DAC
- [ ] Full analog + digital integration
- [ ] DRC clean
- [ ] LVS clean
- [ ] Submit via app.tinytapeout.com

---

## Resources
- Tiny Tapeout analog specs: https://tinytapeout.com/specs/analog/
- SKY130A analog template: https://github.com/TinyTapeout/ttsky-analog-template
- IIC-OSIC-TOOLS Docker: https://github.com/iic-jku/iic-osic-tools
- Xschem tutorial (video): https://www.youtube.com/watch?v=q3ZcpSkVVuc
- Carsten Wulff analog series (video): https://www.youtube.com/playlist?list=PLybHXZ9FyEhZfwQTKrLhm6ZZm4IDfGGla
- Tim Edwards Magic demo (video): https://youtu.be/XvBpqKwzrFY
- Matt's Zero to ASIC analog course: https://zerotoasiccourse.com/analog
- SKY130A PDK docs: https://skywater-pdk.readthedocs.io
- Tiny Tapeout Discord (#verilog-and-hdl, #analog): https://discord.gg/rPK2nSjxy8
