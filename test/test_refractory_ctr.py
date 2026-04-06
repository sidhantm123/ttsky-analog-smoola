"""
test_refractory_ctr.py — cocotb testbench for refractory_ctr

refractory_ctr gates spike_in with a countdown timer:
  - counter=0, spike_in=1  →  spike_valid=1 for 1 cycle, counter loads REFRACTORY_CYCLES
  - counter>0               →  spike_valid=0, counter decrements, spike_in ignored

Run with REFRACTORY_CYCLES overridden to 8 for fast simulation:
  make BLOCK=refractory_ctr SIM_ARGS="-P refractory_ctr.REFRACTORY_CYCLES=8"

Tests:
  1. Single spike passes through and spike_valid is exactly 1 cycle wide
  2. Second spike immediately after is blocked during refractory period
  3. Refractory period expires and next spike is accepted
  4. spike_valid pulse width is exactly 1 cycle (belt-and-suspenders check)
  5. No false spike when spike_in is low after reset
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

REFRACTORY_CYCLES = 8  # must match SIM_ARGS override


async def clk_edge(dut):
    """Await one rising edge, then let NBAs settle."""
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


async def reset_dut(dut):
    """Apply active-low reset for 2 clock cycles then release."""
    dut.rst_n.value = 0
    dut.spike_in.value = 0
    await clk_edge(dut)
    await clk_edge(dut)
    dut.rst_n.value = 1
    await Timer(1, units="ns")


# ---------------------------------------------------------------------------
# Test 1: single spike passes through, spike_valid is 1-cycle wide
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_single_spike(dut):
    """spike_in=1 for one cycle → spike_valid=1 for exactly that cycle."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Verify idle: spike_valid=0 with no input
    assert dut.spike_valid.value == 0, "spike_valid not 0 at idle after reset"

    # Drive spike for one cycle
    dut.spike_in.value = 1
    await clk_edge(dut)
    dut.spike_in.value = 0

    assert dut.spike_valid.value == 1, "spike_valid not 1 on accepted spike"

    # Next cycle: spike_valid must deassert
    await clk_edge(dut)
    assert dut.spike_valid.value == 0, "spike_valid did not drop after 1 cycle"

    dut._log.info("Single spike test passed ✓")


# ---------------------------------------------------------------------------
# Test 2: second spike immediately after is blocked
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_refractory_blocks_second_spike(dut):
    """spike_in held high during refractory period — all blocked."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Accept first spike
    dut.spike_in.value = 1
    await clk_edge(dut)
    assert dut.spike_valid.value == 1, "First spike not accepted"

    # Keep spike_in=1 during entire refractory window
    for cycle in range(REFRACTORY_CYCLES):
        await clk_edge(dut)
        assert dut.spike_valid.value == 0, (
            f"spike_valid spuriously high at refractory cycle {cycle}"
        )

    dut.spike_in.value = 0
    dut._log.info("Refractory blocking test passed ✓")


# ---------------------------------------------------------------------------
# Test 3: refractory expires → next spike accepted
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_refractory_expires(dut):
    """After REFRACTORY_CYCLES cycles, a new spike_in is accepted."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Accept first spike
    dut.spike_in.value = 1
    await clk_edge(dut)
    assert dut.spike_valid.value == 1, "First spike not accepted"
    dut.spike_in.value = 0

    # Wait for refractory to drain (REFRACTORY_CYCLES edges)
    for _ in range(REFRACTORY_CYCLES):
        await clk_edge(dut)

    # Now counter should be 0 — send a new spike
    dut.spike_in.value = 1
    await clk_edge(dut)
    assert dut.spike_valid.value == 1, (
        "Second spike not accepted after refractory period expired"
    )
    dut.spike_in.value = 0

    dut._log.info("Refractory expiry test passed ✓")


# ---------------------------------------------------------------------------
# Test 4: spike_valid pulse width is exactly 1 cycle
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_spike_valid_width(dut):
    """spike_valid must be high for exactly 1 cycle, low for all others."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    dut.spike_in.value = 1
    await clk_edge(dut)
    dut.spike_in.value = 0

    assert dut.spike_valid.value == 1, "spike_valid not high on accepted spike"

    await clk_edge(dut)
    assert dut.spike_valid.value == 0, "spike_valid not low at cycle +1"

    await clk_edge(dut)
    assert dut.spike_valid.value == 0, "spike_valid not low at cycle +2"

    dut._log.info("spike_valid pulse width = exactly 1 cycle ✓")


# ---------------------------------------------------------------------------
# Test 5: no false spike when spike_in is low after reset
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_no_false_spike_at_idle(dut):
    """With spike_in=0, spike_valid must stay 0 indefinitely."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    dut.spike_in.value = 0
    for cycle in range(20):
        await clk_edge(dut)
        assert dut.spike_valid.value == 0, (
            f"spike_valid spuriously high at idle cycle {cycle}"
        )

    dut._log.info("No false spike at idle test passed ✓")
