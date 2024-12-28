def search_with_ret_list(pattern, text):

    M = len(pattern)                                                 #1
    N = len(text)
    
    ret_list = []                                                    #2

    for i_txt in range(0, N - M + 1):                                #3
        j_pat=0

        for j_pat in range (0, M):                                   #4
            if text[i_txt + j_pat] != pattern[j_pat]:
               
                break
    
        if j_pat == M-1 :                                           #5

            print ('Pattern gefunden an Index %d\n' % i_txt)
            ret_list.append(i_txt)

    return ret_list




def search_bitmap(pattern, text):

    M = len(pattern)                                                 #1
    N = len(text)
    bitmap = [0]*len(text)                                                  #2

    for i_txt in range(0, N - M + 1):                                #3
        j_pat=0

        for j_pat in range (0, M):                                   #4
            if text[i_txt + j_pat] != pattern[j_pat]:
               
                break
    
        if j_pat == M-1 :                                           #5

            print ('Pattern gefunden an Index %d\n' % i_txt)
            bitmap[i_txt] = 1

    return bitmap



text = 'ottos mops trotzt\n ottotto: fort mops fort\n ... Ernst Jandl'
pattern = 'otto'

a = search_with_ret_list(pattern, text)  #1

print(a)



