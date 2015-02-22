# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: PATRICK HUSTON

"""

import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string """
    return ''.join(random.sample(s,len(s)))

def get_complement(nucleotide):
    """ Returns the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    complements = {'A':'T', 'T':'A', 'C':'G', 'G':'C'} #Creates dictionary for nucleotide pairs
    return complements[nucleotide]

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    complement = ""
    for char in dna:
        complement += get_complement(char)
    return (complement)[::-1] #Uses power of slice functionality with step size of -1 from start to end to reverse the complementary string

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATGAGACGACAGATATAG")
    'ATGAGACGACAGATA'
    >>> rest_of_ORF("ATGA")
    'ATGA'
    """
    stop_codons = ["TAG","TAA","TGA"]
    output = ""
    for i in range(0,len(dna),3):
        if(dna[i:i+3] not in stop_codons):
            output += dna[i:i+3]
        else:
            break
    return output

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """

    orfs = []
    while(len(dna) >= 3):
        while(dna[:3] != 'ATG' and len(dna) >= 3):
            dna = dna[3:]
        if(len(dna)<3):
            pass
        to_add = rest_of_ORF(dna)
        if(len(to_add)>=3):
            orfs.append(to_add)
        dna = dna[len(to_add):]

    return orfs

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    >>> find_all_ORFs("ATGGATGCATGATCATAGCCATACTAATAGATG")
    ['ATGGATGCA', 'ATG', 'ATGCATGATCATAGCCATACTAATAGATG', 'ATGATCATAGCCATACTAATAGATG']
    """
    return find_all_ORFs_oneframe(dna) + find_all_ORFs_oneframe(dna[1:]) + find_all_ORFs_oneframe(dna[2:])
    
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    >>> longest_ORF("ATGGATGCATAATGATTTATAG")
    'ATGCATAATGATTTA'
    """
    return max(find_all_ORFs_both_strands(dna),key=len)

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF 

        No appropriate doctest can be written for this function; due to the random
        nature of the shuffle, it is impossible to expect a consistent result with
        every call to longest_ORF_noncoding. Approximately, the value should be in the
        700 length range.
        """
    long_ORF = ""
    for i in range(num_trials):
    	dna_shuffle = shuffle_string(dna) #Creates new shuffle of dna, if longest orf in that shuffle is longer than previous max, set max to new value
    	if len(longest_ORF(dna_shuffle)) > len(long_ORF):
    		long_ORF = longest_ORF(dna_shuffle)
    return long_ORF

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
        >>> coding_strand_to_AA('TTTTTCTTATTGTCTTCCTCATCGTATTACTGTTGCTGGCTTCTCCTACTG')
        'FFLLSSSSYYCCWLLLL'
    """
    aa_dict = {'TTT':'F','TTC':'F','TTA':'L','TTG':'L','TCT':'S','TCC':'S','TCA':'S','TCG':'S','TAT':'Y','TAC':'Y','TGT':'C','TGC':'C','TGG':'W','CTT':'L','CTC':'L','CTA':'L','CTG':'L','CCT':'P','CCC':'P','CCA':'P','CCG':'P','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','CGT':'R','CGC':'R','CGA':'R','CGG':'R','ATT':'I','ATC':'I','ATA':'I','ATG':'M','ACT':'T','ACC':'T','ACA':'T','ACG':'T','AAT':'N','AAC':'N','AAA':'K','AAG':'K','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GTT':'V','GTC':'V','GTA':'V','GTG':'V','GCT':'A','GCC':'A','GCA':'A','GCG':'A','GAT':'D','GAC':'D','GAA':'E','GAG':'E','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}
    translated = ''
    for i in range(0,len(dna),3):
        if(len(dna[i:i+3]) == 3):
            translated += aa_dict[dna[i:i+3]]
    return translated

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.

        No appropriate doctests can be written for this function - the result can and
        most likely will vary with each call, because longest_ORF_noncoding is 
        inherently not consistent in its return values, due to the random nature
        of the shuffle.
    """
    max_len = len(longest_ORF_noncoding(dna, 1500))
    return sorted([coding_strand_to_AA(orf) for orf in find_all_ORFs_both_strands(dna) if len(orf) >= max_len], key=len, reverse=True) #Returns reverse length sorted list of all translated genes that are longer than threshold

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    result = gene_finder(load_seq("./data/X73525.fa"))
    print "Here is the result:" 
    for translated_protein in result:
        print translated_protein
