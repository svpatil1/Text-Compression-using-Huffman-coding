# Text-Compression-using-Huffman-coding

###### Implementation:

def HuffmanCode(char_probability,text,filename,symbolmodel):
-	Construct nodes of the tree and store it in the object.
-	Select 2 symbols with minimum probability using heapq.heappop and merge them repeatedly until they are combined into one.
-	Build a tree of the above process: Created a HuffmanNodeObject class and used objects to maintain tree structure.
-	Assign code to characters by recursively traversing the tree.
-	Encode the input text. 
-	Pad encoded text if the length is not the multiple of 8.
-	Store the padding information in 8 bits and add this to the beginning of the encoded text.
-	Make byte array.
-	Write the byte array to binary(.bin) file.

###### Performance Evaluation:
   Here I have used “heapq” data structure to build the Huffman tree.  The advantage of using this data structure is that each time when “heappop(heap)” is used , the smallest of the heap elements is popped. Hence, we do not have to maintain sorted list as we remove elements with smallest probabilities. Moreover, when the element is pushed or popped the heap structure is always maintained with heap[0] to be the smallest element each time.
   
   To check the integrity between the input .txt file and the file recovered after decompression, SHA256 supported by hashlib library in python is used. If the hex value for the original text file is equal to the file recovered after decompression, then there is no data loss observed and the file has been correctly decompressed.
   
    Table 1 shows the evaluation parameters for word and char based symbol model w.r.t “mobydick.txt” file.

###### TABLE 1: Evaluation table

Parameters | Char based symbol model | Word based symbol model
------------ | ------------- | -------------
Time to build symbol model | 0.000637 sec | 0.26 sec
Time to encode the input file | 0.34 sec | 0.35 sec
Time to decode the compressed file | 1.88 sec | 1.10 sec
Size of symbol model | 2,042 bytes | 8,58,499 bytes
Size of .bin file after compression | 6,90,361 bytes | 3,92,563 bytes
Size of original .txt file | 12,20,150 bytes | 12,20,150 bytes 

