import os
import aes
import subprocess

source_dir = "/home/deepinder/Desktop/Academics/Semester_7/CE/DPA_contest2_public_base_diff_vcc_a128_2009_12_23"
target_1 = "/home/deepinder/Desktop/Academics/Semester_7/CE/p1"
target_2 = "/home/deepinder/Desktop/Academics/Semester_7/CE/p2"

directory = os.fsencode(source_dir)
m = 5


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"): 
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
            file_location = source_dir + "/" + filename
            #conditon
            v1 = intermediate[m]
            v2 = intermediate[m+1]
            v1_int = int(v1, 16)
            v2_int = int(v2, 16)
            v1 = format(v1_int, '0>128b')
            v2 = format(v2_int, '0>128b')

            # 5th round 100th bit test
            v1_int = int(v1[100])
            v2_int = int(v2[100])

            if (v1_int + v2_int == 1):
                # XOR = 1
                target_location = target_1
            else:
                target_location = target_2

            command.append(file_location)
            command.append(target_location)
            subprocess.run(command)
        else:
            print("Error in decryption")



