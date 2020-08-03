--! Use IEEE library
LIBRARY ieee;

--! Use IEEE standard logic
USE ieee.std_logic_1164.ALL;

--! Half adder test-bench entity
ENTITY half_adder_fail_tb IS
END ENTITY half_adder_fail_tb;

--! Half adder test-bench architecture
ARCHITECTURE tb OF half_adder_fail_tb IS

    --! Test bench clock period
    CONSTANT c_clk_period : time := 10 ns;

    -- Signals to unit under test
    SIGNAL a_in  : std_logic; --! A input to half-adder
    SIGNAL b_in  : std_logic; --! B input to half-adder
    SIGNAL s_out : std_logic; --! Sum output from half-adder
    SIGNAL c_out : std_logic; --! Carry output from half-adder
    
BEGIN

    --! Instantiate half-adder as unit under test
    i_uut : ENTITY work.half_adder(rtl)
        PORT MAP (
            a_in  => a_in,
            b_in  => b_in,
            s_out => s_out,
            c_out => c_out
        );
        
    --! Stimulus process
    pr_stimulus : PROCESS IS
    BEGIN
    
        -- Test
        a_in <= '0';
        b_in <= '0';
        WAIT FOR c_clk_period;
        ASSERT (s_out = '1') REPORT "Bad s_out test" SEVERITY error;
        ASSERT (c_out = '1') REPORT "Bad c_out test" SEVERITY error;
        
        -- Finish the simulation
        std.env.finish;
    
    END PROCESS pr_stimulus;
        
END ARCHITECTURE tb;
