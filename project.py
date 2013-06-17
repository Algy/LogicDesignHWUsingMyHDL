from myhdl import *

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

def random(select_clk, fast_clk , old, new):

    count = Signal(intbv(0)[3:]) # [0,4]
    clk_sep = Signal(1)
    
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

# upper is lower bit
# from left, col 0, 1 , 2 , 3, 4
def upLEDShift(clk, rst, i, sel, sel_out, right_out):
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

# below is test code
def randomerTestbench():
    fastClk = Signal(True)
    selClk = Signal(intbv(True))
    old = Signal(intbv(0)[3:])
    new = Signal(intbv(0)[3:])

    @always(delay(37))
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
    selClk = Signal(intbv(True))
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
    
    upled = upLEDShift(selClk, ResetSignal(0, active=1, async=True), left_in, sel, sel_out, right_out)
    downled = upLEDShift(selClk, ResetSignal(0, active=1, async=True), right_out, sel, sel_out2, right_out2)
    
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
                
                                          
    return fastClkGen,selClkGen,rand,monitor, upled, downled, dec

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
    sim = Simulation(ledGenTest())

    sim.run(100000)
