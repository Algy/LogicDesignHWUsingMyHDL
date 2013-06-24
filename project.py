# -*- coding: cp949 -*-
from myhdl import *

#tested
def dec325(sel, o):
    @always_comb
    def decoder():
        '''
        if sel == 0:
            o.next = intbv(1)
        elif sel == 1:
            o.next = intbv(2)
        elif sel == 2:
            o.next = intbv(4)
        elif sel == 3:
            o.next = intbv(8)
        elif sel == 4:
            o.next = intbv(16)
        '''
        o.next[0]= not sel[0] and  not sel[1] and  not sel[2] 
        o.next[1]=sel[0] and  not sel[1] and  not sel[2] 
        o.next[2]= not sel[0] and sel[1] and  not sel[2] 
        o.next[3]=sel[0] and sel[1] and  not sel[2] 
        o.next[4]= not sel[0] and  not sel[1] and sel[2] 
    return decoder

#tested
def random(select_clk, fast_clk , old, new_out):

    count = Signal(modbv(0)[3:]) # [0,4]
    clk_sep = Signal(True)
    
    @always(fast_clk.posedge)
    def counting():
        
        if count != 4:
            count.next = count + 1
        else:
            count.next = 0
    
    @always(select_clk.posedge)
    def clock_cutting():
        clk_sep.next = not clk_sep
        
    @always(clk_sep.posedge)
    def showing():
        if old == count:
            
            a  = (count + 1)
            if a == 5:
                a = 0
            new_out.next = a #(count + 1)%5
            old.next = a #(count + 1)%5
        else:
            new_out.next = count
            old.next = count
    return counting, showing, clock_cutting

#tested
def random_comp(select_clk, fast_clk, o):
    old = Signal(modbv(0)[3:])
    new_out = Signal(modbv(0)[3:])
    
    dec = dec325(new_out, o)
    rand = random(select_clk, fast_clk, old, new_out)

    return dec, rand

#tested
# upper is lower bit
# from left, col 0, 1 , 2 , 3, 4
def LEDShift(clk, rst, i, sel, sel_out, right_out):
    # a =0, b = 1, c =2 , d =3 , e = 4 
    a,b,c,d,e = [Signal(modbv(0)[4:]) for x in range(5)]
    
    @always_seq(clk.posedge, reset=rst)
    def shifter():
        a.next[4:1] = a[3:0]
        a.next[0] = i[0]
        
        b.next[4:1] = b[3:0]
        b.next[0] = i[1]
        
        c.next[4:1] = c[3:0]
        c.next[0] = i[2]
        
        d.next[4:1] = d[3:0]
        d.next[0] = i[3]
        
        e.next[4:1] = e[3:0]
        e.next[0] = i[4]
        
    @always_comb
    def selector():
        if sel == 0:
            sel_out.next = a
        elif sel == 1:
            sel_out.next = b
        elif sel == 2:
            sel_out.next = c
        elif sel == 3:
            sel_out.next = d
        elif sel == 4:
            sel_out.next = e

    @always_comb
    def right_outter():
        right_out.next = concat( e[3], d[3], c[3], b[3], a[3])
    return shifter, selector, right_outter

#tested
def position(left, right, pos):
    count = Signal(intbv(0)[3:])

    # left : -- , right : ++
    @always(left.posedge, right.posedge)
    def shifting():
        if right:
            if not left:
                if count == 0:
                    count.next = 4
                else:
                    count.next = count - 1
        elif left:
            if not right:
                    
                if count == 4:
                    count.next = 0
                else:
                    count.next = count + 1
        else:
            pass

    '''
    @always(right.posedge)
    def righting():
        if left == False:
            if count == 4:
                count.next = 0
            else:
                count.next = count + 1
    '''
    @always_comb
    def assign():
        pos.next = count
    return shifting, assign
def CPLD1(clk, left_in, right_out2, fastClk, leftbutton, resetbutton, rightbutton , pos_c, sel):
    st = enum('START', 'LOSE')
    my_state = Signal(st.START)
    pos = Signal(intbv(0)[3:])
    
    # random "hat"
    random_hat = Signal(intbv(0)[5:])
    
    count_for_lose = Signal(intbv(0)[5:])
    isThereCollision = Signal(False)    
    # component here

    # for last time, I will seperate these to 3 CPLDs
    # def LEDShift(clk, rst, i, sel, sel_out, right_out):
    positionBuf = position(leftbutton, rightbutton, pos)# my charactor's position

    rand = random_comp(clk, fastClk, random_hat)
    
    @always(fastClk.posedge)
    def changeCol():
        if sel == 4:
            sel.next = 0
        else:
            sel.next = sel + 1

    @always_comb
    def collision_check():
        # collision check
        if pos == 0:
            if right_out2[0]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 1:
            if right_out2[1]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 2:
            if right_out2[2]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 3:
            if right_out2[3]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 4:
            if right_out2[4]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        else:
            isThereCollision.next = True

            
    @always_seq(clk.posedge, reset= resetbutton)
    def FSM():
        if my_state == st.START:
            #seeding "random hat"
            left_in.next = random_hat
            
            # collision check
            if isThereCollision:
                my_state.next = st.LOSE
                left_in.next = 31
                #print "COLLISION"
                
        else: # LOSE state
            
            if count_for_lose < 23:
                # downing&holding : 24 ticks
                # row = count_for_lose
                left_in.next = 31
                ''' 
                left_in.next[0] = 1
                left_in.next[1] = (not row[1] and not row[4]) or (not row[2] and row[3] and not row[4]) or (row[2] and not row[3] and not row[4]) or (row[0] and row[3]) or (row[0] and row[2])
                left_in.next[2] = (not row[4]) or (row[0] and row[3]) or (row[0] and row[4])
                left_in.next[3] = (not row[2] and not row[3] and not row[4]) or (not row[1] and row[2] and row[3] and not row[4]) or (row[1] and not row[3] and not row[4]) or (row[0] and row[2] and row[4])
                left_in.next[4] = 1
                '''
            elif count_for_lose < 31:
                # clearing : 7 ticks
                left_in.next = 0
            else: 
                left_in.next = 0
                # change state : 1 ticks
                my_state.next = st.START
                
            count_for_lose.next = (count_for_lose + 1)%32

                    
    @always_comb
    def assign():
        pos_c.next = pos
            
    return changeCol, assign, FSM, positionBuf,  collision_check , rand

def CPLD2(clk,rst, left_in, sel, sel_out, right_out, sel_decoded):
    sel_decoded_before_fit = Signal( intbv(0)[5:] )
    
    a = LEDShift(clk,rst,left_in,sel,sel_out, right_out)
    dec = dec325(sel, sel_decoded_before_fit)

    @always_comb
    def fitToMatrix():
        sel_decoded.next[0] = not sel_decoded_before_fit[0]
        sel_decoded.next[1] = not sel_decoded_before_fit[1]
        sel_decoded.next[2] = not sel_decoded_before_fit[2]
        sel_decoded.next[3] = not sel_decoded_before_fit[3]
        sel_decoded.next[4] = not sel_decoded_before_fit[4]
        
    return a, dec, fitToMatrix
def CPLD3(clk,rst, left_in2, sel, sel_out2, right_out2, pos_c, last_row):
    a = LEDShift(clk,rst,left_in2,sel,sel_out2, right_out2)
    last = Signal(True)
    
    @always_comb
    def replaceCharactor():
        if pos_c == sel:
            last_row.next = 1
        else:
            last_row.next = sel_out2[3]
    
    return a, replaceCharactor
def overall( clk, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel, sel_decoded):
    # (clk, left_in, right_out2, fastClk, leftbutton, resetbutton, rightbutton , pos_c, col_sel):
    left_in = Signal(intbv(0)[5:])
    right_out2 = Signal(intbv(0)[5:])
    left_in2 = Signal(intbv(0)[5:])
    pos_c = Signal(intbv(0)[3:])
    sel = Signal(intbv(0)[3:])
    sel_out = Signal(intbv(0)[4:])
    sel_out2 = Signal(intbv(0)[4:])
    last_row = Signal(True)
    
    cpld1 = CPLD1(clk, left_in, right_out2, fastClk, leftbutton, resetbutton, rightbutton, pos_c, sel)
    cpld2 = CPLD2(clk, resetbutton, left_in, sel, sel_out, left_in2, sel_decoded)
    
    cpld3 = CPLD3(clk, resetbutton, left_in2, sel,sel_out2, right_out2, pos_c, last_row)
    
                  
    @always_comb
    def assign():
        rows.next[4:] = sel_out
        rows.next[7:4] = sel_out2[3:]
        rows.next[7] = last_row
        col_sel.next = sel
        
    return cpld1, cpld2, cpld3, assign
def display(clk, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel):
    disp_col = Signal(intbv(0)[3:])
    st = enum('START', 'LOSE')
    my_state = Signal(st.START)
    
    pos = Signal(intbv(0)[3:])

    # random "hat"
    random_hat = Signal(intbv(0)[5:])
    
    #signals for buffers
    sel_out = Signal(intbv(0)[4:])
    sel_out2 = Signal(intbv(0)[4:])
    left_in = Signal(intbv(0)[5:]) 
    right_out = Signal(intbv(0)[5:])
    right_out2 = Signal(intbv(0)[5:])

    count_for_lose = Signal(intbv(0)[6:])
    isThereCollision = Signal(False)    
    # component here

    # for last time, I will seperate these to 3 CPLDs
    # def LEDShift(clk, rst, i, sel, sel_out, right_out):
    upperBuf = LEDShift(clk, resetbutton, left_in, disp_col, sel_out, right_out) #"positional" upper
    lowerBuf = LEDShift(clk, resetbutton, right_out, disp_col, sel_out2, right_out2)
    positionBuf = position(leftbutton, rightbutton, pos)# my charactor's position

    rand = random_comp(clk, fastClk, random_hat)
    
    @always(fastClk.posedge)
    def changeCol():
        if disp_col == 4:
            disp_col.next = 0
        else:
            disp_col.next = disp_col + 1

    @always_comb
    def collision_check():
        # collision check
        if pos == 0:
            if right_out2[0]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 1:
            if right_out2[1]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 2:
            if right_out2[2]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 3:
            if right_out2[3]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        elif pos == 4:
            if right_out2[4]:
                isThereCollision.next = True
            else:
                isThereCollision.next = False
        else:
            isThereCollision.next = True

            
    @always_seq(clk.posedge, reset= resetbutton)
    def FSM():
        if my_state == st.START:
            #seeding "random hat"
            left_in.next = random_hat
            
            # collision check
            if isThereCollision:
                my_state.next = st.LOSE
                left_in.next = 31
                #print "COLLISION"
                
        else: # LOSE state
            
            if count_for_lose < 24:
                # downing&holding : 24 ticks
                # row = count_for_lose
                left_in.next = 31
                ''' 
                left_in.next[0] = 1
                left_in.next[1] = (not row[1] and not row[4]) or (not row[2] and row[3] and not row[4]) or (row[2] and not row[3] and not row[4]) or (row[0] and row[3]) or (row[0] and row[2])
                left_in.next[2] = (not row[4]) or (row[0] and row[3]) or (row[0] and row[4])
                left_in.next[3] = (not row[2] and not row[3] and not row[4]) or (not row[1] and row[2] and row[3] and not row[4]) or (row[1] and not row[3] and not row[4]) or (row[0] and row[2] and row[4])
                left_in.next[4] = 1
                '''
            elif count_for_lose < 31:
                # clearing : 7 ticks
                left_in.next = 0
            else: 
                # change state : 1 ticks
                my_state.next = st.START
                
            count_for_lose.next = (count_for_lose + 1)%32

                    
    @always_comb
    def assign():
        col_sel.next = disp_col
        
        #row assign
        rows.next[7:4] = sel_out2[3:]
        rows.next[4:0] = sel_out
        
        if pos == disp_col:
            rows.next[7] = 1
#            rows.next[6] = 1
        else:
            rows.next[7] = sel_out2[3]
#            rows.next[6] = sel_out2[2]
            
    return changeCol, assign, FSM, upperBuf, lowerBuf, positionBuf, rand, collision_check

'''
"LOSE" - ASCII ART\
1 1 1 1 1
1 1 1 1 1
1 0 1 1 1
1 0 1 1 1
1 0 1 1 1
1 0 0 0 1
1 1 1 1 1
1 0 0 0 1
1 0 1 0 1
1 0 0 0 1
1 1 1 1 1
1 0 0 0 1
1 0 1 1 1
1 0 0 0 1
1 1 1 0 1
1 0 0 0 1
1 1 1 1 1
1 0 0 0 1
1 0 1 1 1
1 0 0 0 1
1 0 1 1 1
1 0 0 0 1 - row 1
1 1 1 1 1 - row 0
'''
'''
def LOSEAscii(row, o):
    @always_comb
    def comb():
        o[0] = 1
        o[1] = (not row[2] and not row[3] and not row[4]) or (not row[1] and row[2] and row[3] and not row[4]) or (row[1] and not row[3] and not row[4]) or (row[0] and row[2] and row[4])
        o[2] = (not row[4]) or (row[0] and row[3]) or (row[0] and row[4])
        o[3] = (not row[1] and not row[4]) or (not row[2] and row[3] and not row[4]) or (row[2] and not row[3] and not row[4]) or (row[0] and row[4]) or (row[0] and row[2])
        o[4] = 1
    return comb
'''
g_rows = [[0]*8 for x in range(5)]
def printRows():
    for i in range(5):
        for j in range(8):
            print int(g_rows[i][j]),
        print ""
    print ""
def assignRows(col_sel,rows):
    
    g_rows[col_sel] = [int(r) for r in rows]
        
# below is test code
def displayTestBench():
    fastClk = Signal(True)
    selClk = Signal(True)
    leftButton = Signal(False)
    rightButton = Signal(False)
    resetButton = ResetSignal(0, active=1, async=True)
    rows = Signal(intbv(0)[8:])
    col_sel = Signal(intbv(0)[3:])
    
    @always(delay(37))
    def fastClkGen():
        fastClk.next = not fastClk

    @always(delay(3537))
    def selClkGen():
        selClk.next = not selClk
    #(clk, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel)
        
    sel_decoded = Signal(intbv(0)[5:])
    main = overall(selClk, fastClk, leftButton, resetButton, rightButton, rows, col_sel, sel_decoded)

    @instance
    def monitor():
        al = [[0]*8 for x in range(5)]
        while True:
            yield selClk.negedge
            yield selClk.posedge
            '''
            print "[",col_sel,"]",
            for i in range(8):
                print int(rows[i]),
            print ""
            '''
            for t in range(5):

                yield fastClk.posedge
                print bin(sel_decoded)
                for x in range(8):
                    
                    al[col_sel][x] = "■" if rows[x] else "□"
                    
            
            for i in range(5):
                for j in range(8):
                    print al[i][j],
                print ""
            print ""
            
    return fastClkGen, selClkGen, main, monitor

def ledGenTest():

    # Random
    fastClk = Signal(True)
    selClk = Signal(True)
    old = Signal(intbv(0)[3:])
    new_out = Signal(intbv(0)[3:])
    
    @always(delay(37))
    def fastClkGen():
        fastClk.next = not fastClk

    @always(delay(3539))
    def selClkGen():
        selClk.next = not selClk


    # LED
    sel = Signal(intbv(0)[3:])
    sel_out = Signal(intbv(0)[4:])
    sel_out2 = Signal(intbv(0)[4:])
    left_in = Signal(intbv(0)[5:])
    right_out = Signal(intbv(0)[5:])
    right_out2 = Signal(intbv(0)[5:])
    

    dec = dec325(new_out, left_in)
    rand = random(selClk, fastClk, old, new_out)
    
    upled = LEDShift(selClk, ResetSignal(0, active=1, async=True), left_in, sel, sel_out, right_out)
    downled = LEDShift(selClk, ResetSignal(0, active=1, async=True), right_out, sel, sel_out2, right_out2)
    
    @instance
    def monitor():
        while True:
            yield selClk.negedge
            print "------>"
            
            print ""
            print new_out
            print ""
            
            yield selClk.posedge
            for s in range(5):
                sel.next = s
                yield delay(2)
                for x in range(4):
                    print int(sel_out[x]),
                for x in range(4):
                    print int(sel_out2[x]),

                print ""
            print "right_out", right_out                           
    return fastClkGen,selClkGen,rand, upled, downled, dec,monitor

def decoderTest():
    i,o = [Signal(intbv(0)[2:]), Signal(intbv(0)[4:])]
    
    r = dec224(i,o)

    @instance
    def mon():
        for x in range(4):
            i.next = x
            yield delay(1)
            print "%d %d"%(i , o)
    return r, mon        
if __name__ == "__main__":
    sim = Simulation(displayTestBench())
    '''
def CPLD2(clk,rst, left_in, sel, sel_out, right_out):
def CPLD3(clk,rst, left_in2, sel, sel_out2, right_out2, pos_c, last_row):
'''
    #def display(clk, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel):
    toVerilog(display, Signal(False), Signal(False), Signal(False), ResetSignal(0,active=1, async=True), Signal(False), Signal(intbv(0)[8:]), Signal(intbv(0)[3:])) 
    #def LEDShift(clk, rst, i, sel, sel_out, right_out):
    toVerilog(LEDShift, Signal(False),ResetSignal(0,active=1, async=True), Signal(intbv(0)[5 : ]), Signal(intbv(0)[5:]), Signal(intbv(0)[4:]), Signal(intbv(0)[5:]))
    toVerilog(CPLD2, Signal(False),ResetSignal(0,active=1, async=True), Signal(intbv(0)[5 : ]), Signal(intbv(0)[3:]), Signal(intbv(0)[4:]), Signal(intbv(0)[5:]), Signal(intbv(0)[5:]))
    toVerilog(CPLD3, Signal(False),ResetSignal(0,active=1, async=True), Signal(intbv(0)[5 : ]), Signal(intbv(0)[3:]), Signal(intbv(0)[4:]), Signal(intbv(0)[5:]), Signal(intbv(0)[3:]), Signal(True)) 
    #displaySeperate(clk, left_in, right_out2, sel_out,sel_out2, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel):
    #displaySeperate(clk, left_in, right_out2, fastClk, leftbutton, resetbutton, rightbutton , pos_c, col_sel):
    toVerilog(CPLD1, Signal(False), Signal(modbv(0)[5:]), Signal(modbv(0)[5:]),Signal(False), Signal(False), ResetSignal(0,active=1, async=True), Signal(False), Signal(intbv(0)[3:]), Signal(intbv(0)[3:]))
    sim.run(10000000)
