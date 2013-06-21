// File: CPLD3.v
// Generated by MyHDL 0.8
// Date: Fri Jun 21 19:13:59 2013


`timescale 1ns/10ps

module CPLD3 (
    clk,
    rst,
    left_in2,
    sel,
    sel_out2,
    right_out2,
    pos_c,
    last_row
);


input clk;
input rst;
input [4:0] left_in2;
input [4:0] sel;
output [3:0] sel_out2;
reg [3:0] sel_out2;
output [4:0] right_out2;
wire [4:0] right_out2;
input [2:0] pos_c;
output last_row;
reg last_row;

reg [3:0] a_a;
reg [3:0] a_c;
reg [3:0] a_b;
reg [3:0] a_e;
reg [3:0] a_d;





always @(posedge clk, posedge rst) begin: CPLD3_A_SHIFTER
    if (rst == 1) begin
        a_a <= 0;
        a_c <= 0;
        a_b <= 0;
        a_e <= 0;
        a_d <= 0;
    end
    else begin
        a_a[4-1:1] <= a_a[3-1:0];
        a_a[0] <= left_in2[0];
        a_b[4-1:1] <= a_b[3-1:0];
        a_b[0] <= left_in2[1];
        a_c[4-1:1] <= a_c[3-1:0];
        a_c[0] <= left_in2[2];
        a_d[4-1:1] <= a_d[3-1:0];
        a_d[0] <= left_in2[3];
        a_e[4-1:1] <= a_e[3-1:0];
        a_e[0] <= left_in2[4];
    end
end


always @(a_a, a_c, a_b, a_e, a_d, sel) begin: CPLD3_A_SELECTOR
    case (sel)
        'h0: begin
            sel_out2 = a_a;
        end
        'h1: begin
            sel_out2 = a_b;
        end
        'h2: begin
            sel_out2 = a_c;
        end
        'h3: begin
            sel_out2 = a_d;
        end
        'h4: begin
            sel_out2 = a_e;
        end
    endcase
end



assign right_out2 = {a_e[3], a_d[3], a_c[3], a_b[3], a_a[3]};


always @(pos_c, sel, sel_out2) begin: CPLD3_REPLACECHARACTOR
    if ((pos_c == sel)) begin
        last_row = 1;
    end
    else begin
        last_row = sel_out2[3];
    end
end

endmodule
