/*
 * Copyright (c) 2024 Sidhant Moola
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_sidhantm123_neural_adc (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    inout  wire [7:0] ua,       // Analog pins, only ua[5:0] can be used
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // uio[0] is an input (mode_select), uio[1] is an output (spike_valid).
    // uio_oe bits: 1 = output, 0 = input.
    assign uio_oe = 8'b00000010;  // only uio[1] is driven by us

    // uio[2:7] unused — drive low
    assign uio_out[7:2] = 6'b0;
    assign uio_out[0]   = 1'b0;   // uio[0] is input (mode_select), do not drive

    // comparator_in and dac_bits are the analog-digital boundary.
    // In the final chip these connect to the analog comparator output and
    // cap DAC switch controls via metal routing in the Magic layout.
    // For Verilog/hardening purposes they are left unconnected here —
    // the actual wires are made in Magic at tape-out time.
    wire       comparator_in;   // from analog comparator (unconnected in RTL)
    assign comparator_in = 1'b0;  // RTL stub for hardening; overridden by analog routing in Magic layout
    wire [5:0] dac_bits;        // to cap DAC switches (unconnected in RTL)

    digital_top u_digital_top (
        .clk         (clk),
        .rst_n       (rst_n),
        .comparator_in(comparator_in),
        .threshold   (ui_in[7:2]),
        .mode_select (uio_in[0]),
        .dac_bits    (dac_bits),
        .data_out    (uo_out),
        .spike_valid (uio_out[1])
    );

endmodule
