import nltk
import json
import random
from spellbee.score_data import scores

def load_pangram_data() -> dict:
    """ Loads the contents of pangram.json into pangram dict and return it """

    file_path = 'pangram.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_all_words() -> list:
    """ Returns a list of all words in english dictionary """ 
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    all_words = [word for word in english_vocab if "s" not in word]

    return all_words

def get_alphabet_weights() -> dict:
    """ Returns a dictionary containing probability weights for each letter based on their occurence in english vocabular""" 
    file_path = 'letter_weights.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def check_15_words(letters: list, inner: str) -> bool:
    """ """
    count_of_words = 0
    words = []
    for word in get_all_words():
        if inner not in word:
            continue
        for letter in word:
            if letter not in letters:
                continue
        count_of_words += 1
        words.append(word)

        if count_of_words >= 15:
            print(count_of_words)
            print(words)
            return True
    return False


def generate_letters_for_spellbee(pangram, alphabet_weight) -> (str, list, str):
    """ """  
    vowels = ['a', 'e', 'i', 'o', 'u']
    inner_found = False
    vowel_present_in_choice = False

    while not vowel_present_in_choice:
        choice = random.choice(list(pangram.keys()))  # choice is one of the pangram words
        for vowel in vowels:
            if vowel in choice:
                vowel_present_in_choice = True

    while not inner_found:
        inner_choice = random.choice(list(choice))
        if alphabet_weight[inner_choice] > float(1.0):
            inner_found = True
            choice_set = set(choice)
            choice_set.remove(inner_choice)
            return choice, choice_set, inner_choice
        


def is_valid_word(word: str, inner_letter: str, outer_letters: list[str]) -> bool:
    """ """
    word = word.lower()
    inner_letter= inner_letter.lower()
    outer_letters = [letter.lower() for letter in outer_letters]

    all_words = get_all_words()
    if len(word) < 4:
        return False
    if inner_letter not in word:
        return False
    for letter in word:
        if (letter not in outer_letters) and letter != inner_letter :
            return False
        
    if word in all_words:
        return True
    else:
        return False

def score_word(word: str, current_score: int) -> int:
    """ """
    pangram = load_pangram_data()

    if word in pangram:
        current_score += 15
    # elif => logic for scoring rare words 
    elif len(word) == 4:
        current_score += 1
    else:
        current_score += len(word)
    
    return current_score

def check_duplicate(word, session_id) -> bool:
    """ Returns True if word has already been scored for the same session """

    if word in scores.get(session_id, {}).get('scored_words', []):
        return True
    return False




def initialize_session():
    pass
    # Generate a new session_id
    # Generate outer_letters and inner_letter 
    # Set score to 0
    # Initialize scored_words = []

    