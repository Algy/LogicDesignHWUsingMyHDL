module tb_CPLD3;

reg clk;
reg rst;
reg [4:0] left_in2;
reg [4:0] sel;
wire [3:0] sel_out2;
wire [4:0] right_out2;
reg [2:0] pos_c;
wire last_row;

initial begin
    $from_myhdl(
        clk,
        rst,
        left_in2,
        sel,
        pos_c
    );
    $to_myhdl(
        sel_out2,
        right_out2,
        last_row
    );
end

CPLD3 dut(
    clk,
    rst,
    left_in2,
    sel,
    sel_out2,
    right_out2,
    pos_c,
    last_row
);

endmodule
