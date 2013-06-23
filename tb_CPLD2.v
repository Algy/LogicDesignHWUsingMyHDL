module tb_CPLD2;

reg clk;
reg rst;
reg [4:0] left_in;
reg [2:0] sel;
wire [3:0] sel_out;
wire [4:0] right_out;
wire [4:0] sel_decoded;

initial begin
    $from_myhdl(
        clk,
        rst,
        left_in,
        sel
    );
    $to_myhdl(
        sel_out,
        right_out,
        sel_decoded
    );
end

CPLD2 dut(
    clk,
    rst,
    left_in,
    sel,
    sel_out,
    right_out,
    sel_decoded
);

endmodule
