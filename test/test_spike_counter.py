"""
test_spike_counter.py — cocotb testbench for spike_counter

spike_counter increments an 8-bit counter on every spike_valid pulse.
Wraps from 255 to 0 naturally. Holds when spike_valid=0.

Tests:
  1. Count N spikes and verify count == N
  2. Rollover: fill to 255, one more spike → count = 0
  3. Count holds when spike_valid=0
  4. Reset clears count mid-sequence
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def clk_edge(dut):
    """Await one rising edge, then let NBAs settle."""
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


async def reset_dut(dut):
    """Apply active-low reset for 2 clock cycles then release."""
    dut.rst_n.value = 0
    dut.spike_valid.value = 0
    await clk_edge(dut)
    await clk_edge(dut)
    dut.rst_n.value = 1
    await Timer(1, units="ns")


async def send_spikes(dut, n):
    """Send n single-cycle spike_valid pulses."""
    for _ in range(n):
        dut.spike_valid.value = 1
        await clk_edge(dut)
        dut.spike_valid.value = 0
        await clk_edge(dut)


# ---------------------------------------------------------------------------
# Test 1: count N spikes
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_count_spikes(dut):
    """Send 10 spikes and verify count reaches 10."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    assert dut.count.value == 0, "count not 0 after reset"

    for n in range(1, 11):
        dut.spike_valid.value = 1
        await clk_edge(dut)
        dut.spike_valid.value = 0
        assert dut.count.value == n, (
            f"count={int(dut.count.value)} after {n} spikes, expected {n}"
        )
        await clk_edge(dut)

    dut._log.info("Count 10 spikes test passed ✓")


# ---------------------------------------------------------------------------
# Test 2: rollover at 255
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_rollover(dut):
    """Count to 255, send one more spike, verify count wraps to 0."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Fast-fill to 255: hold spike_valid high for 255 consecutive cycles
    for _ in range(255):
        dut.spike_valid.value = 1
        await clk_edge(dut)

    dut.spike_valid.value = 0
    assert dut.count.value == 255, (
        f"count={int(dut.count.value)}, expected 255 before rollover"
    )

    # One more spike → should wrap to 0
    dut.spike_valid.value = 1
    await clk_edge(dut)
    dut.spike_valid.value = 0

    assert dut.count.value == 0, (
        f"count={int(dut.count.value)} after rollover, expected 0"
    )
    dut._log.info("Rollover 255→0 test passed ✓")


# ---------------------------------------------------------------------------
# Test 3: count holds when spike_valid=0
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_count_holds(dut):
    """count must not change when spike_valid stays low."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Send 5 spikes to get a non-zero count
    await send_spikes(dut, 5)
    assert dut.count.value == 5, f"count={int(dut.count.value)}, expected 5"

    # Hold spike_valid low for 10 cycles — count must stay at 5
    dut.spike_valid.value = 0
    for cycle in range(10):
        await clk_edge(dut)
        assert dut.count.value == 5, (
            f"count changed to {int(dut.count.value)} at idle cycle {cycle}"
        )

    dut._log.info("Count holds at idle test passed ✓")


# ---------------------------------------------------------------------------
# Test 4: reset clears count mid-sequence
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_reset_clears(dut):
    """Reset during counting clears count to 0."""
    cocotb.start_soon(Clock(dut.clk, 1000, units="ns").start())
    await reset_dut(dut)

    # Count up to 20
    await send_spikes(dut, 20)
    assert dut.count.value == 20, f"count={int(dut.count.value)}, expected 20"

    # Assert reset
    dut.rst_n.value = 0
    await clk_edge(dut)
    assert dut.count.value == 0, (
        f"count={int(dut.count.value)} during reset, expected 0"
    )

    # Release reset and confirm count stays 0
    dut.rst_n.value = 1
    await clk_edge(dut)
    assert dut.count.value == 0, (
        f"count={int(dut.count.value)} after reset release, expected 0"
    )

    dut._log.info("Reset clears count test passed ✓")
