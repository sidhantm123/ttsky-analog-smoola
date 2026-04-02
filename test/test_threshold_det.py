"""
test_threshold_det.py — cocotb testbench for threshold_det

threshold_det is purely combinational: spike = (adc_result >= threshold).
No clock required — each test just drives inputs and reads outputs after
a 1 ns settle delay.

Tests:
  1. Exhaustive sweep: all 64 ADC values vs threshold=32 (mid-range)
  2. Boundary threshold=0: spike must always be high (0 >= 0 is true)
  3. Boundary threshold=63: spike high only at adc_result=63
  4. Spot-check several thresholds across the range
"""

import cocotb
from cocotb.triggers import Timer


async def check(dut, adc, thresh):
    """Drive inputs, settle 1 ns, assert spike matches expectation."""
    dut.adc_result.value = adc
    dut.threshold.value = thresh
    await Timer(1, units="ns")
    expected = 1 if adc >= thresh else 0
    assert dut.spike.value == expected, (
        f"adc={adc} thresh={thresh}: spike={int(dut.spike.value)}, expected={expected}"
    )


# ---------------------------------------------------------------------------
# Test 1: exhaustive sweep at threshold=32
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_sweep_threshold_32(dut):
    """All 64 ADC values against threshold=32 — checks both sides of boundary."""
    thresh = 32
    for adc in range(64):
        await check(dut, adc, thresh)
    dut._log.info("Exhaustive sweep at threshold=32 passed ✓")


# ---------------------------------------------------------------------------
# Test 2: threshold=0 → spike always high
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_threshold_zero(dut):
    """threshold=0: every ADC value should assert spike (anything >= 0)."""
    for adc in range(64):
        await check(dut, adc, 0)
    dut._log.info("threshold=0 always-high test passed ✓")


# ---------------------------------------------------------------------------
# Test 3: threshold=63 → spike only at adc_result=63
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_threshold_max(dut):
    """threshold=63: only adc_result=63 should assert spike."""
    for adc in range(64):
        await check(dut, adc, 63)
    dut._log.info("threshold=63 single-hit test passed ✓")


# ---------------------------------------------------------------------------
# Test 4: spot-check several thresholds, focusing on the boundary value
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_boundary_values(dut):
    """
    For several thresholds, verify that:
      adc_result = threshold - 1  →  spike = 0  (just below)
      adc_result = threshold      →  spike = 1  (exactly at)
      adc_result = threshold + 1  →  spike = 1  (just above)
    """
    for thresh in [1, 10, 25, 32, 50, 62]:
        if thresh > 0:
            await check(dut, thresh - 1, thresh)   # just below → no spike
        await check(dut, thresh, thresh)            # exactly at → spike
        if thresh < 63:
            await check(dut, thresh + 1, thresh)   # just above → spike

    dut._log.info("Boundary value tests passed ✓")
