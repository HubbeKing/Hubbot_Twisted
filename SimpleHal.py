#!/usr/bin/python
# A simple implimentation of MegaHAL - Markov conversation simulator
#
#
# Copyright (c) 2010 WptNgm@gmail.com
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import sys
import pickle
import random 

class SimpleHAL(object):

  # initializer
  def __init__(self, order=4, max_word=75):
    self.n = order
    self.max = max_word
    self.forward = dict()
    self.backward = dict()
 

  # public methods
  # respond() operate the user input and the respond to it
  def respond(self, input, reply=True, learn=True):

    if not input:
      return 'No input entered!'

    # must learn before reply
    if learn:
      self._learn(input)

    if reply:
      return self._reply(input)

    return # in any cases


  # save HAL data
  def save(self, file="hal.db"):

    try:
      fp = open(file, 'wb')
      pickle.dump(self.n, fp)
      pickle.dump(self.forward, fp)
      pickle.dump(self.backward, fp)
      fp.close()
    except Exception, e:
      print "Error saving HAL data to file %s:" % file
      raise Exception, e
 

  # load HAL data
  def load(self, file="hal.db"):

    try:
      fp = open(file, 'rb')
      self.n = pickle.load(fp)
      self.forward = pickle.load(fp)
      self.backward = pickle.load(fp)
      fp.close()
    except Exception, e:
      print "Error loading HAL data from file %s:" % file
      raise Exception, e


  # maybe, these are private methods
  # tokenize() process the user input
  # to the token words
  def _tokenize(self, text):

    return text.split(" ")


  # learn() read input text and add them to both 
  # forward and backford model dict 
  def _learn(self, text):

    words = self._tokenize(text)

    if len(words) <= self.n:
      # fill to extend short word
      words.extend( [' ']*(self.n-len(words)+1) )

    # add forward
    self._add_markov_chain(self.forward, words)
    # add backward
    words.reverse()
    self._add_markov_chain(self.backward, words)


  # reply() read input text and reply with possible 
  # gerated Markov random text 
  def _reply(self, input):

    # TODO: at current state, HAL just randomly
    # choose a key as the starting state.
    # Figure out, how to search for the key
    # that relavent to user input

    words = self._tokenize(input)
    # find the possible keys that
    # relavent to input
    all_possible_keys = []
    for word in words:
      key = self._find_key(self.forward, word)
      if key:
        all_possible_keys.extend(key)

    #print all_possible_keys

    # find the starting point
    try:
      seed = random.choice(all_possible_keys)
    except IndexError:
      return 'I am utterly speechless!'

    # generate random sentence with seed
    output = self._generate_sentence(seed)

    str = ' '.join(output)

    if not str:
      return 'I am utterly speechless!'

    return str

  # generate Markov sentence
  def _generate_sentence(self, seed):
    
    tmp = []
    start = seed
    # forward Markov chain
    output = self._get_markov_chain(self.forward, start)
    if output:
      tmp = output[self.n:] #+ ' [' + ' '.join(start) + ']'

    # backward Markov chain
    start = list(seed)
    start.reverse()
    start = tuple(start)
    output = self._get_markov_chain(self.backward, start)
    output.reverse()
    if output:
      output.extend(tmp)

    return output
 

  # add the Markov chain of the specific words
  # into the model dict
  def _add_markov_chain(self, model, words):

    for i in range(len(words) - self.n):

      key = tuple(words[i:i+self.n])
      next = words[i+self.n] 

      if key in model:
        model[key].append(next)
      else:
        model[key] = [next]


  # get the generated markov text of the specific model dict
  def _get_markov_chain(self, model, start):

    current = start
    output = list(current)

    for i in range(self.max):
      if current in model:
        possible_next = model[current]
        next = random.choice(possible_next)
        output.append(next)
        current = tuple(output[-self.n:])
      else:
        break

    return output


  # find key from input
  def _find_key(self, dict, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dict.iteritems() if val in k]
