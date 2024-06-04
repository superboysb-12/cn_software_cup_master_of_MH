from nltk.corpus import wordnet
import random
#for the first time you use wordnet
#import nltk
#nltk.download()
#nltk.download('wordnet')


class EDA:
    def __init__(self):
        self.stop_words = []

    def get_synonyms(self,word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        return synonyms

    def synonym_replacement(self,words, n):
        stop_words = []
        new_words = words.copy()
        random_word_list = list(set([word for word in words if word not in stop_words]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonyms = self.get_synonyms(random_word)
            if len(synonyms) >= 1:
                synonym = random.choice(list(synonyms))
                new_words = [synonym if word == random_word else word for word in new_words]
                #print("replaced", random_word, "with", synonym)
                num_replaced += 1
            if num_replaced >= n: #only replace up to n words
                break

        #this is stupid but we need it, trust me
        sentence = ' '.join(new_words)
        new_words = sentence.split(' ')
        return new_words

    def random_deletion(self,words, p = 0.01):

        #obviously, if there's only one word, don't delete it
        if len(words) == 1:
            return words

        #randomly delete words with probability p
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(word)

        #if you end up deleting all words, just return a random word
        if len(new_words) == 0:
            rand_int = random.randint(0, len(words)-1)
            return [words[rand_int]]

        return new_words


    def random_swap(self,words, n):
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)
        return new_words

    def swap_word(self,new_words):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words)-1)
            counter += 1
            if counter > 3:
                return new_words
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words

    def random_insertion(self,words, n):
        new_words = words.copy()
        for _ in range(n):
            self.add_word(new_words)
        return new_words

    def add_word(self,new_words):
        synonyms = []
        counter = 0
        while len(synonyms) < 1:
            random_word = new_words[random.randint(0, len(new_words)-1)]
            synonyms = self.get_synonyms(random_word)
            counter += 1
            if counter >= 10:
                return
        random_synonym = synonyms[0]
        random_idx = random.randint(0, len(new_words)-1)
        new_words.insert(random_idx, random_synonym)
