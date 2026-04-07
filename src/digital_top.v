`timescale 1ns/1ps
/*
 * digital_top.v — Digital integration top-level
 *
 * Instantiates and connects all 5 digital sub-blocks:
 *   sar_fsm → threshold_det → refractory_ctr → spike_counter → output_mux
 *
 * comparator_in and dac_bits are the analog-digital boundary.
 * They are Verilog ports here but physically connected in the Magic layout.
 */

`default_nettype none

module digital_top (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       comparator_in,  // from analog comparator
    input  wire [5:0] threshold,      // spike detection threshold (ui_in[7:2])
    input  wire       mode_select,    // output mode: 0=ADC, 1=spike count (uio_in[0])
    output wire [5:0] dac_bits,       // trial voltage to cap DAC switches
    output wire [7:0] data_out,       // uo_out[7:0]
    output wire       spike_valid     // spike event pulse (uio_out[1])
);

    // --- Internal wires ---
    wire [5:0] adc_result;
    wire       conv_done;   // not used externally; sar_fsm output must be connected
    wire       spike;
    wire [7:0] count;

    // --- SAR control FSM ---
    sar_fsm u_sar_fsm (
        .clk          (clk),
        .rst_n        (rst_n),
        .comparator_in(comparator_in),
        .dac_bits     (dac_bits),
        .adc_result   (adc_result),
        .conv_done    (conv_done)
    );

    // --- Threshold detector ---
    threshold_det u_threshold_det (
        .adc_result(adc_result),
        .threshold (threshold),
        .spike     (spike)
    );

    // --- Refractory counter ---
    refractory_ctr u_refractory_ctr (
        .clk        (clk),
        .rst_n      (rst_n),
        .spike_in   (spike),
        .spike_valid(spike_valid)
    );

    // --- Spike counter ---
    spike_counter u_spike_counter (
        .clk        (clk),
        .rst_n      (rst_n),
        .spike_valid(spike_valid),
        .count      (count)
    );

    // --- Output mux ---
    output_mux u_output_mux (
        .adc_result  (adc_result),
        .spike_count (count),
        .mode_select (mode_select),
        .data_out    (data_out)
    );

endmodule
