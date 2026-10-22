import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

@cocotb.test()
async def test_vreg_basic(dut):

    # Create a 10ns period clock (100MHz) on port 'clk'
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.wr_en.value = 0
    dut.wr_data.value = 0
    dut.wr_addr.value = 0
    dut.wr_bank_sel.value = 0

    dut.rd_bank_sel.value = 0
    dut.rd_addr_a.value = 0
    dut.rd_addr_b.value = 0

    await Timer(20, unit="ns")  # Wait 2 cycles for signals to settle

    #Test values
    test_pattern = 0xDEADBEEF_ABCDBDEF_BBDBABDE_BDEBFDAE
    target_reg = 1
    target_bank = 0

    await RisingEdge(dut.clk)  # Wait for the next rising edge of the clock
    
    dut.wr_en.value = 1
    dut.wr_data.value = test_pattern
    dut.wr_addr.value = target_reg
    dut.wr_bank_sel.value = target_bank
    
    await RisingEdge(dut.clk)  # Wait for the next rising edge of the clock
    
    dut.wr_en.value = 0
    dut.rd_bank_sel.value = target_bank
    dut.rd_addr_a.value = target_reg

    await Timer(1, unit="ns")  # Wait for a short time for combinational propogation

    read_value = dut.rd_data_a.value.integer
    dut._log.info(f"Written: {hex(test_pattern)}")
    dut._log.info(f"Read: {hex(read_value)}")

    assert read_value == test_pattern, f"Mismatch! Expected {hex(test_pattern)}, got {hex(read_value)}"