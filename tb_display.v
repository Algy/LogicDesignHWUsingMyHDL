module tb_display;

reg clk;
reg fastClk;
reg leftbutton;
reg resetbutton;
reg rightbutton;
wire [7:0] rows;
wire [2:0] col_sel;

initial begin
    $from_myhdl(
        clk,
        fastClk,
        leftbutton,
        resetbutton,
        rightbutton
    );
    $to_myhdl(
        rows,
        col_sel
    );
end

display dut(
    clk,
    fastClk,
    leftbutton,
    resetbutton,
    rightbutton,
    rows,
    col_sel
);

endmodule
