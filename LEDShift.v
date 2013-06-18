// File: LEDShift.v
// Generated by MyHDL 0.8
// Date: Tue Jun 18 10:15:56 2013


`timescale 1ns/10ps

module LEDShift (
    clk,
    rst,
    i,
    sel,
    sel_out,
    right_out
);


input clk;
input rst;
input [4:0] i;
input [4:0] sel;
output [3:0] sel_out;
reg [3:0] sel_out;
output [4:0] right_out;
wire [4:0] right_out;

reg [3:0] a;
reg [3:0] c;
reg [3:0] b;
reg [3:0] e;
reg [3:0] d;





always @(posedge clk, posedge rst) begin: LEDSHIFT_SHIFTER
    if (rst == 1) begin
        a <= 0;
        c <= 0;
        b <= 0;
        e <= 0;
        d <= 0;
    end
    else begin
        a[4-1:1] <= a[3-1:0];
        a[0] <= i[0];
        b[4-1:1] <= b[3-1:0];
        b[0] <= i[1];
        c[4-1:1] <= c[3-1:0];
        c[0] <= i[2];
        d[4-1:1] <= d[3-1:0];
        d[0] <= i[3];
        e[4-1:1] <= e[3-1:0];
        e[0] <= i[4];
    end
end


always @(a, c, b, e, d, sel) begin: LEDSHIFT_SELECTOR
    case (sel)
        'h0: begin
            sel_out = a;
        end
        'h1: begin
            sel_out = b;
        end
        'h2: begin
            sel_out = c;
        end
        'h3: begin
            sel_out = d;
        end
        'h4: begin
            sel_out = e;
        end
    endcase
end



assign right_out = {e[3], d[3], c[3], b[3], a[3]};

endmodule