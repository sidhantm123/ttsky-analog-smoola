`timescale 1ns/1ps
/*
 * threshold_det.v — Spike threshold detector
 *
 * Purely combinational. Asserts spike when the ADC result meets or
 * exceeds the programmed threshold (ui_in[7:2] in the top level).
 *
 * spike = 1  →  adc_result >= threshold  (spike detected)
 * spike = 0  →  adc_result <  threshold  (no spike)
 */

`default_nettype none

module threshold_det (
    input  wire [5:0] adc_result,
    input  wire [5:0] threshold,
    output wire       spike
);

    assign spike = (adc_result >= threshold);

endmodule
