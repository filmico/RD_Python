# Sample final Script

# Check if each word of a sentence ends with an soecified letter


def EndsWithVerif(sentence, letter):
    
    wordsLst = sentence.split()

    # print wordsLst    
    
    for w in wordsLst:
        if (w.endswith(letter)):
            print 'The word ' + w + ' ends with ' + letter
                

            
EndsWithVerif('the fat cat sat on the mat', 't')