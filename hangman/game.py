from .exceptions import *
import random


class GuessAttempt(object):
    new_word = ""
    def __init__(self, guess, hit=False, miss=False):
        self.hit = hit
        self.miss = miss
        self.guess = guess
        if self.hit == True and self.miss== True:
            raise InvalidGuessAttempt
        
            
    def is_hit(self):
        return self.hit
        
    def is_miss(self):
        return self.miss

class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer.lower()
        self.masked = '*' * len(self.answer)
        if not answer:
            raise InvalidWordException
            
   
     
    def perform_attempt(self, guess):
        self.guess = guess.lower()
        if len(self.guess) > 1:
            raise InvalidGuessedLetterException
         
        if self.guess not in self.answer:
            return GuessAttempt(self.guess, miss=True)
        
        new_word = ""
    
        for i in range(len(self.answer)):
            if self.answer[i] == self.guess:
                new_word += self.answer[i]
            else:
                new_word += self.masked[i]
                
        self.masked = new_word
        

        return GuessAttempt(self.guess, hit=True)
                
        
            


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
        
    def is_won(self):
        return self.word.masked == self.word.answer
    
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
        
    def guess(self, char):
        self.char = char.lower()
        if self.char in self.previous_guesses:
            raise InvalidGuessedLetterException()
            
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(self.char)
        
        attempt = self.word.perform_attempt(self.char)
        
        if self.char not in self.word.answer:
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException()
            
        if self.is_lost():
            raise GameLostException()
            
        return attempt
        
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
