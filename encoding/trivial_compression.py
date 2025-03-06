# Description: This file contains a class that compresses a gene sequence into a bit_string and optimizes the memory usage

class CompressedGene():

    def __init__(self, gene: str) -> None:
        self.__compress(gene)


    # Private method to compress a gene sequence into a bit_string
    # In the loop, deslocates the bits of the bit_string to the left by 2 and then adds the bits that represents the nucleotide
    # Initializes the bit_string with 1, to avoid the case where the gene is empty
    # Uses OR operator (sum) to add the bits (0bxxxxx, xxxxx = bits sequence) that represents the nucleotide
    def __compress(self, gene: str) -> None:
        self.bit_string: int = 1
        for nucleotide in gene.upper():
            self.bit_string <<= 2
            if nucleotide == "A":
                self.bit_string |= 0b00
            elif nucleotide == "C":
                self.bit_string |= 0b01
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide: {}".format(nucleotide))
    

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            # deslocates the bits of the bit_string to the right by i and then applies a AND (product) with 0b11 to get the last 2 bits
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError("Invalid bits: {}".format(bits))
        return gene[::-1]
    

    # override __str__ method to return the decompressed gene
    def __str__(self) -> str:
        return self.decompress()
    

if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTT" * 100
    print("Original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)
    print("Compressed is {} bytes".format(getsizeof(compressed.bit_string)))

    # When using print on a object, the __str__ method is called. So, the decompressed gene is returned
    print(compressed)

    print("Original and decompressed are the same: {}".format(original == compressed.decompress()))