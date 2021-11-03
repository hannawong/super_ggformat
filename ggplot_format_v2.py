r_str = '''ggplot() +
  geom_ribbon(data = ribbon, aes(ymin = min, ymax = max, x = x.ribbon, fill = 'lightgreen')) +
  geom_line(data = ribbon, aes(x = x.ribbon, y = avg, color = 'black')) +
  geom_line(data = data, aes(x = x, y = new.data, color = 'red')) +
  scale_fill_identity(name = 'the fill', guide = 'legend', labels = c('m1')) +
  scale_colour_manual(name = 'the colour', values = c('black' = 'black', 'red' = 'red'),values = c('black' = 'black', 'red' = 'red'),values = c('black' = 'black', 'red' = 'red'),values = c('black' = 'black', 'red' = 'red'),values = c('black' = 'black', 'red' = 'red'),values = c('black' = 'black', 'red' = 'red'),
    labels = c('c2', 'c1')) +
  xlab('x') +
  ylab('density')'''

alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_1234567890"


def insert_str(str,npos,insert):
    prev_str = str[:npos]
    post_str = str[npos:]
    return prev_str+insert+post_str


def prologue(full_str):
    str_list = full_str.split("\n")
    for i in range(len(str_list)):
        if str_list[i] == "":
            continue
        if "#" in str_list[i]:  ### to do: parse annotation, don't remove all blank!
            str_list[i] += "<annot_end>"
        if str_list[i][-1] in alphabet:
            str_list[i] += "@@@@@@@"
    str_collapse = "".join(str_list).replace(" ", "")
    return(str_collapse)


def parse_sentences(str_collapse):
    parse_list = []
    sentences = str_collapse.split("<-")
    for i in range(1, len(sentences)):
        dest =  sentences[i-1].split(")")[-1]   ## the destination of assigning value
        sentences[i-1] = ")".join(sentences[i-1].split(")")[:-1])+")"
        sentences[i] = dest+"<-"+sentences[i]
    if ")" in sentences:
        sentences.remove(")")
    for i in range(len(sentences)):
        sentences[i] = sentences[i].split("@@@@@@@")
        parse_list.extend(sentences[i])

    return parse_list




atom_sentences = []


def parse_small_sentences(large_sentence):
    i = 0
    j = 0
    while(i < len(large_sentence)-1 and j < len(large_sentence)-1):
        if(large_sentence[j]==")" and large_sentence[j+1] in alphabet):
            atom_sentences.append(large_sentence[i:j+1])
            j+=1
            i = j
        else:
            j+=1
    atom_sentences.append(large_sentence[i:len(large_sentence)])


def arrange_sentence_order(atom_sentences):
    sort_atom_sentences = []
    for sentence in atom_sentences:
        if(sentence[:7]=="library"):
            sort_atom_sentences.insert(0,sentence)
        else:
            sort_atom_sentences.append(sentence)
    return sort_atom_sentences


def rearrange_single_ggplot(str):

    i = 0
    while(i<len(str)):
        if(str[i]=="+"):
            if(i < len(str)-1 and str[i+1] != "#"):
                str = insert_str(str,i+1,"\n")
            i+=1
        if(str[i]=="%"):
            if(i<len(str)-2 and str[i:i+3]=="%>%" and str[i+3] != "#"):
                str = insert_str(str,i+3,"\n")
            i+=1
        if(str[i] == "<"):
            if(i < len(str) - 11 and str[i:i+11] == "<annot_end>"):
                str = insert_str(str,i,"\n")
                str = str.replace("<annot_end>","")
                print(str)
            i = i + 1
        i+=1
    return str

def wrap_long_sentences(sent):
    epoch = len(sent) // 80
    for e in range(1,epoch+1):
        for i in range(len(sent)-80*e,len(sent)):
            if sent[i] == ",":
                sent = insert_str(sent,i+1,"\n"+"\t\t")
                break
    return sent

def final_format(ggplot_sent):
    ggplot_sents = ggplot_sent.split("\n")

    if(len(ggplot_sents)<=1):
        return ggplot_sent
    else:
        for i in range(1,len(ggplot_sents)):
            if len(ggplot_sents[i]) > 80 :
                print(ggplot_sents[i])
                ggplot_sents[i] = wrap_long_sentences(ggplot_sents[i])
            ggplot_sents[i] = "\t"+ggplot_sents[i]

    return "\n".join(ggplot_sents)


All_sentence = []
str_collapse = prologue(r_str)

sentences = parse_sentences(str_collapse)

for sentence in sentences:
    parse_small_sentences(sentence)
sort_sentence = arrange_sentence_order(atom_sentences)

for sentence in sort_sentence:
    rearrange_ggplot = rearrange_single_ggplot(sentence)
    All_sentence.append(rearrange_ggplot)

for sentence in All_sentence:
    formated_sent = final_format(sentence)
    print(formated_sent+"\n")