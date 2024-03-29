import sys
import os
import traceback
from textwrap import wrap
import numpy as np

PATH = os.getcwd()
PLAINTEXT_PATH = os.path.dirname(PATH) + '\data\plaintext.txt'
SUBKEY_PATH = os.path.dirname(PATH) + '\data\subkey_example.txt'
RESULT_PATH = os.path.dirname(PATH) + '\data\_result_subkey.txt'
RESULT_DIR = os.path.dirname(PATH) + '\data\_result.txt'

SCALE = 16 #equal to hex
NUM_BITS = 8
AES_S_BOX = np.array([
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
])

MIX_COLUMNS = np.array([
    ["0x02", "0x03", "0x01", "0x01"],
    ["0x01", "0x02", "0x03", "0x01"],
    ["0x01", "0x01", "0x02", "0x03"],
    ["0x03", "0x01", "0x01", "0x02"]
])


class aes_Obj(object):

    def __init__(self):
        self.platform = sys.platform
        self.message_ascii = None
        self.message_bit = None
        self.message_hex = None
        self.initial_state = None
        self.plaintext_path = None
        self.subkey_path = None
        self.result_path = None
        self.result_dir = None
        self.subkey0_bin = None
        self.subkey0_hex = None
        self.subkey1_bin = None
        self.subkey1_hex = None
        self.subkey_matrix0 = None
        self.subkey_matrix1 = None

    @staticmethod
    def sub_bytes():       
    
        '''
         Replace every byte in the State with the corresponding AES_S_BOX value.
        '''         

        for x in aes.initial_state:
            first = x[0]
            second = x[1]
            third = x[2]
            fourth = x[3]

            new1 = hex(AES_S_BOX[int(first[0], 16), int(first[1], 16)])
            new2 = hex(AES_S_BOX[int(second[0], 16), int(second[1], 16)])
            new3 = hex(AES_S_BOX[int(third[0], 16), int(third[1], 16)])
            new4 = hex(AES_S_BOX[int(fourth[0], 16), int(fourth[1], 16)])

            aes.initial_state = (np.where(aes.initial_state == first, new1, aes.initial_state))
            aes.initial_state = (np.where(aes.initial_state == second, new2, aes.initial_state))
            aes.initial_state = (np.where(aes.initial_state == third, new3, aes.initial_state))
            aes.initial_state = (np.where(aes.initial_state == fourth, new4, aes.initial_state))
        print('Result of the Substitution Box (S-Box) operation: ')
        print(aes.initial_state)
        return

    @staticmethod
    def shift_rows(): 
        '''
        Perform a byte shift operation on the State
        '''                                              
        aes.initial_state[1] = np.roll(aes.initial_state[1], -1)
        aes.initial_state[2] = np.roll(aes.initial_state[2], -2)
        aes.initial_state[3] = np.roll(aes.initial_state[3], -3)
        print("Result of the Row Shifting operation: ")
        print(aes.initial_state)
        return

    @staticmethod
    def mix_columns():     
        '''
        Apply a reversible transformation on each column, except for the final round.
        '''                                         
        list = []
        list2 = []

        for j in range(0, len(aes.initial_state)):
            for i in range(0, len(MIX_COLUMNS)):
                mix_col_list = (MIX_COLUMNS[i].tolist())
                i_state_list = (aes.initial_state.T[j].tolist())

                for k in range(0, len(mix_col_list)):
                    x = str(i_state_list[k])
                    y = str(mix_col_list[k])
                    r = (to_hex(x) * to_hex(y))
                    r = bin(r)[2:]
                    list.append(r)

                n = 00000000

                for i in range(0, len(list)):
                    n = (int(list[i], 2) ^ n)
                list2.append(hex(n))
        chunks = [list2[x:x + 4] for x in range(0, len(list2), 4)]
        aes.initial_state[0] = chunks[0]
        aes.initial_state[1] = chunks[1]
        aes.initial_state[2] = chunks[2]
        aes.initial_state[3] = chunks[3]
        print("Result of the MixColumns operation: ")
        print(aes.initial_state)
        return

    @staticmethod
    def add_key(state, subkey):
        '''
        At this stage, the initial state matrix is XORed with the subkey to generate the next round's initial state. 
        '''                                    
        xor_list = []
        for x, y in zip(state, subkey):
            for elem1, elem2 in zip(x, y):
                elem1 = int(elem1, 16)
                new_elem1 = elem1 + 0x200
                elem2 = int(elem2, 16)
                new_elem2 = elem2 + 0x200
                xor1 = new_elem1 ^ new_elem2
                xor1 = hex(xor1)[2:]
                if len(xor1) < 2:
                    r = '0' + xor1
                    xor_list.append(r)
                else:
                    xor_list.append(xor1)
        chunks = [xor_list[x:x + 4] for x in range(0, len(xor_list), 4)]
        state[0] = chunks[0]
        state[1] = chunks[1]
        state[2] = chunks[2]
        state[3] = chunks[3]
        return state

    @staticmethod
    def add_key_0(): 
        '''
        This step involves the XOR operation between the initial state matrix and the subkey to produce a new state matrix, which will be used as the initial state for the next round.
        '''                                              
        aes.initial_state = aes_Obj.add_key(aes.initial_state, aes.subkey_matrix0)
        print(' Result of AddKey1: ')
        print(aes.initial_state)
        return

    @staticmethod
    def add_key_1():   
        '''
        At this stage, an XOR operation is performed between the initial state matrix and the subkey. The output produced by this operation is then used as the initial state for the next round.
        '''                                          
        aes.initial_state = aes_Obj.add_key(aes.initial_state, aes.subkey_matrix1)
        print('Result of AddKey2 (Final result after first round of AES): ')
        print(aes.initial_state)
        return

    @staticmethod
    def get_initial_state():    
        '''
        The initial state is defined as a 4x4 block matrix containing the hexadecimal values of the input message. This function is responsible for retrieving and assigning the initial state to the object.
        '''
        aes.initial_state = aes.get_matrix(aes.message_hex)
        print('Matrix representing the initial : \n' + str(aes.initial_state))

    @staticmethod
    def get_matrix(hex):     
        '''
        To perform the AES algorithm, the subkey must be converted into a 4x4 matrix using the numpy module.
        '''

        bytes = wrap(hex, 2)


        row1 = []
        row2 = []
        row3 = []
        row4 = []
        for index in range(4):
            row1.append('0x' + bytes[index])
        for index in bytes[4:8]:
            row2.append('0x' + index)
        for index in bytes[8:12]:
            row3.append('0x' + index)
        for index in bytes[12:16]:
            row4.append('0x' + index)
        matrix = np.array([row1, row2, row3, row4])
        matrix = matrix.T
        return matrix

    @staticmethod
    def get_subkey_matrix_0():  
        '''
        In order to use the subkey for the AES algorithm, it must be formatted as a 4x4 matrix using the numpy module.
        '''
        aes.subkey_matrix0 = aes.get_matrix(aes.subkey0_hex)
        print('sub_key matrix 0: \n' + str(aes.subkey_matrix0))

    @staticmethod
    def get_subkey_matrix_1():   
        '''
        To use the subkey in the AES algorithm, it must be converted into a 4x4 matrix using the numpy module.
        '''                                   
        aes.subkey_matrix1 = aes.get_matrix(aes.subkey1_hex)
        print('sub_key matrix 1: \n' + str(aes.subkey_matrix1))

    @staticmethod
    def get_subkeys():        
        '''
        This code assigns the subkeys to the AES object in their 128-bit binary form, while retrieving the hexadecimal values from a file. It is necessary to add a leading 0 to ensure that the subkeys are 128-bits long in case the bit converter drops it.
        '''
        with open(aes.subkey_path, 'r') as f:
            lines = f.readlines()
            aes.subkey0_hex = lines[0]
            aes.subkey1_hex = lines[1]
        aes.subkey0_bin = format_to_bit(aes.subkey0_hex)
        aes.subkey1 = format_to_bit(aes.subkey1_hex)
        if aes.subkey0_bin is None or aes.subkey1 is None:
            raise Exception("The generation of subkeys was unsuccessful. Please refer to the 'report.pdf' file for further information.")
        if len(aes.subkey0_bin) < 128:
            aes.subkey0_bin = '0' + aes.subkey0_bin
        if len(aes.subkey1) < 128:
            aes.subkey1_bin = '0' + aes.subkey1_bin

    @staticmethod
    def get_message():  
        '''
        This code assigns the plaintext message to the AES object by reading it from a file in ASCII format and then converting it to binary.
        '''                                                  
        with open(aes.plaintext_path, 'r') as f:
            message_plaintext = f.read().strip()
            print()
            print("Margi_Amin_m15219371")
            print()
            print('Message is: ' + message_plaintext)
        aes.message_ascii = to_ascii(message_plaintext)

        aes.message_bit = format_ascii_to_bit(aes.message_ascii)

        aes.message_hex = format_to_hex(aes.message_bit)
        print('Message in hex-form: ' + aes.message_hex)
        if aes.message_bit is None:
            raise Exception('The plaintext message could not be obtained. Please refer to the "report.pdf" file for further details.')

    @staticmethod
    def check_OS_and_files():        
        if aes.platform == "win32" or aes.platform == "win64":
            if not os.path.exists(PLAINTEXT_PATH):
                raise Exception('Please ensure that the message to be encrypted is stored in the following file path: "...\data\plaintext.txt".')
            aes.plaintext_path = PLAINTEXT_PATH
            if not os.path.exists(SUBKEY_PATH):
                raise Exception('Please ensure that the subkey is stored in the following file path: "...\data\subkey_example.txt".')
            aes.subkey_path = SUBKEY_PATH
            aes.result_path = RESULT_PATH
            aes.result_dir = RESULT_DIR

    @staticmethod
    def generate_2_subkeys():  
        '''
        This code generates the first two subkeys for the AES algorithm based on a 128-bit encryption key.
        '''                                     
        key = aes.subkey0_hex
        chunks = [key[x:x + 8] for x in range(0, len(key), 8)]
        w0 = chunks[0]
        w1 = chunks[1]
        w2 = chunks[2]
        w3 = chunks[3]

        temp = (2) % len(w3)        #Shift left 1 byte
        gw3 = w3[temp:] + w3[: temp]
        gw3_list = [gw3[i:i + 2] for i in range(0, len(gw3), 2)]    #Create into list
        gw3_list = aes_Obj.sub_bytes_key(gw3_list)
        gw3 = ''.join(gw3_list)
        temp = '40' #Constant in binary 01000000
        gw3 = hex((to_hex(gw3) ^ to_hex(temp)))

        w4 = hex(((to_hex(w0)) ^ (to_hex(gw3))))[2:]
        w5 = hex(((to_hex(w4)) ^ (to_hex(w1))))[2:]
        w6 = hex(((to_hex(w5)) ^ (to_hex(w2))))[2:]
        w7 = hex(((to_hex(w6)) ^ (to_hex(w3))))[2:]

        key1 = []
        key1.append(w4)
        key1.append(w5)
        key1.append(w6)
        key1.append(w7)
        print()
        print("(Additional Task for CS6053) The subkey schedule algorithm in AES can be used to generate the next subkey based on the first subkey (Subkey0): ")
        print(key1)
        outF = open(aes.result_path, "w")
        for line in key1:
            outF.write(line)
            outF.write("\n")
        outF.close()

        return

    @staticmethod
    def sub_bytes_key(list):                                
        '''
        Each byte in the State can be substituted with its corresponding AES_S_BOX value.
        '''        
        list_to_ret = []
        listnp = np.array(list)
        for x in listnp:
            first = x[0]
            second = x[1]
            first = int(first)
            second = int(to_hex(second))
            new1 = AES_S_BOX[first, second]
            list_to_ret.append((hex(new1))[2:])
        return list_to_ret

    @staticmethod
    def results():

        output = []
        for line in aes.initial_state:
            output.append(str(line))
        outF = open(aes.result_dir, "w")
        outF.write(str(output))
        outF.close()

    @staticmethod
    def do_round():                                   
        '''
        These are the operations that will be executed in each round of AES.
        '''    
        aes_Obj.check_OS_and_files()
        aes_Obj.get_message()
        aes_Obj.get_subkeys()
        aes_Obj.get_initial_state()
        aes_Obj.get_subkey_matrix_0()
        aes_Obj.get_subkey_matrix_1()
        aes_Obj.add_key_0()  # With subkey 0
        aes_Obj.sub_bytes()
        aes_Obj.shift_rows()
        aes_Obj.mix_columns()
        aes_Obj.add_key_1()  # With subkey 1
        aes_Obj.results()
        aes_Obj.generate_2_subkeys()                                #This is the function meant for graduate school students. These keys are not used it is just to show the operation


        return


def to_hex(hexdig):                                                 
    '''
    Convert a string hex value to literal hex value
    '''
    return int(hexdig, 16)


def to_ascii(string):                                               
    '''
    Convert a string value to ASCII value
    '''
    char_list = list(string)
    asc_arr = []
    for char in char_list:
        ascii_val = ''.join(str(ord(c)) for c in char)
        asc_arr.append(ascii_val)
    return asc_arr


def format_ascii_to_bit(text):                                      
    '''
    Convert an ascii value to hex value
    '''
    char_list = list(text)
    bit_arr = []
    for char in char_list:
        binary = format(int(char), 'b').zfill(8)
        bit_arr.append(binary)
    str = ''
    joins = str.join(bit_arr)
    return joins


def format_to_hex(bit):                                             #Convert a bit value to a hexadecimal value
    hex_val = hex(int(bit, 2))[2:]
    return hex_val


def format_to_bit(hex):                                             #Convert a hexadecimal value to a bit value
    bit_val = bin(int(hex, SCALE))[2:].zfill(NUM_BITS)
    return bit_val


def script_execute():                                               #Executes our AES algorithm
    aes_Obj.do_round()


if __name__ == '__main__':
    try:
        aes = aes_Obj()
        script_execute()

    except:
        print(traceback.format_exc())
        sys.stdout.flush()
        sys.exit(1)