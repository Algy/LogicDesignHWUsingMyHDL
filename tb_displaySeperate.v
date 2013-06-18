module tb_displaySeperate;

reg clk;
wire [4:0] left_in;
reg [4:0] right_out2;
reg [3:0] sel_out;
reg [3:0] sel_out2;
reg fastClk;
reg leftbutton;
reg resetbutton;
reg rightbutton;
wire [7:0] rows;
wire [2:0] col_sel;

initial begin
    $from_myhdl(
        clk,
        right_out2,
        sel_out,
        sel_out2,
        fastClk,
        leftbutton,
        resetbutton,
        rightbutton
    );
    $to_myhdl(
        left_in,
        rows,
        col_sel
    );
end

displaySeperate dut(
    clk,
    left_in,
    right_out2,
    sel_out,
    sel_out2,
    fastClk,
    leftbutton,
    resetbutton,
    rightbutton,
    rows,
    col_sel
);

endmodule
