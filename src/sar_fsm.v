`timescale 1ns/1ps
/*
 * sar_fsm.v — 6-bit Successive Approximation Register FSM
 *
 * Drives the capacitor DAC and samples the analog comparator to produce
 * a 6-bit ADC result in 6 clock cycles, then pulses conv_done for 1 cycle.
 * Automatically restarts the next conversion after conv_done.
 *
 * Timing (7 cycles per conversion):
 *   States 0–5: conversion cycles, MSB (bit 5) first down to LSB (bit 0)
 *   State 6:    conv_done=1, adc_result valid; then restart to state 0
 *
 * comparator_in: 1 = Vin >= DAC trial voltage (keep the bit)
 *                0 = Vin <  DAC trial voltage (clear the bit)
 */

`default_nettype none

module sar_fsm (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       comparator_in,
    output reg  [5:0] dac_bits,    // current DAC trial value
    output reg  [5:0] adc_result,  // latched conversion result
    output reg        conv_done    // pulses high for exactly 1 clock cycle
);

    reg [2:0] state;
    reg [5:0] result;  // accumulates decided bits across the 6 cycles

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= 3'd0;
            result     <= 6'd0;
            dac_bits   <= 6'b100000;  // MSB trial ready immediately
            adc_result <= 6'd0;
            conv_done  <= 1'b0;
        end else begin
            conv_done <= 1'b0;  // default: deassert each cycle

            case (state)
                // --- Conversion cycles ---
                // Each state samples comparator_in for the current trial bit,
                // updates result, and sets dac_bits for the next trial.
                // dac_bits = {bits decided so far} | {next trial bit = 1}.
                // Note: result[N] below is its OLD value (set in a prior cycle),
                // which is correct because non-blocking assigns don't update
                // result until the end of this clock edge.

                3'd0: begin  // trial bit 5
                    result[5] <= comparator_in;
                    dac_bits  <= {comparator_in, 1'b1, 4'b0};
                    state     <= 3'd1;
                end

                3'd1: begin  // trial bit 4
                    result[4] <= comparator_in;
                    dac_bits  <= {result[5], comparator_in, 1'b1, 3'b0};
                    state     <= 3'd2;
                end

                3'd2: begin  // trial bit 3
                    result[3] <= comparator_in;
                    dac_bits  <= {result[5:4], comparator_in, 1'b1, 2'b0};
                    state     <= 3'd3;
                end

                3'd3: begin  // trial bit 2
                    result[2] <= comparator_in;
                    dac_bits  <= {result[5:3], comparator_in, 1'b1, 1'b0};
                    state     <= 3'd4;
                end

                3'd4: begin  // trial bit 1
                    result[1] <= comparator_in;
                    dac_bits  <= {result[5:2], comparator_in, 1'b1};
                    state     <= 3'd5;
                end

                3'd5: begin  // trial bit 0 (last bit)
                    result[0]  <= comparator_in;
                    adc_result <= {result[5:1], comparator_in};  // latch final result
                    conv_done  <= 1'b1;
                    dac_bits   <= 6'b100000;  // prep MSB trial for next conversion
                    state      <= 3'd6;
                end

                // --- Done / restart ---
                3'd6: begin
                    result   <= 6'd0;
                    state    <= 3'd0;
                    // conv_done already deasserted by default above
                    // dac_bits already 6'b100000 from state 5
                end

                default: begin
                    state    <= 3'd0;
                    result   <= 6'd0;
                    dac_bits <= 6'b100000;
                end
            endcase
        end
    end

endmodule
