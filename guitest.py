#
# guitest
# StoryGeneration
#
# Created by Nehir Poyraz on 16.12.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.

import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import *
import generator as gen
import random
import nltk
import ssl
from collections import Counter
import plan
import numpy as np
import pickle


START='1.0'


class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack(fill='both', expand='yes')
		self.data = gen.load('data.csv')
		self.rake_samples = gen.generate(self.data, 5)
		self.corpus = plan.load_tagged_corpus('taggedcorpus')
		self.tags = plan.tagged_words(self.corpus)
		self.tokens = nltk.Text(word for (word, tag) in self.tags)
		self.noundict = plan.findtags_prefix('NN', self.tags)
		self.plantitles = [word[0] for word in sorted(self.noundict['NN'])]
		self.adjdict = self.load_dictionary('adjdict.pkl')
		self.avdict = self.load_dictionary('avbdict.pkl')
		self.nndict = self.load_dictionary('nndict.pkl')
		self.vbdict = self.load_dictionary('vbdict.pkl')
		self.similars = self.load_dictionary('similardict.pkl')
		self.pair_dicts = [self.similars, self.adjdict, self.vbdict, self.avdict, self.nndict]

		# self.create_widgets_rake()

		# self.create_widgets_plan()
		self.create_widgets()

	def load_dictionary(self, dictfile):
		with open(dictfile, 'rb') as file:
			dictionary = pickle.load(file)
		return dictionary


	def create_widgets(self):
		self.master.title('Storyline Planning')
		# self.master.geometry("140x40")
		self.LabelFrame = Frame(master=self.master)

		self.rake_LblFrame = Frame(master=self.LabelFrame)
		self.static_lblFrame = Frame(master=self.LabelFrame)
		self.rake_LblFrame.pack(side=LEFT)
		self.static_lblFrame.pack(side=RIGHT)

		self.rake_label = Label(master=self.rake_LblFrame, text='RAKE Storyline Planning')
		self.static_label = Label(master=self.static_lblFrame, text='Static Storyline Planning')
		self.rake_label.pack()
		self.static_label.pack()

		self.responsiveFrame = Frame(master=self.master)
		self.responsive_rake = Frame(master=self.responsiveFrame)
		self.responsive_static = Frame(master=self.responsiveFrame)
		self.rake_examples = [story['title'] for story in self.rake_samples]
		self.static_examples = np.random.choice(self.plantitles, 5)

		self.rake_example = StringVar(master=self.responsive_rake)
		self.rake_example.set(self.rake_examples[0])
		self.static_example = StringVar(master=self.responsiveFrame)
		self.static_example.set(self.static_examples[0])
		self.rakeOpts = OptionMenu(self.responsive_rake, self.rake_example, *self.rake_examples)
		# self.rakeOpts.grid(column=0)
		self.rake_storylineBtn = Button(self.responsive_rake, text='Extract', command=self.display_rake_story_line)
		# self.rake_storylineBtn.grid(column=0)
		self.rake_randomBtn = Button(master=self.responsive_rake, text='Random', command=self.displayrandomstory_line)
		# self.rake_randomBtn.grid(column=0)
		self.rake_refreshBtn = Button(master=self.responsive_rake, text='Refresh', command=self.refreshBtn)
		# self.rake_refreshBtn.grid(column=0)
		self.staticOpts = OptionMenu(self.responsive_static, self.static_example, *self.static_examples)
		# self.staticOpts.grid(column=1)
		self.static_storylineBtn = Button(self.responsive_static, text='Extract', command=self.display_static_storyline)
		# self.static_storylineBtn.grid(column=1)
		self.static_randomBtn = Button(master=self.responsive_static, text='Random',
									   command=self.display_random_static_storyline)
		# self.static_randomBtn.grid(column=1)
		self.static_refreshBtn = Button(master=self.responsive_static, text='Refresh', command=self.refreshBtn_plan)

		self.rakeOpts.pack()
		self.rake_storylineBtn.pack()
		self.rake_randomBtn.pack()
		self.staticOpts.pack()
		self.static_storylineBtn.pack()
		self.static_refreshBtn.pack()
		self.static_randomBtn.pack()

		self.responsive_rake.pack(side=LEFT)
		self.responsive_static.pack(side=RIGHT)

		self.storyFrame = Frame(master=self.master)
		self.static_storyFrm = Frame(master=self.storyFrame)
		self.rake_storyFrm = Frame(master=self.storyFrame)
		self.rake_storytext = Text(master=self.rake_storyFrm, wrap=WORD, width=70, height=10, padx=10, pady=10)
		self.rake_storytext.pack()
		self.static_storytext = Text(master=self.static_storyFrm, wrap=WORD, width=70, height=10, padx=40, pady=10)
		self.static_storytext.pack()
		self.rake_storyFrm.pack(side=LEFT)
		self.static_storyFrm.pack(side=RIGHT)

		self.storylineFrame = Frame(master=self.master)
		self.rake_storylinetext = Text(master=self.storylineFrame, wrap=WORD, width=70, height=5)
		self.static_storylinetext = Text(master=self.storylineFrame, wrap=WORD, width=70, height=5)

		self.rake_storylinetext.pack(side=LEFT)
		self.static_storylinetext.pack(side=RIGHT)

		self.quitBtn = Button(master=self.master, text="QUIT", fg="red", command=self.master.destroy)

		self.LabelFrame.pack()
		self.responsiveFrame.pack()
		self.storyFrame.pack()
		self.storylineFrame.pack()
		self.quitBtn.pack(side=BOTTOM)

	def display_static_storyline(self, **kwargs):
		self.static_storylinetext.delete(START, END)
		if kwargs and kwargs['random']:
			title = random.choice(self.plantitles)
		else:
			title = self.static_example.get()
		storyline = []
		for dictionary in self.pair_dicts:
			storyline.append(dictionary.get(title, "Null"))
		# storyline = plan.plan_storyline(self.tags, title)
		self.static_storylinetext.insert(INSERT, title + "\n\n")
		size = len(storyline)
		for i in range(size):
			self.static_storylinetext.insert(INSERT, storyline[i])
			if i < size - 1:
				self.static_storylinetext.insert(INSERT, " --> ")


	def display_random_static_storyline(self):
		return self.display_static_storyline(random=True)


		# self.editArea = tkst.ScrolledText(master=self.master, wrap=WORD, width=20, height=10)

	def display_rake_story_line(self, **kwargs):
		self.rake_storytext.delete(START, END)
		self.rake_storylinetext.delete(START, END)
		if kwargs and kwargs['random']:
			story = gen.generate(self.data, 1)[0]
		else:
			for story in self.rake_samples:
				if story['title'] == self.rake_example.get():
					break
		self.rake_storytext.insert(INSERT, story['title'] + "\n\n")
		tags = {'keyword1': 'red', 'keyword2': 'green', 'keyword3': 'blue', 'keyword4': 'purple', 'keyword5': 'orange'}
		size = len(story['line'])
		for i in range(size):
			sl = story['line'][i]
			t = story['text'][i]
			# if sl in t:
			sli = t.lower().index(sl)
			slen = len(story['line'][i])
			tag = 'keyword' + str(i + 1)
			self.rake_storytext.insert(INSERT, t[:sli])
			self.rake_storytext.insert(INSERT, t[sli:sli+slen], tag)
			self.rake_storytext.insert(INSERT, t[sli+slen:] + "\n")
			self.rake_storylinetext.insert(INSERT, story['line'][i], tag)
			if i < size - 1:
				self.rake_storylinetext.insert(INSERT, " --> ")
				# tag = 'keyword'+str(i+1)
				# self.text.tag_add(tag, float(keyindex[i][0]), float(keyindex[i][1]))
		# self.storytext.insert(INSERT, "\n")
		# for i in range(size):
		# 	self.storytext.insert(INSERT, story['line'][i], 'keyword' + str(i + 1))
		# 	if i < size - 1:

		# 		self.text.insert(INSERT, " --> ")
		for tag in tags:
			self.rake_storytext.tag_configure(tag, foreground=tags[tag])
			self.rake_storylinetext.tag_configure(tag, foreground=tags[tag])


	def displayrandomstory_line(self):
		# print(data.shape)
		return self.display_rake_story_line(random=True)

	def refreshBtn(self):
		self.rakeOpts['menu'].delete(0, END)
		self.rake_samples = gen.generate(self.data, 5)
		self.rake_examples = [story['title'] for story in self.rake_samples]
		for example in self.rake_examples:
			self.rakeOpts['menu'].add_command(label=example, command=tk._setit(self.rake_example, example))
		self.rake_example.set(self.rake_examples[0])

	def refreshBtn_plan(self):
		self.staticOpts['menu'].delete(0, END)
		self.static_examples = np.random.choice(self.plantitles, 5)
		for example in self.static_examples:
			self.staticOpts['menu'].add_command(label=example, command=tk._setit(self.static_example, example))
		self.static_example.set(self.static_examples[0])



root = Tk()
app = Application(master=root)
app.mainloop()

