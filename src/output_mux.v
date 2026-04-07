`timescale 1ns/1ps
/*
 * output_mux.v — Output mode selector
 *
 * Purely combinational. Selects what appears on uo_out[7:0]:
 *   mode_select = 0  →  raw 6-bit ADC result, zero-padded to 8 bits
 *   mode_select = 1  →  8-bit spike count
 */

`default_nettype none

module output_mux (
    input  wire [5:0] adc_result,   // from sar_fsm
    input  wire [7:0] spike_count,  // from spike_counter
    input  wire       mode_select,  // 0 = ADC mode, 1 = spike count mode
    output wire [7:0] data_out      // to uo_out[7:0]
);

    assign data_out = mode_select ? spike_count : {2'b00, adc_result};

endmodule
