// File: display.v
// Generated by MyHDL 0.8
// Date: Tue Jun 18 08:41:55 2013


`timescale 1ns/10ps

module display (
    clk,
    fastClk,
    leftbutton,
    resetbutton,
    rightbutton,
    rows,
    col_sel
);


input clk;
input fastClk;
input leftbutton;
input resetbutton;
input rightbutton;
output [7:0] rows;
reg [7:0] rows;
output [2:0] col_sel;
reg [2:0] col_sel;

reg [4:0] left_in;
wire [4:0] right_out2;
reg [3:0] sel_out2;
reg isThereCollision;
reg [2:0] disp_col;
reg [0:0] my_state;
wire [2:0] pos;
reg [3:0] sel_out;
reg [4:0] random_hat;
wire [4:0] right_out;
reg [4:0] count_for_lose;
reg [2:0] rand_new;
reg [2:0] rand_old;
reg [2:0] rand_rand_count;
reg rand_rand_clk_sep;
reg [2:0] positionBuf_count;
reg [3:0] lowerBuf_a;
reg [3:0] lowerBuf_c;
reg [3:0] lowerBuf_b;
reg [3:0] lowerBuf_e;
reg [3:0] lowerBuf_d;
reg [3:0] upperBuf_a;
reg [3:0] upperBuf_c;
reg [3:0] upperBuf_b;
reg [3:0] upperBuf_e;
reg [3:0] upperBuf_d;





always @(posedge fastClk) begin: DISPLAY_CHANGECOL
    if ((disp_col == 4)) begin
        disp_col <= 0;
    end
    else begin
        disp_col <= (disp_col + 1);
    end
end


always @(sel_out, pos, sel_out2, disp_col) begin: DISPLAY_ASSIGN
    col_sel = disp_col;
    rows[7-1:0] = {sel_out2[3-1:0], sel_out};
    if ((pos == disp_col)) begin
        rows[7] = 1;
    end
    else begin
        rows[7] = sel_out2[3];
    end
end


always @(posedge clk, posedge resetbutton) begin: DISPLAY_FSM
    if (resetbutton == 1) begin
        left_in <= 0;
        my_state <= 1'b0;
        count_for_lose <= 0;
    end
    else begin
        if ((my_state == 1'b0)) begin
            left_in <= random_hat;
            if (isThereCollision) begin
                my_state <= 1'b1;
                left_in <= 31;
            end
        end
        else begin
            if ((count_for_lose < 23)) begin
                left_in <= 31;
                // left_in.next[0] = 1
                // left_in.next[1] = (not row[1] and not row[4]) or (not row[2] and row[3] and not row[4]) or (row[2] and not row[3] and not row[4]) or (row[0] and row[3]) or (row[0] and row[2])
                // left_in.next[2] = (not row[4]) or (row[0] and row[3]) or (row[0] and row[4])
                // left_in.next[3] = (not row[2] and not row[3] and not row[4]) or (not row[1] and row[2] and row[3] and not row[4]) or (row[1] and not row[3] and not row[4]) or (row[0] and row[2] and row[4])
                // left_in.next[4] = 1
            end
            else if ((count_for_lose < 31)) begin
                left_in <= 0;
            end
            else begin
                my_state <= 1'b0;
            end
            count_for_lose <= ((count_for_lose + 1) % 32);
        end
    end
end


always @(posedge clk, posedge resetbutton) begin: DISPLAY_UPPERBUF_SHIFTER
    if (resetbutton == 1) begin
        upperBuf_a <= 0;
        upperBuf_c <= 0;
        upperBuf_b <= 0;
        upperBuf_e <= 0;
        upperBuf_d <= 0;
    end
    else begin
        upperBuf_a[4-1:1] <= upperBuf_a[3-1:0];
        upperBuf_a[0] <= left_in[0];
        upperBuf_b[4-1:1] <= upperBuf_b[3-1:0];
        upperBuf_b[0] <= left_in[1];
        upperBuf_c[4-1:1] <= upperBuf_c[3-1:0];
        upperBuf_c[0] <= left_in[2];
        upperBuf_d[4-1:1] <= upperBuf_d[3-1:0];
        upperBuf_d[0] <= left_in[3];
        upperBuf_e[4-1:1] <= upperBuf_e[3-1:0];
        upperBuf_e[0] <= left_in[4];
    end
end


always @(upperBuf_a, upperBuf_c, upperBuf_b, upperBuf_e, upperBuf_d, disp_col) begin: DISPLAY_UPPERBUF_SELECTOR
    case (disp_col)
        'h0: begin
            sel_out = upperBuf_a;
        end
        'h1: begin
            sel_out = upperBuf_b;
        end
        'h2: begin
            sel_out = upperBuf_c;
        end
        'h3: begin
            sel_out = upperBuf_d;
        end
        'h4: begin
            sel_out = upperBuf_e;
        end
    endcase
end



assign right_out = {upperBuf_e[3], upperBuf_d[3], upperBuf_c[3], upperBuf_b[3], upperBuf_a[3]};


always @(posedge clk, posedge resetbutton) begin: DISPLAY_LOWERBUF_SHIFTER
    if (resetbutton == 1) begin
        lowerBuf_a <= 0;
        lowerBuf_c <= 0;
        lowerBuf_b <= 0;
        lowerBuf_e <= 0;
        lowerBuf_d <= 0;
    end
    else begin
        lowerBuf_a[4-1:1] <= lowerBuf_a[3-1:0];
        lowerBuf_a[0] <= right_out[0];
        lowerBuf_b[4-1:1] <= lowerBuf_b[3-1:0];
        lowerBuf_b[0] <= right_out[1];
        lowerBuf_c[4-1:1] <= lowerBuf_c[3-1:0];
        lowerBuf_c[0] <= right_out[2];
        lowerBuf_d[4-1:1] <= lowerBuf_d[3-1:0];
        lowerBuf_d[0] <= right_out[3];
        lowerBuf_e[4-1:1] <= lowerBuf_e[3-1:0];
        lowerBuf_e[0] <= right_out[4];
    end
end


always @(lowerBuf_a, lowerBuf_c, lowerBuf_b, lowerBuf_e, lowerBuf_d, disp_col) begin: DISPLAY_LOWERBUF_SELECTOR
    case (disp_col)
        'h0: begin
            sel_out2 = lowerBuf_a;
        end
        'h1: begin
            sel_out2 = lowerBuf_b;
        end
        'h2: begin
            sel_out2 = lowerBuf_c;
        end
        'h3: begin
            sel_out2 = lowerBuf_d;
        end
        'h4: begin
            sel_out2 = lowerBuf_e;
        end
    endcase
end



assign right_out2 = {lowerBuf_e[3], lowerBuf_d[3], lowerBuf_c[3], lowerBuf_b[3], lowerBuf_a[3]};


always @(posedge leftbutton, posedge rightbutton) begin: DISPLAY_POSITIONBUF_SHIFTING
    if (rightbutton) begin
        if ((positionBuf_count == 0)) begin
            positionBuf_count <= 4;
        end
        else begin
            positionBuf_count <= (positionBuf_count - 1);
        end
    end
    else if (leftbutton) begin
        if ((positionBuf_count == 4)) begin
            positionBuf_count <= 0;
        end
        else begin
            positionBuf_count <= (positionBuf_count + 1);
        end
    end
    else begin
        // pass
    end
end



assign pos = positionBuf_count;


always @(rand_new) begin: DISPLAY_RAND_DEC_DECODER
    case (rand_new)
        'h0: begin
            random_hat = 1;
        end
        'h1: begin
            random_hat = 2;
        end
        'h2: begin
            random_hat = 4;
        end
        'h3: begin
            random_hat = 8;
        end
        'h4: begin
            random_hat = 16;
        end
    endcase
end


always @(posedge fastClk) begin: DISPLAY_RAND_RAND_COUNTING
    if ((rand_rand_count != 4)) begin
        rand_rand_count <= (rand_rand_count + 1);
    end
    else begin
        rand_rand_count <= 0;
    end
end


always @(posedge rand_rand_clk_sep) begin: DISPLAY_RAND_RAND_SHOWING
    integer a;
    if ((rand_old == rand_rand_count)) begin
        a = (rand_rand_count + 1);
        if ((a == 5)) begin
            a = 0;
        end
        rand_new <= a;
        rand_old <= a;
    end
    else begin
        rand_new <= rand_rand_count;
        rand_old <= rand_rand_count;
    end
end


always @(posedge clk) begin: DISPLAY_RAND_RAND_CLOCK_CUTTING
    rand_rand_clk_sep <= (!rand_rand_clk_sep);
end


always @(right_out2, pos) begin: DISPLAY_COLLISION_CHECK
    case (pos)
        'h0: begin
            if (right_out2[0]) begin
                isThereCollision = 1'b1;
            end
            else begin
                isThereCollision = 1'b0;
            end
        end
        'h1: begin
            if (right_out2[1]) begin
                isThereCollision = 1'b1;
            end
            else begin
                isThereCollision = 1'b0;
            end
        end
        'h2: begin
            if (right_out2[2]) begin
                isThereCollision = 1'b1;
            end
            else begin
                isThereCollision = 1'b0;
            end
        end
        'h3: begin
            if (right_out2[3]) begin
                isThereCollision = 1'b1;
            end
            else begin
                isThereCollision = 1'b0;
            end
        end
        'h4: begin
            if (right_out2[4]) begin
                isThereCollision = 1'b1;
            end
            else begin
                isThereCollision = 1'b0;
            end
        end
        default: begin
            isThereCollision = 1'b1;
        end
    endcase
end

endmodule