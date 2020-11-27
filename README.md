# Test Vector Leakage Assessment (TVLA) methodology implementation

This repository contains an implementation to conduct the specific leakage tests as per the TVLA methodology, given the CSV files for collected power traces.

## File Descriptions
- aes.py: Contains a software implementation of AES-128.
- TVLA.py: Contains the code that analyses the power traces and generates the graphs
- test.py: Main file to be run to conduct the test

## Tests implemented
- **Test 1 - RIRO_M_bit_0 through RIRO_M_bit_127** : For each trace t, let RIRO_M(t) denote the EXOR of Round M input with Round M output for trace t. For each bit i from 0 to 127, the test RIRO_M_bit_i is a t-test that compares the subset of traces t, where bit i of RIRO_M(t) is 0 vs. traces t where bit i of RIRO_M(t) is 1.

- **Test 2 - Rout_M_bit_0 through Rout_M_bit_127**: For each trace t, let Rout_M(t) denote the output of Round M for trace t. For each bit i, from 0 to 127, the test Rout_M_bit_i is a t-test that compares the subset of traces t where bit i of Rout_M(t) is 0 vs. traces t where bit i of Rout_M(t) is 1.

- **Test 3 - Rout_M_byte_0_is_0 through Rout_M_byte_0_is_255**: For each trace t, let Rout_M_byte_0(t) denote the value of the first byte of output of Round M for that trace. For each value b of a byte from 0 to 255, the test Rout_M_byte_0_is_b is a t-test that compares the subset of traces t where Rout_M_byte_0(t) is b vs. traces t where Rout_M_byte_0(t) is not equal to b.

- **Test 4 - Rout_M_byte_1_is_0 through Rout_M_byte_1_is_255**: For each trace t, let Rout_M_byte_1(t)
denote the value of the second byte of output of Round M for that trace. For each value b of a byte from0 to 255, the test Rout_M_byte_1_is_b is a t-test that compares the subset of traces t where
Rout_M_byte_1(t) is b vs. traces t where Rout_M_byte_1(t) is not equal to b.

## Usage Instructions
- In the file test.py, make the value of the variable 'source_dir' as the path to the directory containing the CSV files of the power traces
- Run the file test.py
- Input the value of the test as per the description above
- For tests 1 and 2, at the next prompt, input the value of the i'th bit as per the description above. This value should lie between 0 and 127
- For tests 3 and 4, at the next prompt, input the value b of the byte to be compared with as per the description above. This value should lie between 0 and 255.
- After the test finishes execution, the resulting analysis plot will be in a new directory called results. 