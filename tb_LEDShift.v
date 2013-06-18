module tb_LEDShift;

reg clk;
reg rst;
reg [4:0] i;
reg [4:0] sel;
wire [3:0] sel_out;
wire [4:0] right_out;

initial begin
    $from_myhdl(
        clk,
        rst,
        i,
        sel
    );
    $to_myhdl(
        sel_out,
        right_out
    );
end

LEDShift dut(
    clk,
    rst,
    i,
    sel,
    sel_out,
    right_out
);

endmodule
