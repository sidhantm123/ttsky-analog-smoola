"""
test_sar_fsm.py — cocotb testbench for the 6-bit SAR FSM

Tests:
  1. Three known conversion values (42, 0, 63)
  2. conv_done pulses for exactly 1 clock cycle
  3. Conversion restarts automatically after conv_done
  4. dac_bits trial sequence is correct for target=42

Timing note:
  `await RisingEdge(dut.clk)` resumes in the active region, before
  non-blocking assigns (NBAs) have propagated.  A 1 ns Timer after
  each edge lets the NBA region settle so register outputs are stable
  before we sample them.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def get_comparator_seq(target):
    """
    Compute the comparator response sequence for a given target value.
    Returns (seq, recovered) where:
      seq       = list of 6 comparator values (1 or 0), MSB first
      recovered = the value the SAR algorithm would reconstruct
    """
    seq = []
    dac = 0
    for bit in range(5, -1, -1):
        trial = dac | (1 << bit)
        cmp = 1 if target >= trial else 0
        seq.append(cmp)
        if cmp:
            dac = trial
    return seq, dac


async def clk_edge(dut):
    """Await one rising edge, then let NBAs settle."""
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


async def reset_dut(dut):
    """Apply active-low reset for 2 clock cycles then release."""
    dut.rst_n.value = 0
    dut.comparator_in.value = 0
    await clk_edge(dut)
    await clk_edge(dut)
    dut.rst_n.value = 1
    # Let rst_n deassertion propagate before first conversion edge
    await Timer(1, units="ns")


async def run_conversion(dut, target, label=""):
    """
    Drive a full 6-bit SAR conversion for the given target value.

    Drives comparator_in with the correct SAR responses, then:
    - asserts conv_done is high for exactly 1 cycle after 6 conversion edges
    - checks adc_result equals the target
    - checks conv_done drops the following cycle
    - checks dac_bits resets to 6'b100000 (restart)

    Returns the adc_result value seen when conv_done is asserted.
    """
    seq, expected = get_comparator_seq(target)

    dut._log.info(
        f"[{label}] target={target} (0b{target:06b}), "
        f"comparator_seq={seq}, expected={expected}"
    )

    # Drive comparator for the first trial (bit 5) before the first edge
    dut.comparator_in.value = seq[0]

    # --- 6 conversion edges (states 0 → 5 → 6) ---
    for i in range(6):
        await clk_edge(dut)
        # NBAs have now settled; FSM has processed seq[i].

        if i < 5:
            # Not done yet — feed comparator value for the next trial
            assert dut.conv_done.value == 0, (
                f"[{label}] conv_done spuriously high at conversion step {i}"
            )
            dut.comparator_in.value = seq[i + 1]
        else:
            # After the 6th edge (state 5→6): conv_done should be 1
            assert dut.conv_done.value == 1, (
                f"[{label}] conv_done not asserted after 6 conversion cycles"
            )
            result = int(dut.adc_result.value)
            assert result == expected, (
                f"[{label}] adc_result={result} != expected={expected} "
                f"(target={target})"
            )
            dut._log.info(f"[{label}] conv_done=1, adc_result={result} ✓")

    # --- conv_done must deassert after exactly 1 cycle ---
    # Drive comparator for the upcoming restart conversion
    dut.comparator_in.value = seq[0]
    await clk_edge(dut)  # state 6 → 0; conv_done NBA clears

    assert dut.conv_done.value == 0, (
        f"[{label}] conv_done still high — should be a 1-cycle pulse"
    )
    dut._log.info(f"[{label}] conv_done deasserted ✓")

    # --- Verify restart: dac_bits should be back to 6'b100000 = 32 ---
    assert int(dut.dac_bits.value) == 0b100000, (
        f"[{label}] dac_bits={int(dut.dac_bits.value):06b} after restart, "
        f"expected 100000"
    )
    dut._log.info(f"[{label}] dac_bits=100000 after restart ✓")

    return result


# ---------------------------------------------------------------------------
# Test: three known conversion values
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_conversion_42(dut):
    """Convert 42 (0b101010) — mid-range alternating bits."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)
    await run_conversion(dut, 42, label="target=42")


@cocotb.test()
async def test_conversion_0(dut):
    """Convert 0 (0b000000) — minimum value, all comparator responses 0."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)
    await run_conversion(dut, 0, label="target=0")


@cocotb.test()
async def test_conversion_63(dut):
    """Convert 63 (0b111111) — maximum value, all comparator responses 1."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)
    await run_conversion(dut, 63, label="target=63")


# ---------------------------------------------------------------------------
# Test: conv_done pulse width is exactly 1 cycle
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_conv_done_pulse_width(dut):
    """conv_done must be high for exactly 1 clock cycle, no more."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)

    seq, _ = get_comparator_seq(27)
    dut.comparator_in.value = seq[0]

    for i in range(6):
        await clk_edge(dut)
        if i < 5:
            dut.comparator_in.value = seq[i + 1]

    # After 6th edge: conv_done must be 1
    assert dut.conv_done.value == 1, "conv_done not high on done cycle"

    dut.comparator_in.value = seq[0]
    await clk_edge(dut)  # state 6 → 0

    assert dut.conv_done.value == 0, "conv_done did not drop after 1 cycle"

    # One more cycle to be sure it stays low
    await clk_edge(dut)
    assert dut.conv_done.value == 0, "conv_done spuriously reasserted"

    dut._log.info("conv_done pulse width = exactly 1 cycle ✓")


# ---------------------------------------------------------------------------
# Test: automatic restart — two back-to-back conversions
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_auto_restart(dut):
    """After conv_done, the FSM restarts and produces a correct second conversion."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)

    # First conversion: target = 17
    await run_conversion(dut, 17, label="conv1 target=17")

    # The FSM is now in state 0 of the next conversion.
    # Run a second full conversion: target = 50
    await run_conversion(dut, 50, label="conv2 target=50")

    dut._log.info("Auto-restart: two consecutive conversions succeeded ✓")


# ---------------------------------------------------------------------------
# Test: dac_bits trial sequence correctness (target = 42)
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_dac_bits_sequence(dut):
    """
    Verify dac_bits follows the expected SAR trial pattern for target=42.

    Expected dac_bits AFTER each clock edge settles:
      edge 0 (state 0→1): 110000 (48)   — keep bit5, try bit4
      edge 1 (state 1→2): 101000 (40)   — clear bit4, try bit3
      edge 2 (state 2→3): 101100 (44)   — keep bit3, try bit2
      edge 3 (state 3→4): 101010 (42)   — clear bit2, try bit1
      edge 4 (state 4→5): 101011 (43)   — keep bit1, try bit0
      edge 5 (state 5→6): 100000 (32)   — done; reset MSB for restart
    """
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())  # 20 kHz
    await reset_dut(dut)

    target = 42
    seq, _ = get_comparator_seq(target)

    # Verify initial state after reset: dac_bits = 100000
    assert int(dut.dac_bits.value) == 0b100000, (
        f"Initial dac_bits={int(dut.dac_bits.value):06b}, expected 100000"
    )

    expected_dac = [
        0b110000,   # edge 0
        0b101000,   # edge 1
        0b101100,   # edge 2
        0b101010,   # edge 3
        0b101011,   # edge 4
        0b100000,   # edge 5 (restart)
    ]

    dut.comparator_in.value = seq[0]

    for i in range(6):
        await clk_edge(dut)
        if i < 5:
            dut.comparator_in.value = seq[i + 1]

        got = int(dut.dac_bits.value)
        exp = expected_dac[i]
        assert got == exp, (
            f"After edge {i}: dac_bits={got:06b} ({got}), "
            f"expected={exp:06b} ({exp})"
        )
        dut._log.info(f"Edge {i}: dac_bits={got:06b} ✓")
