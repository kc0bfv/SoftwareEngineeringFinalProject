import tkinter
import tkinter.ttk

# Generic Widgets, abstracting some tkinter

""" class Root
The root object for tkinter
"""
class Root(tkinter.Tk):
	# Constructor
	def __init__(self, title="", closeCallback=None, bringToFront=True):
		super(Root, self).__init__()

		# Initialize class variables
		self.closeCallback = closeCallback

		# Setup the handler for when the window is closed
		self.protocol("WM_DELETE_WINDOW", self.__closeCallbackHandler)
		self.wm_title(title)

		# TODO: does this belong here?
		# If the window needs to be brought to the front
		if bringToFront:
			self.call('wm', 'attributes', '.', '-topmost', '1')
			self.call('wm', 'attributes', '.', '-topmost', '0')

	# The handler for when the user closes the window
	def __closeCallbackHandler(self):
		# If the user specified a window close callback, call it
		if self.closeCallback is not None:
			self.closeCallback()

		# Destroy the root
		self.destroy()

class Frame(tkinter.Frame):
	def __init__(self, parent, packSide="top", fill=True):
		super(Frame, self).__init__(parent)

		packConfig = dict()
		packConfig["side"] = packSide
		if fill:
			packConfig["fill"] = "both"
			packConfig["expand"] = True
		self.pack(packConfig)

class Label(tkinter.Label):
	def __init__(self, parent, text=""):
		super(Label, self).__init__(parent, text=text)

"""	class Button
Builds a UI button within "parent"

Callback function prototype (it's very simple...):
	def callback(self):
		pass
"""
class Button(tkinter.ttk.Button):
	def __init__(self, parent, text="", callback="", pady=None):
		super(Button, self).__init__(parent, text=text)
		self["command"] = callback

class Checkbutton(tkinter.Checkbutton):
	def __init__(self, parent, text="", initialState = False):
		super(Checkbutton, self).__init__(parent, text=text)

		self._state = BooleanVar()	
		self["variable"] = self._state

		self.state = initialState

	# BooleanVar needs get and set called when changing the variable
	# Use a property to just make that work with attribute "state"
	def _get_state(self):
		return self._state.get()
	def _set_state(self, state):
		self._state.set(state)
	state = property(_get_state, _set_state)

class Entry(tkinter.Entry):
	def __init__(self, parent, text="", width=None):
		super(Entry, self).__init__(parent)
		if width is not None:
			self["width"] = width

		self._text = StringVar()
		self["textvariable"] = self._text

		self.text = text
	
	# StringVar needs get and set called when changing the variable
	# Use a property to just make that work with attribute "text"
	def _get_text(self):
		return self._text.get()
	def _set_text(self, text):
		self._text.set(text)
	text = property(_get_text, _set_text)

class Listbox(tkinter.Listbox):
	def __init__(self, parent, mode="browse"):
		# Call the parent constructor
		#		exportselection disables bad behavior when multiple listboxes exist
		super(Listbox, self).__init__(parent, selectmode=mode, exportselection=0)
		self.pack({"side": "top", "fill": "both", "expand": True})

	# Add everything in a list into the listbox - delete the current entries
	def populate(self, items):
		self.delete(0, "end")
		for item in items:
			self.append(item)

	# Append one item to the list
	def append(self, item):
		self.insert("end", item)

	# Remove selected item
	def removeSelected(self):
		self.delete("anchor")

	# Return all items in the listbox
	def getContents(self):
		return self.get(0, "end")

	# Return the selected items in the listbox
	def getSelected(self):
		return self.indicesToItems(self.curselection())

	# Turn an index list into a list of items
	def indicesToItems(self, indexList):
		outList = list()
		if indexList is not None:
			for index in indexList:
				outList.append(self.get(index))
		return outList

class StringVar(tkinter.StringVar):
	pass

class BooleanVar(tkinter.BooleanVar):
	pass

class Image(tkinter.Label):
	def __init__(self, parent, filename=None, imagedata=None):
		self.image = tkinter.PhotoImage(data=imagedata)
		super(Image, self).__init__(parent, image=self.image)
