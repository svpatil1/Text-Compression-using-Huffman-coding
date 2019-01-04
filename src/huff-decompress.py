import pickle
import argparse
import os,time

huffCompress = __import__('huff-compress')

if __name__ == '__main__':
    
    # start timer for decoding
    t0 = time.clock()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    args = parser.parse_args()
    infile = args.infile
    Name,ext = os.path.splitext(args.infile)
    originalFileName = Name + ".txt"
    root,file = os.path.splitext(args.infile)
    PickleFile = root + '-symbol-model.pkl'
    
   # load the symbol model from .pkl file
    with open(PickleFile, "rb") as input_file:
        reverse_mapping = pickle.load(input_file)
    
    
    InputFile = root + '.bin'
    # read .bin file to be decompressed
    file = open(InputFile,'rb')
    
    bit_string = ""
        
    while True:
        byte = file.read(1)
        if not byte:
            # eof
            break
        else:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            
     
    # remove extra padding
    padded_info = bit_string[:8]
    extra_padding = int(padded_info, 2)

    bit_string = bit_string[8:]
    encoded_text = bit_string[:-1 * extra_padding]
    
    current = ""
    decompressed_text = ""
    for bit in encoded_text:
        current += bit
        if (current in reverse_mapping):
            character = reverse_mapping[current]
            decompressed_text += character
            current = ""
            
    
    # write in .txt file
    OutFileName = root + '-decompressed.txt'
    OutputFile = open(OutFileName,'w')
    OutputFile.write(decompressed_text)
    OutputFile.close()
    
    # to check the integrity of files
    compress  = huffCompress.CompareFiles.SHA256(originalFileName)
    print("The hexadecimal equivalent of SHA256 for original file to be compressed is : ", compress)
    decompress = huffCompress.CompareFiles.SHA256(OutFileName)
    print("The hexadecimal equivalent of SHA256 for file after decompression is : ", decompress)
    
    if(decompress == compress):
        print("MESSAGE --> Compressed and decompressed files are equal")
    else:
        print("MESSAGE --> Compressed and decompressed files are not equal")
        
    
    # end timer 
    t1 = time.clock()
    time_duration = t1 - t0
    print("time duration for decoding the compressed file= ",time_duration,"sec")

           
    
    
    
    
    
   