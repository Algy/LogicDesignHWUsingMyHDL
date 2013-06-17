from myhdl import *

#tested
def dec325(sel, o):
    @always_comb
    def decoder():
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
    return decoder

#tested
def random(select_clk, fast_clk , old, new):

    count = Signal(intbv(0)[3:]) # [0,4]
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
            new.next = (count + 1)%5
            old.next = (count + 1)%5
        else:
            new.next = count
            old.next = count
    return counting, showing, clock_cutting

#tested
def random_comp(select_clk, fast_clk, o):
    old = Signal(intbv(0)[3:])
    new = Signal(intbv(0)[3:])
    
    dec = dec325(new, o)
    rand = random(select_clk, fast_clk, old, new)

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
        right_out.next = Signal(concat( e[3], d[3], c[3], b[3], a[3]))
    return shifter, selector, right_outter

def position(left, right, pos):
    count = Signal(intbv(0)[3:])
    # left : -- , right : ++
    @always(left.posedge)
    def lefting():
        if right == False:
            if left == 0:
                count.next = 4
            else:
                count.next = count - 1
    @always(right.posedge)
    def righting():
        if left == False:
            if left == 4:
                count.next = 0
            else:
                count.next = count + 1
    @always_comb
    def assign():
        pos.next = count
    return lefting, righting, assign

def display(clk, fastClk, leftbutton, resetbutton, rightbutton , rows, col_sel):
    disp_col = Signal(intbv(0)[3:])
    st = enum('START', 'LOSE')
    state = Signal(st.START)
    pos = Signal(intbv(0)[3:])

    # random "hat"
    random_hat = Signal(intbv(0)[5:])
    
    #signals for buffers
    sel = Signal(intbv(0)[3:])
    sel_out = Signal(intbv(0)[4:])
    sel_out2 = Signal(intbv(0)[4:])
    left_in = Signal(intbv(0)[5:]) # this is
    right_out = Signal(intbv(0)[5:])
    right_out2 = Signal(intbv(0)[5:])
    
    # component here

    # for last time, I will seperate these to 3 CPLDs
    upperBuf = LEDShift(clk, resetbutton, left_in, sel, sel_out, right_out) #"positional" upper
    lowerBuf = LEDShift(clk, resetbutton, right_out, sel, sel_out2, right_out2)
    positionBuf = position(leftbutton, rightbutton, pos)# my charactor's position

    rand = random_comp(clk, fastClk, random_hat)
    
    
    @always(resetbutton.posedge)
    def resetState():
        if resetbutton == True:
            state.next = st.START

    @always(fastClk.posedge)
    def changeCol():
        if disp_col == 4:
            disp_col.next = 0
        else:
            disp_col.next = disp_col + 1

    count_for_lose = Signal(intbv(0)[5:])
    
    @always(clk.posedge)
    def FSM():
        if state == st.START:
            #seeding "random hat"
            left_in.next = random_hat
            
            # collision check
            if pos == 0:
                if right_out2[0]:
                    state.next = st.LOSE
            elif pos == 1:
                if right_out2[1]:
                    state.next = st.LOSE
            elif pos == 2:
                if right_out2[2]:
                    state.next = st.LOSE
            elif pos == 3:
                if right_out2[3]:
                    state.next = st.LOSE
            elif pos == 4:
                if right_out2[4]:
                    state.next = st.LOSE
                    
        else: # LOSE state
            count_for_lose.next = count_for_lose + 1
            
            if count_for_lose < 8:
                # downing : 8 ticks
                left_in.next = 63
            elif count_for_lose < 24:
                # holding : 16 ticks
                left_in.next = right_out2
            elif count_for_lose < 31:
                # clearing : 7 ticks
                left_in.next = 0
            else: 
                # change state : 1 ticks
                state = st.START

                    
    @always_comb
    def assign():
        col_sel.next = disp_col
        
        #row assign
        rows.next[7:] = concat(sel_out2[3:] , sel_out )

        if pos == disp_col:
            rows.next[7] = 1
        else:
            rows.next[7] = sel_out2[3]
            
    return changeCol, assign, FSM, upperBuf, lowerBuf, positionBuf, resetState

# below is test code
def randomCompTestBench():
    fastClk = Signal(True)
    selClk = Signal(True)
    val = Signal(intbv(0)[5:])
    @always(delay(37))
    def fastClkGen():
        fastClk.next = not fastClk

    @always(delay(3539))
    def selClkGen():
        selClk.next = not selClk

    
    rand = random_comp(selClk, fastClk, val)
    
    @instance
    def monitor():
        while True:
            yield selClk.negedge
            print val
            yield selClk.posedge
                                        
    return fastClkGen, selClkGen,rand, monitor


def randomerTestbench():
    fastClk = Signal(True)
    selClk = Signal(True)
    old = Signal(intbv(0)[3:])
    new = Signal(intbv(0)[3:])

    @always(delay(31))
    def fastClkGen():
        fastClk.next = not fastClk

    @always(delay(3539))
    def selClkGen():
        selClk.next = not selClk

    r = random(selClk, fastClk, old, new)
    
    @instance
    def monitor():
        while True:
            yield selClk.negedge
            print new
            yield selClk.posedge
                                          
    return fastClkGen,selClkGen,r,monitor
def ledGenTest():

    # Random
    fastClk = Signal(True)
    selClk = Signal(True)
    old = Signal(intbv(0)[3:])
    new = Signal(intbv(0)[3:])
    
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
    

    dec = dec325(new, left_in)
    rand = random(selClk, fastClk, old, new)
    
    upled = LEDShift(selClk, ResetSignal(0, active=1, async=True), left_in, sel, sel_out, right_out)
    downled = LEDShift(selClk, ResetSignal(0, active=1, async=True), right_out, sel, sel_out2, right_out2)
    
    @instance
    def monitor():
        while True:
            yield selClk.negedge
            print "------>"
            
            print ""
            print new
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
    sim = Simulation(randomCompTestBench())
    sim.run(1000000)
