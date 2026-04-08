"""
test_digital_top.py — cocotb integration testbench for digital_top

Drives the full pipeline end-to-end:
  comparator_in → sar_fsm → threshold_det → refractory_ctr
                                           → spike_counter → output_mux → data_out

Pipeline latency (after adc_result is latched in state 5):
  +1 edge: refractory_ctr clocks spike_in → spike_valid goes high
  +1 edge: spike_counter clocks spike_valid → count increments

So after run_conversion (which ends in FSM state 0), one more edge is needed
before checking count. This extra edge puts the FSM in state 1.

To re-enter state 0 before the next run_conversion, wait_refractory() waits
exactly 1504 cycles = 214×7 + 6, which satisfies:
  (1 + 1504) % 7 == 0   → returns to state 0
  1504 > 1500           → refractory counter (1500) fully drained

Tests:
  1. ADC mode: drive a known conversion, verify data_out shows correct ADC value
  2. Threshold: adc_result below threshold → no spike; at/above → spike
  3. Spike count: three conversions above threshold, count increments each time
  4. Refractory: two conversions back-to-back, second spike blocked
  5. Mode switch: same state, toggle mode_select, verify data_out changes
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REFRACTORY_CYCLES = 1500  # must match refractory_ctr default parameter (75ms @ 20kHz)

async def clk_edge(dut):
    """Await one rising edge, then let NBAs settle."""
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


async def reset_dut(dut):
    """Apply active-low reset for 2 cycles, then release. FSM ends in state 0."""
    dut.rst_n.value         = 0
    dut.comparator_in.value = 0
    dut.threshold.value     = 0
    dut.mode_select.value   = 0
    await clk_edge(dut)
    await clk_edge(dut)
    dut.rst_n.value = 1
    await Timer(1, units="ns")


def get_comparator_seq(target):
    """
    Compute the 6-element comparator response sequence for a SAR conversion.
    Returns (seq, recovered_value).
    """
    seq, dac = [], 0
    for bit in range(5, -1, -1):
        trial = dac | (1 << bit)
        cmp = 1 if target >= trial else 0
        seq.append(cmp)
        if cmp:
            dac = trial
    return seq, dac


async def run_conversion(dut, target):
    """
    Drive one full 6-cycle SAR conversion for the given target, then one
    restart edge (state 6→0).  FSM ends in state 0.

    Does NOT wait for the spike pipeline to propagate — call
    await_spike_pipeline() afterwards if you need to read count.
    """
    seq, expected = get_comparator_seq(target)
    dut.comparator_in.value = seq[0]

    for i in range(6):
        await clk_edge(dut)        # edges 0-5: states 0→1→…→5→6
        if i < 5:
            dut.comparator_in.value = seq[i + 1]

    # State 6: conv_done=1, adc_result valid, spike asserted (combinational)
    # One more edge: state 6→0 — refractory_ctr clocks, spike_valid goes high
    dut.comparator_in.value = 0
    await clk_edge(dut)
    # FSM now in state 0. spike_valid=1 (if spike fired). count not yet updated.
    return expected


async def await_spike_pipeline(dut):
    """
    One additional edge so spike_counter clocks spike_valid → count updates.
    After this call the FSM is in state 1.
    """
    await clk_edge(dut)


async def wait_refractory(dut):
    """
    Wait 1504 cycles (= 214×7 + 6) with comparator_in=0.

    1504 satisfies two constraints:
      (1 + 1504) % 7 == 0   → returns FSM from state 1 to state 0
      1504 > 1500           → refractory counter (1500 − 2 already elapsed) drains to 0
    """
    dut.comparator_in.value = 0
    for _ in range(1504):
        await clk_edge(dut)


async def align_to_state0(dut):
    """
    Advance 6 edges (from state 1 → state 0) with comparator_in=0.
    Used when we need state 0 but cannot wait a full refractory period.
    """
    dut.comparator_in.value = 0
    for _ in range(6):
        await clk_edge(dut)


# ---------------------------------------------------------------------------
# Test 1: ADC mode — verify data_out shows the converted value
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_adc_mode_output(dut):
    """ADC mode: data_out[5:0] == adc_result after conversion, upper bits = 0."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())
    await reset_dut(dut)

    dut.mode_select.value = 0   # ADC mode
    dut.threshold.value   = 63  # max threshold — no spikes, no refractory needed

    for target in [0, 42, 63, 17, 55]:
        expected = await run_conversion(dut, target)
        # adc_result is a register — no extra pipeline edge needed for ADC mode
        got = int(dut.data_out.value)
        assert got == expected, (
            f"target={target}: data_out={got}, expected={expected}"
        )
        assert (got >> 6) == 0, f"upper 2 bits not zero: data_out={got:#04x}"
        dut._log.info(f"ADC mode target={target} → data_out={got} ✓")

    dut._log.info("ADC mode output test passed ✓")


# ---------------------------------------------------------------------------
# Test 2: threshold crossing
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_threshold_crossing(dut):
    """Spike fires for adc_result >= threshold, not for adc_result < threshold."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())
    await reset_dut(dut)

    dut.threshold.value   = 32
    dut.mode_select.value = 1   # spike count mode to observe count changes

    # --- Below threshold: target=20 → no spike ---
    count_before = int(dut.data_out.value)
    await run_conversion(dut, 20)
    await await_spike_pipeline(dut)     # FSM now state 1
    count_after = int(dut.data_out.value)
    assert count_after == count_before, (
        f"Spike fired below threshold: count {count_before}→{count_after}"
    )
    dut._log.info("Below threshold: no spike ✓")

    await wait_refractory(dut)          # FSM back to state 0

    # --- At threshold: target=32 → spike ---
    count_before = int(dut.data_out.value)
    await run_conversion(dut, 32)
    await await_spike_pipeline(dut)     # FSM now state 1
    count_after = int(dut.data_out.value)
    assert count_after == count_before + 1, (
        f"Spike not fired at threshold: count {count_before}→{count_after}"
    )
    dut._log.info("At threshold: spike fired ✓")

    await wait_refractory(dut)          # FSM back to state 0

    # --- Above threshold: target=50 → spike ---
    count_before = int(dut.data_out.value)
    await run_conversion(dut, 50)
    await await_spike_pipeline(dut)     # FSM now state 1
    count_after = int(dut.data_out.value)
    assert count_after == count_before + 1, (
        f"Spike not fired above threshold: count {count_before}→{count_after}"
    )
    dut._log.info("Above threshold: spike fired ✓")

    dut._log.info("Threshold crossing test passed ✓")


# ---------------------------------------------------------------------------
# Test 3: spike count increments across multiple conversions
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_spike_count_increments(dut):
    """Three above-threshold conversions increment spike count by 1 each."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())
    await reset_dut(dut)

    dut.threshold.value   = 10   # low threshold — easy to cross
    dut.mode_select.value = 1

    for expected_count in range(1, 4):
        await run_conversion(dut, 63)
        await await_spike_pipeline(dut)         # FSM state 1, count updated
        got = int(dut.data_out.value)
        assert got == expected_count, (
            f"After conversion {expected_count}: count={got}, expected={expected_count}"
        )
        dut._log.info(f"Spike count={got} ✓")
        await wait_refractory(dut)              # FSM back to state 0

    dut._log.info("Spike count increment test passed ✓")


# ---------------------------------------------------------------------------
# Test 4: refractory blocks back-to-back spikes
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_refractory_blocks(dut):
    """Two above-threshold conversions back-to-back: only first increments count."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())
    await reset_dut(dut)

    dut.threshold.value   = 10
    dut.mode_select.value = 1

    # First conversion — accepted
    await run_conversion(dut, 63)
    await await_spike_pipeline(dut)     # FSM state 1, count=1
    assert int(dut.data_out.value) == 1, (
        f"First spike not counted: count={int(dut.data_out.value)}"
    )
    dut._log.info("First spike counted ✓")

    # Realign to state 0 (6 edges) — refractory still very much active
    await align_to_state0(dut)          # FSM state 0

    # Second conversion immediately — refractory still active, should be blocked
    await run_conversion(dut, 63)
    await await_spike_pipeline(dut)     # FSM state 1
    assert int(dut.data_out.value) == 1, (
        f"Second spike not blocked: count={int(dut.data_out.value)}, expected 1"
    )
    dut._log.info("Second spike blocked by refractory ✓")

    dut._log.info("Refractory blocking test passed ✓")


# ---------------------------------------------------------------------------
# Test 5: mode switch changes data_out between ADC value and spike count
# ---------------------------------------------------------------------------

@cocotb.test()
async def test_mode_switch(dut):
    """Toggling mode_select switches data_out between ADC value and spike count."""
    cocotb.start_soon(Clock(dut.clk, 50, units="us").start())
    await reset_dut(dut)

    dut.threshold.value   = 10
    dut.mode_select.value = 1   # spike count mode

    # First conversion — spike fires, count=1
    await run_conversion(dut, 63)
    await await_spike_pipeline(dut)     # FSM state 1, count=1
    await wait_refractory(dut)          # FSM state 0

    # Second conversion — spike fires, count=2; also records adc_result=42
    target = 42
    expected_adc = await run_conversion(dut, target)
    await await_spike_pipeline(dut)     # FSM state 1, count=2

    # Spike count mode: data_out should be 2
    dut.mode_select.value = 1
    await Timer(1, units="ns")
    count_out = int(dut.data_out.value)
    assert count_out == 2, f"Spike count mode: data_out={count_out}, expected 2"
    dut._log.info(f"Spike count mode: data_out={count_out} ✓")

    # ADC mode: data_out should be the last adc_result (42)
    dut.mode_select.value = 0
    await Timer(1, units="ns")
    adc_out = int(dut.data_out.value)
    assert adc_out == expected_adc, (
        f"ADC mode: data_out={adc_out}, expected={expected_adc}"
    )
    dut._log.info(f"ADC mode: data_out={adc_out} ✓")

    dut._log.info("Mode switch test passed ✓")
