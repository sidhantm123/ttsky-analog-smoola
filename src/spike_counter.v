`timescale 1ns/1ps
/*
 * spike_counter.v — 8-bit spike event counter
 *
 * Increments on every spike_valid pulse from refractory_ctr.
 * Wraps naturally from 255 to 0 on overflow.
 */

`default_nettype none

module spike_counter (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       spike_valid,  // from refractory_ctr, 1-cycle pulse per spike
    output reg  [7:0] count         // running total, wraps at 255
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 8'd0;
        end else if (spike_valid) begin
            count <= count + 8'd1;
        end
    end

endmodule
