// File: CPLD1.v
// Generated by MyHDL 0.8
// Date: Mon Jun 24 17:55:39 2013


`timescale 1ns/10ps

module CPLD1 (
    clk,
    left_in,
    right_out2,
    fastClk,
    leftbutton,
    resetbutton,
    rightbutton,
    pos_c,
    sel
);


input clk;
output [4:0] left_in;
reg [4:0] left_in;
input [4:0] right_out2;
input fastClk;
input leftbutton;
input resetbutton;
input rightbutton;
output [2:0] pos_c;
wire [2:0] pos_c;
output [2:0] sel;
reg [2:0] sel;

reg isThereCollision;
reg [0:0] my_state;
wire [2:0] pos;
reg [4:0] random_hat;
reg [4:0] count_for_lose;
reg [2:0] rand_new_out;
reg [2:0] rand_old;
reg [2:0] rand_rand_count;
reg rand_rand_clk_sep;
reg [2:0] positionBuf_count;





always @(posedge fastClk) begin: CPLD1_CHANGECOL
    if ((sel == 4)) begin
        sel <= 0;
    end
    else begin
        sel <= (sel + 1);
    end
end



assign pos_c = pos;


always @(posedge clk, posedge resetbutton) begin: CPLD1_FSM
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
                left_in <= 0;
                my_state <= 1'b0;
            end
            count_for_lose <= ((count_for_lose + 1) % 32);
        end
    end
end


always @(negedge clk) begin: CPLD1_POSITIONBUF_SHIFTING
    if (rightbutton) begin
        if ((!leftbutton)) begin
            if ((positionBuf_count == 0)) begin
                positionBuf_count <= 4;
            end
            else begin
                positionBuf_count <= (positionBuf_count - 1);
            end
        end
    end
    else if (leftbutton) begin
        if ((!rightbutton)) begin
            if ((positionBuf_count == 4)) begin
                positionBuf_count <= 0;
            end
            else begin
                positionBuf_count <= (positionBuf_count + 1);
            end
        end
    end
    else begin
        // pass
    end
end



assign pos = positionBuf_count;


always @(right_out2, pos) begin: CPLD1_COLLISION_CHECK
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

// if sel == 0:
//     o.next = intbv(1)
// elif sel == 1:
//     o.next = intbv(2)
// elif sel == 2:
//     o.next = intbv(4)
// elif sel == 3:
//     o.next = intbv(8)
// elif sel == 4:
//     o.next = intbv(16)
always @(rand_new_out) begin: CPLD1_RAND_DEC_DECODER
    random_hat[0] = ((!rand_new_out[0]) && (!rand_new_out[1]) && (!rand_new_out[2]));
    random_hat[1] = (rand_new_out[0] && (!rand_new_out[1]) && (!rand_new_out[2]));
    random_hat[2] = ((!rand_new_out[0]) && rand_new_out[1] && (!rand_new_out[2]));
    random_hat[3] = (rand_new_out[0] && rand_new_out[1] && (!rand_new_out[2]));
    random_hat[4] = ((!rand_new_out[0]) && (!rand_new_out[1]) && rand_new_out[2]);
end


always @(posedge fastClk) begin: CPLD1_RAND_RAND_COUNTING
    if ((rand_rand_count != 4)) begin
        rand_rand_count <= (rand_rand_count + 1);
    end
    else begin
        rand_rand_count <= 0;
    end
end


always @(posedge rand_rand_clk_sep) begin: CPLD1_RAND_RAND_SHOWING
    integer a;
    if ((rand_old == rand_rand_count)) begin
        a = (rand_rand_count + 1);
        if ((a == 5)) begin
            a = 0;
        end
        rand_new_out <= a;
        rand_old <= a;
    end
    else begin
        rand_new_out <= rand_rand_count;
        rand_old <= rand_rand_count;
    end
end


always @(posedge clk) begin: CPLD1_RAND_RAND_CLOCK_CUTTING
    rand_rand_clk_sep <= (!rand_rand_clk_sep);
end

endmodule
