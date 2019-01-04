import heapq
import pickle
import argparse
import os
import time
import string
import hashlib 

class CompareFiles():
    
    def __init__(self,filename):
        self.filename = filename
    
    def SHA256(filename):
        
        file = open(filename,"r", encoding="utf-8-sig")
        str = file.read()
        file.close()
        
          
        # encoding str using encode() 
        # then sending to SHA256() 
        result = hashlib.sha256(str.encode()) 
          
        # returning the equivalent hexadecimal value. 
                
        return result.hexdigest()
    
#################################################### 
 # to find probability of words and create word dictionary
       
class WordCount():

    def __init__(self):
        
        # dictionary holding the word count
        self.dictWordCount = {}
        self.fd = 0
        self.str = ""

        pass

    def getWordCount(self, filePath):
        
        self.fd = self.openFile(filePath)
        self.str = self.fd.read()

        word = ""
        for eachChar in (self.str):
            
            if eachChar in string.ascii_letters:
                word = word + eachChar
            else:

                # check if the word is in the dictionary
                if(word != ""):
                    self.updateDict(word)
                    word = ""
                self.updateDict(eachChar)    
                
                    
        
        # For the cases when a file ends with [a-z A-Z]                
        if(word != ""):
            self.updateDict(word)
        WordCount = {}  
        
        value_list = self.dictWordCount.values()
        length = sum(value_list)
           
        for key , values in self.dictWordCount.items():
            value = values/length
            WordCount[key] = value
        
        return WordCount , self.str

        pass

    def updateDict(self, word):

        if word not in self.dictWordCount:
            self.dictWordCount[word] = 1
        else:
            self.dictWordCount[word] = self.dictWordCount.get(word) + 1

        pass

    def openFile(self, filePath):
        fd = open(filePath, "r", encoding="utf-8-sig")
        return fd

#################################################### 
# to find character probabilities
        
class CharCount():

    def __init__(self,file_name):
        self.file_name = file_name
        pass
    
    def readChar(file_name):
        char_dict = {}
        file = open(file_name)
        text = file.read()
        file.close()
    
        for char in text:
            if char not in char_dict:
                char_dict[char] = 1
            else:
                char_dict[char] = char_dict[char]+ 1
        
        total_characters = 0
        for key,value in char_dict.items():
            total_characters += value
    
        char_probability = {}
    
        for char,frequency in char_dict.items():
            probability = frequency/total_characters
            char_probability[char] = probability
            
        return char_probability,text


#################################################### 
# create node objects
        
class HuffmanNodeObject(object):
    
    def __init__(self, char, prob):
        self.char = char
        self.prob = prob
        self.left = None
        self.right = None

    def __eq__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob == other.prob

    def __ne__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob != other.prob

    def __lt__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob < other.prob

    def __le__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob <= other.prob

    def __gt__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob > other.prob

    def __ge__(self, other):
        return HuffmanNodeObject.CheckObject(other) and self.prob >= other.prob

    @staticmethod
    def CheckObject(other):
        if other is None:
            return False
        if not isinstance(other, HuffmanNodeObject):
            return False
        return True

    def __repr__(self):
        return "Char[%s]->Freq[%s]" % (self.char, self.prob)

#################################################### 
# implement huffman coding algorithm
        
class HuffmanAlgorithm:
    
    def  __init__(self,char_probability,text,filename,symbolmodel):
        self.char_probability = char_probability
        self.text = text
        self.filename = filename
        self.symbolmodel = symbolmodel
        
    def HuffmanCode(char_probability,text,filename,symbolmodel): 
        
        # start timer to build symbol model
        t0 = time.clock()
        
    # to construct nodes of tree
        heap = []
        for char, prob in char_probability.items():
            heapq.heappush(heap, HuffmanNodeObject(char, prob))
            
    # to get the two lowest probability character nodes and create new node
    # and put it back in the heap
    # Repeat this process until all the Huffman trees are combined into one
            
        while len(heap) > 1:
            node_1 = heapq.heappop(heap)
            node_2 = heapq.heappop(heap)
            merged = HuffmanNodeObject(None, node_1.prob + node_2.prob)
            merged.left = node_1   
            merged.right = node_2
            heapq.heappush(heap, merged)
        
        # to build codes for each character
        codes, reverse_mapping = {}, {}
        codes, reverse_mapping = HuffmanAlgorithm.BuildCode(codes, reverse_mapping, heapq.heappop(heap))
        
        
        # end timer for creating symbol model
        t1 = time.clock()
        time_duration = t1 - t0
        print("time duration to build symbol model= ",time_duration,"sec")
         
        # start timer for encoding given symbol model
        t2 = time.clock()   
        
        if(symbolmodel == 'char'):
            # to find the encoded text for char symbol model
            encoded_text = ''.join([codes[char] for char in text])
        else:
            word = ""
            l = list()
            for char in text:
                #print(char)
                if char in string.ascii_letters:
                    word = word + char
                else:
                     if(word != ""):
                         l.append(codes[word])
                         word = ""   
                     l.append(codes[char])
                         
            if(word != ""):
                l.append(codes[word])
            
            encoded_text = ''.join(l)     
            
        
        # add padding at the end if there are arbitrary number of bits in length
        extra_pad = 8 - len(encoded_text) % 8
        padding_info = "{0:08b}".format(extra_pad)
    
        # to build the padded encoded text containing padding information
        
        padded_encoded_text =  padding_info + encoded_text + ''.join(["0"] * extra_pad) 
        
        
        # convert the padded_encoded_text into byte to write in binary file
        
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text is not properly padded")
        code_array = bytearray()  # store information as array of bytes for padded_encoded_text
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]  # Reading byte by byte
            #print("BYTE:",byte)
            code_array.append(int(byte, 2))
        
        WriteToBinFile = bytes(code_array)  # bytes() makes the code_array immutable
        
        # end timer for encoding input file
        t3 = time.clock()
        time_duration = t3 - t2
        print("time duration to encode the input file given the symbol model= ",time_duration,"sec")
        
        # write in .bin file
        OutFileName = filename + '.bin'
        OutputFile = open(OutFileName,'wb')
        OutputFile.write(WriteToBinFile)
        OutputFile.close()
        
             
        # create .pkl file to store symbol model
        PickleFileName = filename + '-symbol-model.pkl'
        PickleFile = open(PickleFileName,'wb') 
        pickle.dump(reverse_mapping,PickleFile) 
        PickleFile.close()
        
        return PickleFile, OutputFile
        
   
#################################################### 
    # to build codes
     
    def BuildCode(codes, reverse_mapping, root, current=''):
        if root is not None:
            if root.char is not None:
                codes[root.char] = current
                reverse_mapping[current] = root.char
                #print("CODES:",codes)
                return
            HuffmanAlgorithm.BuildCode(codes, reverse_mapping, root.left, current + "0")
            HuffmanAlgorithm.BuildCode(codes, reverse_mapping, root.right, current + "1")
        return codes, reverse_mapping


####################################################  
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("-s", "--symbolmodel", choices=["char","word"])
    args = parser.parse_args()
    symbolmodel = args.symbolmodel
    infile = args.infile


    (root,file) = os.path.splitext(infile)
    if (args.symbolmodel == 'char'):
        char_probability,text = CharCount.readChar(infile)
        PickleFile, OutputFile = HuffmanAlgorithm.HuffmanCode(char_probability,text,root,symbolmodel)
        
    else:
        wc = WordCount()
        word_dict, text = wc.getWordCount(infile)
        PickleFile, OutputFile = HuffmanAlgorithm.HuffmanCode(word_dict,text,root,symbolmodel)
        
    

