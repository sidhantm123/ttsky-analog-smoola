"""
test_output_mux.py — cocotb testbench for output_mux

output_mux is purely combinational. No clock needed.
Uses Timer(1, units="ns") after each input change to let signals settle.

Tests:
  1. ADC mode (mode_select=0): data_out = {2'b00, adc_result}
  2. Spike count mode (mode_select=1): data_out = spike_count
  3. ADC zero-padding: data_out[7:6] always 0 in ADC mode
  4. Mode switch updates output immediately
"""

import cocotb
from cocotb.triggers import Timer


async def drive(dut, adc=0, count=0, mode=0):
    """Drive all inputs and settle for 1 ns."""
    dut.adc_result.value  = adc
    dut.spike_count.value = count
    dut.mode_select.value = mode
    await Timer(1, units="ns")


# ---------------------------------------------------------------------------
# Test 1: ADC mode — all 64 ADC values, verify zero-padding
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_adc_mode(dut):
    """mode_select=0: data_out = {2'b00, adc_result} for all 64 values."""
    for adc in range(64):
        await drive(dut, adc=adc, count=0xFF, mode=0)
        expected = adc  # upper 2 bits are 0
        got = int(dut.data_out.value)
        assert got == expected, (
            f"adc_mode adc={adc}: data_out={got:#04x}, expected={expected:#04x}"
        )
        assert (got >> 6) == 0, (
            f"adc_mode adc={adc}: upper 2 bits not zero, data_out={got:#04x}"
        )

    dut._log.info("ADC mode test passed ✓")


# ---------------------------------------------------------------------------
# Test 2: spike count mode — all 256 count values
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_spike_count_mode(dut):
    """mode_select=1: data_out = spike_count for all 256 values."""
    for count in range(256):
        await drive(dut, adc=0x3F, count=count, mode=1)
        got = int(dut.data_out.value)
        assert got == count, (
            f"count_mode count={count}: data_out={got}, expected={count}"
        )

    dut._log.info("Spike count mode test passed ✓")


# ---------------------------------------------------------------------------
# Test 3: mode switch updates output immediately
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_mode_switch(dut):
    """Switching mode_select immediately changes data_out."""
    adc   = 0b101010   # 42
    count = 0b11001100  # 204

    # Start in ADC mode
    await drive(dut, adc=adc, count=count, mode=0)
    assert int(dut.data_out.value) == adc, "ADC mode: wrong output"

    # Switch to spike count mode — same inputs, just change mode
    dut.mode_select.value = 1
    await Timer(1, units="ns")
    assert int(dut.data_out.value) == count, "Count mode: wrong output after switch"

    # Switch back to ADC mode
    dut.mode_select.value = 0
    await Timer(1, units="ns")
    assert int(dut.data_out.value) == adc, "ADC mode: wrong output after switch back"

    dut._log.info("Mode switch test passed ✓")


# ---------------------------------------------------------------------------
# Test 4: spot-check several adc+count combinations in both modes
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_spot_checks(dut):
    """Spot-check several values in both modes simultaneously."""
    cases = [
        (0,  0,   0,   0),    # adc=0, count=0, adc_mode=0, count_mode=0
        (63, 255, 63,  255),  # adc=63, count=255
        (32, 100, 32,  100),
        (1,  200, 1,   200),
        (0,  1,   0,   1),
    ]
    for adc, count, exp_adc_mode, exp_count_mode in cases:
        await drive(dut, adc=adc, count=count, mode=0)
        assert int(dut.data_out.value) == exp_adc_mode, (
            f"ADC mode: adc={adc} count={count} → {int(dut.data_out.value)}, expected {exp_adc_mode}"
        )
        await drive(dut, adc=adc, count=count, mode=1)
        assert int(dut.data_out.value) == exp_count_mode, (
            f"Count mode: adc={adc} count={count} → {int(dut.data_out.value)}, expected {exp_count_mode}"
        )

    dut._log.info("Spot-check test passed ✓")
