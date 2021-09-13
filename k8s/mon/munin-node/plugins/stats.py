# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

class Field(object):
	name = None
	label = None
	min = 0
	max = None
	draw = None
	derive = False
	value = None

	def __init__(self, name):
		self.name = mon.cleanfn(name)

	def _config(self, colour):
		if self.label is None:
			print(f"{self.name}.label {self.name}")
		else:
			print(f"{self.name}.label {self.label}")
		print(f"{self.name}.colour COLOUR{colour}")
		print(f"{self.name}.draw {self.draw}")
		print(f"{self.name}.min {self.min}")
		if self.max is not None:
			print(f"{self.name}.max {self.max}")
		if self.derive:
			print(f"{self.name}.type DERIVE")
			print(f"{self.name}.cdef {self.name},1000,/")
		else:
			print(f"{self.name}.type GAUGE")

	def _report(self):
		if self.value is None:
			print(f"{self.name}.value U")
		else:
			print(f"{self.name}.value {self.value}")

class Graph(object):
	name = None
	title = None
	base = 1000
	lower = 0
	upper = None
	category = None
	vlabel = None
	scale = False
	__f = dict()

	def __init__(self, name):
		self.name = mon.cleanfn(name)

	def add(self, field):
		self.__f[field.name] = field

	def _config(self):
		print(f"multigraph {self.name}")
		print(f"graph_title {self.title}")
		g_args = f"--base {self.base} -l {self.lower}"
		if self.upper is not None:
			g_args += f" -u {self.upper}"
		print(f"graph_args {g_args}")
		print(f"graph_category {self.category}")
		print(f"graph_vlabel {self.vlabel}")
		if self.scale:
			print('graph_scale yes')
		else:
			print('graph_scale no')
		fc = 0
		for n in sorted(self.__f.keys()):
			self.__f[n]._config(fc)
			fc += 1
			if fc > 28:
				fc = 0

	def _report(self):
		print(f"multigraph {self.name}")
		for n in sorted(self.__f.keys()):
			self.__f[n]._report()

class Config(object):
	__g = dict()

	def add(self, graph):
		self.__g[graph.name] = graph

	def print(self):
		for n in sorted(self.__g.keys()):
			self.__g[n]._config()
			if mon.debug: print()

class Report(object):
	__g = dict()

	def add(self, graph):
		self.__g[graph.name] = graph

	def print(self):
		for n in sorted(self.__g.keys()):
			self.__g[n]._report()
			if mon.debug: print()
