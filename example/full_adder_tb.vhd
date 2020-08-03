--! Use IEEE library
LIBRARY ieee;

--! Use IEEE standard logic
USE ieee.std_logic_1164.ALL;

--! Full adder test-bench entity
ENTITY full_adder_tb IS
END ENTITY full_adder_tb;

--! Full adder test-bench architecture
ARCHITECTURE tb OF full_adder_tb IS

    --! Test bench clock period
    CONSTANT c_clk_period : time := 10 ns;

    -- Signals to unit under test
    SIGNAL a_in  : std_logic; --! A input to full-adder
    SIGNAL b_in  : std_logic; --! B input to full-adder
    SIGNAL c_in  : std_logic; --! Carry input to full-adder
    SIGNAL s_out : std_logic; --! Sum output from full-adder
    SIGNAL c_out : std_logic; --! Carry output from full_adder
    
BEGIN

    --! Instantiate full-adder as unit under test
    i_uut : ENTITY work.full_adder(rtl)
        PORT MAP (
            a_in  => a_in,
            b_in  => b_in,
            c_in  => c_in,
            s_out => s_out,
            c_out => c_out
        );
        
    --! Stimulus process
    pr_stimulus : PROCESS IS
    BEGIN
    
        -- Test
        a_in <= '0';
        b_in <= '0';
        c_in <= '0';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '0') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '0') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '1';
        b_in <= '0';
        c_in <= '0';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '1') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '0') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '0';
        b_in <= '1';
        c_in <= '0';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '1') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '0') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '1';
        b_in <= '1';
        c_in <= '0';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '0') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '1') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '0';
        b_in <= '0';
        c_in <= '1';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '1') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '0') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '1';
        b_in <= '0';
        c_in <= '1';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '0') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '1') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '0';
        b_in <= '1';
        c_in <= '1';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '0') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '1') REPORT "Unexpected c_out value" SEVERITY warning;
    
        -- Test
        a_in <= '1';
        b_in <= '1';
        c_in <= '1';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '1') REPORT "Unexpected s_out value" SEVERITY warning;
        ASSERT (c_out = '1') REPORT "Unexpected c_out value" SEVERITY warning;

        REPORT "Boojum failure" SEVERITY failure;
        
        -- Finish the simulation
        std.env.finish;
    
    END PROCESS pr_stimulus;
        
END ARCHITECTURE tb;
