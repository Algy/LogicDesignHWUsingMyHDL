module tb_displaySeperate;

reg clk;
wire [4:0] left_in;
reg [4:0] right_out2;
reg fastClk;
reg leftbutton;
reg resetbutton;
reg rightbutton;
wire [2:0] pos_c;
wire [2:0] disp_col;

initial begin
    $from_myhdl(
        clk,
        right_out2,
        fastClk,
        leftbutton,
        resetbutton,
        rightbutton
    );
    $to_myhdl(
        left_in,
        pos_c,
        disp_col
    );
end

displaySeperate dut(
    clk,
    left_in,
    right_out2,
    fastClk,
    leftbutton,
    resetbutton,
    rightbutton,
    pos_c,
    disp_col
);

endmodule
