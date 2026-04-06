`timescale 1ns/1ps
/*
 * refractory_ctr.v — Refractory period counter
 *
 * Enforces a dead-time after each valid spike. Once spike_in is accepted,
 * spike_valid pulses high for exactly 1 clock cycle, then the output is
 * blocked for REFRACTORY_CYCLES cycles before the next spike can pass.
 *
 * spike_valid = 1  →  spike accepted (counter was 0, spike_in=1)
 * spike_valid = 0  →  either idle or in refractory period
 */

`default_nettype none

module refractory_ctr #(
    parameter REFRACTORY_CYCLES = 100
) (
    input  wire clk,
    input  wire rst_n,
    input  wire spike_in,    // raw spike from threshold_det
    output reg  spike_valid  // gated spike: high for exactly 1 cycle per accepted spike
);

    reg [7:0] counter;  // counts down from REFRACTORY_CYCLES to 0

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter     <= 8'd0;
            spike_valid <= 1'b0;
        end else begin
            spike_valid <= 1'b0;  // default: deassert every cycle

            if (counter > 0) begin
                counter <= counter - 8'd1;
            end else if (spike_in) begin
                spike_valid <= 1'b1;
                counter     <= REFRACTORY_CYCLES[7:0];
            end
        end
    end

endmodule
