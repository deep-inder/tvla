import os
import aes
import subprocess
from tqdm import tqdm
import TVLA

source_dir = "/home/deepinder/Desktop/Academics/Semester_7/CE_proj/sample/"
target_1 = "p1/"
target_2 = "p2/"
m = 4


def riro_round_5_bit_i(bit, test):
    directory = os.fsencode(source_dir)

    subprocess.run(['mkdir', target_1])
    subprocess.run(['mkdir', target_2])
    count = 0
    for file in os.listdir(directory):
        count += 1
        if (count % 1000 == 0):
            print("Processed", count, "files")


        filename = os.fsdecode(file)
        arr = filename.strip().split('_')
        # get the key, plaintext and ciphertext
        key = arr[5]
        pt = arr[6]
        ct = arr[7]
        key = key[2:]
        pt = pt[2:]
        ct = ct[2:34]
        #convert these to bytes objects
        key = bytes.fromhex(key)
        pt = bytes.fromhex(pt)
        ct = bytes.fromhex(ct)

        aes_obj = aes.AES(key)
        out, intermediate = aes_obj.decrypt_block(ct)
        if (out == pt):
            command = ["cp"]
            file_location = source_dir + filename
            #conditon
            v1 = intermediate[m]
            v2 = intermediate[m+1]
            v1_int = int(v1, 16)
            v2_int = int(v2, 16)
            v1 = format(v1_int, '0>128b')
            v2 = format(v2_int, '0>128b')

            # 5th round bth bit test
            if(bit < 128):
                v1_int = int(v1[bit])
                v2_int = int(v2[bit])

            if (test == 1):
                if (v1_int + v2_int == 1):
                    # XOR = 1
                    target_location = target_2
                else:
                    target_location = target_1
            elif (test == 2):
                if (v1_int == 0):
                    target_location = target_1

                else:
                    target_location = target_2

            elif (test == 3):
                b_str = v1[120:]
                b = int(b_str, 2)
                if (b == bit):
                    target_location = target_1
                else:
                    target_location = target_2

            elif (test == 4):
                b_str = v1[112:120]
                b = int(b_str, 2)
                if (b == bit):
                    target_location = target_1
                else:
                    target_location = target_2

            command.append(file_location)
            command.append(target_location)
            subprocess.run(command)
        else:
            print("Error in decryption")

    TVLA.run(target_1, target_2, str(bit)+"_"+str(test))

    subprocess.run(['rm', '-r', target_1])
    subprocess.run(['rm', '-r', target_2])

if __name__ == "__main__":
    test = int(input("Test: "))
    if (test == 3 or test == 4):
        byte = int(input("Comparison byte value: "))
        riro_round_5_bit_i(byte, test)
    else:
        bit = int(input("Bit: "))
        riro_round_5_bit_i(bit, test)



