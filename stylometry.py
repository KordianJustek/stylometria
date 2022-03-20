# coding=utf8
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

LINES = ['-',':','--']
#Style lini do wykresów

def jaccard_test(words_by_author,len_shortest_corpus):
    jaccard_by_author = dict()
    unique_words_unknow = set(words_by_author['unknows'][:len_shortest_corpus])
    authors = (author for author in words_by_author if author != 'unknown')
    for author in authors:
        unique_words_author = set(words_by_author[author][:len_shortest_corpus])
        shared_words = unique_words_author.intersection(unique_words_unknow)
        jaccard_sim = (float(len(shared_words)) / (len(unique_words_author)+ len(unique_words_unknow) - len(shared_words) ) )
        jaccard_by_author[author] = jaccard_sim
        print('Indeks Jaccarda dla klucza {} = {}'.format(author,jaccard_sim))
    most_likley_author = max(jaccard_by_author, key=jaccard_by_author.get)
    print("Biorać pod uwagę prawdopodobienstwo, autorem jest: {} ".format(most_likley_author))

def vocab_test(words_by_author):
    chisquared_by_author = dict()
    for author in words_by_author:
        if author!= 'unknown':
            combined_corpus = (words_by_author[author]+words_by_author['unknown'])
            author_proportion = (len(words_by_author[author]) / len(combined_corpus))
            combined_freq_dist = nltk.FreqDist(combined_corpus)
            most_common_words = list(combined_freq_dist.most_common(1000))
            chisquared = 0
            for word, combined_count in most_common_words:
                observed_count_author = words_by_author[author].count(word)
                excepted_count_author = combined_count * author_proportion
                chisquared += ((observed_count_author - excepted_count_author)**2 / excepted_count_author )
                chisquared_by_author[author] = chisquared
            print('Chi-Kwadrat dla klucza {} = {:.1f}'.format(author,chisquared))
        most_likely_author = min(chisquared_by_author,key=chisquared_by_author.get)
        print('Biorac pod uwage słownictwo,authorem najprowdopodobniej jest: {} .\n'.format(most_likely_author) )



def stopwords_test(words_by_author,len_shortest_corpus):
    #Tworzymy wykres czestotliwosci wystepowania slow nieindeksowanych z ograniczeniem danycj do dlugosci najkrotszego korpusu
    stopwords_by_author_freq_dist = dict()
    plt.figure(2)
    stop_words = set(stopwords.words('english'))
    for i,author in enumerate(words_by_author):
            stopwords_by_author = [word for word in words_by_author[author][:len_shortest_corpus] if word in stop_words ]
            stopwords_by_author_freq_dist[author] = nltk.FreqDist(stopwords_by_author)
            stopwords_by_author_freq_dist[author].plot(50,label=author,linestyle=LINES[i],title='50 Najczesciej uzywanych slow nie indeksowanych')
    plt.legend()
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Słowo")
    plt.savefig('stopwords_test.png')


def parts_of_speech_test(words_by_author,len_shortes_corpus):
    by_author_freq_dist = dict()
    plt.figure(3)
    for i, author in enumerate(words_by_author):
        post_by_author = [pos[1] for pos in nltk.pos_tag(words_by_author[author][:len_shortes_corpus])]
        by_author_freq_dist[author]= nltk.FreqDist(post_by_author)
        by_author_freq_dist[author].plot(35,label=author,linestyle=LINES[i],title='Czesc mowy')

    plt.legend()
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Czesc mowy")
    plt.savefig('parts_of_speech_test.png')

def text_to_string(filename):
    #odczytuje plik tekstowy i zwraca ciag znaków
    with open(filename) as infile:
        return infile.read()

def make_word_dict(string_by_author):
    #Zwraca slownik zawierajacy listy tokenów w postaci slow przypisanyc do odpowieniego autora
    words_by_author = dict()
    for author in string_by_author:
        tokens = nltk.word_tokenize(string_by_author[author])
        words_by_author[author] = ([token.lower() for token in tokens if token.isalpha() ])
    return words_by_author

def find_shortest_corpus(word_by_author):
#zwraca dlugosc najkrótszego korpusu
    word_count = []
    for author in word_by_author:
        word_count.append(len(word_by_author[author]))
        print ('\nLiczba slow dla klucza {} = {}'.format(author,len(word_by_author)))
    len_shortest_corpus = min(word_count)
    print("Długość najkrótszego łańcucha korpusu = {}\n".format(len_shortest_corpus))
    return len_shortest_corpus

def word_lenght_test(words_by_author,len_shortest_corpus):
#Tworzy wykres przedstawiajacy czestotliwość długości slów dla autroa z ograniczeniem danych do długości najkrótszego korpusu
    by_author_lenght_freq_dist = dict()
    plt.figure(1)
    plt.ion()

    for i,author in enumerate(words_by_author):
        word_lenghts = [len(word) for word in words_by_author[author][:len_shortest_corpus]]
        by_author_lenght_freq_dist[author] = nltk.FreqDist(word_lenghts)
        by_author_lenght_freq_dist[author].plot(15,linestyle=LINES[i],label=author,title='Czestotliwosc występowania słów o różnej długości')
    plt.legend()
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Długość słowa")
    plt.savefig('word_lenght_test.png')

def main():
    string_by_author = dict()
    string_by_author['doyle'] = text_to_string('hound.txt')
    string_by_author['wells'] = text_to_string('war.txt')
    string_by_author['unknown'] = text_to_string('lost.txt')

    print(string_by_author['doyle'][:300])

    words_by_author = make_word_dict(string_by_author)
    len_shortest_corpus = find_shortest_corpus(words_by_author)

    word_lenght_test(words_by_author, len_shortest_corpus)
    stopwords_test(words_by_author,len_shortest_corpus)
    parts_of_speech_test(words_by_author, len_shortest_corpus)
    vocab_test(words_by_author)
    #jaccard_test(words_by_author,len_shortest_corpus)

if __name__ == '__main__':
    main()