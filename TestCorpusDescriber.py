#!/usr/bin/env python3

import os.path

from GenericWidgets import Frame, Root, Checkbutton, Button, Entry, Label
from GenericWidgets import Listbox, FileDialog, Toplevel
from Corpus import TestCorpus, Firmware, FirmwareSection

class TestCorpusDescriberWindow(Frame):
	def __init__(self, parent, coordinator=None):
		# Call the parent constructors
		super(TestCorpusDescriberWindow, self).__init__(parent, fill=True)

		# Initialize class variables
		self.coordinator = coordinator
		self.firmwareDict = dict() # firmware objects by key basename
		self.sectionDict = dict() # section objects by key bounds

		# Setup the window objects
		# First, the firmware list
		self.__firmwareList = Listbox(self,
				listChangeCallback=self._firmwareSelectionChangeCallback)
		self.__firmwareList.grid({"row": 0, "column": 0, "rowspan": 10,
				"sticky": "nswe"})

		# The buttons that manage the firmware list - in their own frame
		self.__firmwareButtonFrame = Frame(self)
		self.__firmwareButtonFrame.grid({"row": 10, "column": 0})

		self.__deleteFirmwareButton = Button(self.__firmwareButtonFrame,
				text="Delete", callback=self._deleteFirmwareButtonCallback)
		self.__deleteFirmwareButton.grid({"row": 0, "column": 0})

		self.__addFirmwareButton = Button(self.__firmwareButtonFrame,
				text="Add", callback=self._addFirmwareButtonCallback)
		self.__addFirmwareButton.grid({"row": 0, "column": 2})
		
		# Second, the section list
		self.__sectionList = Listbox(self,
				listChangeCallback=self._sectionSelectionChangeCallback)
		self.__sectionList.grid({"row": 0, "column": 1, "rowspan": 9,
				"sticky": "nsew"})

		# The buttons that manage the section list - in their own frame
		self.__sectionListButtonFrame = Frame(self)
		self.__sectionListButtonFrame.grid({"row": 9, "column": 1, "rowspan": 2})

		self.__sectionStartEntry = Entry(self.__sectionListButtonFrame, width=4)
		self.__sectionStartEntry.grid({"row": 0, "column": 0})
		self.__sectionEndEntry = Entry(self.__sectionListButtonFrame, width=4)
		self.__sectionEndEntry.grid({"row": 0, "column": 1})

		self.__addSection = Button(self.__sectionListButtonFrame, text="Add",
				callback=self._addSectionCallback)
		self.__addSection.grid({"row": 1, "column": 0})

		self.__deleteSection = Button(self.__sectionListButtonFrame,
				text="Delete", callback=self._deleteSectionCallback)
		self.__deleteSection.grid({"row": 1, "column": 1})

		# Lastly, the properties box
		# First the global config options, in their own frame
		self.__globalOptionsFrame = Frame(self, highlight=True)
		self.__globalOptionsFrame.grid({"row": 0, "column": 2, "rowspan": 4,
				"sticky": "nsew"})

		self.__globalSettingsLabel = Label(self.__globalOptionsFrame,
				text="Global Settings")
		self.__globalSettingsLabel.grid({"row": 0, "column":0, "columnspan": 3})

		self.__corpusNameLabel = Label(self.__globalOptionsFrame,
				text="Corpus Name:")
		self.__corpusNameLabel.grid({"row": 1, "column": 0})
		self.__corpusNameEntry = Entry(self.__globalOptionsFrame)
		self.__corpusNameEntry.grid({"row": 1, "column": 1, "columnspan": 2})

		self.__corpusDescriptionLabel = Label(self.__globalOptionsFrame,
				text="Description:")
		self.__corpusDescriptionLabel.grid({"row": 2, "column": 0})
		self.__corpusDescriptionEntry = Entry(self.__globalOptionsFrame)
		self.__corpusDescriptionEntry.grid({"row": 2, "column": 1, "columnspan": 2})

		# Next the firmware options in their own frame
		self.__firmwareOptionsFrame = Frame(self, highlight=True)
		self.__firmwareOptionsFrame.grid({"row": 4, "column": 2, "rowspan": 4, 
				"sticky": "nsew"})

		self.__firmwareSettingsLabel = Label(self.__firmwareOptionsFrame,
				text="Firmware Settings")
		self.__firmwareSettingsLabel.grid({"row": 0, "column":0, "columnspan": 3})

		self.__firmwareNameLabel = Label(self.__firmwareOptionsFrame,
				"Firmware Name:")
		self.__firmwareNameLabel.grid({"row": 1, "column": 0})
		self.__firmwareNameEntry = Entry(self.__firmwareOptionsFrame)
		self.__firmwareNameEntry.grid({"row": 1, "column": 1, "columnspan": 2})

		self.__firmwareFileNameLabel = Label(self.__firmwareOptionsFrame,
				text="Firmware File:")
		self.__firmwareFileNameLabel.grid({"row": 2, "column": 0})
		self.__firmwareFileNameEntry = Entry(self.__firmwareOptionsFrame)
		self.__firmwareFileNameEntry.grid({"row": 2, "column": 1, "columnspan": 2})

		# Next the section options in their own frame
		self.__sectionOptionsFrame = Frame(self, highlight=True)
		self.__sectionOptionsFrame.grid({"row": 8, "column": 2, "rowspan": 2,
				"sticky": "nsew"})

		self.__sectionSettingsLabel = Label(self.__sectionOptionsFrame,
				text="Section Settings")
		self.__sectionSettingsLabel.grid({"row": 0, "column":0, "columnspan": 3})

		self.__sectionFiletypeLabel = Label(self.__sectionOptionsFrame,
				"Section Filetype:")
		self.__sectionFiletypeLabel.grid({"row": 1, "column": 0})
		self.__sectionFiletypeEntry = Entry(self.__sectionOptionsFrame)
		self.__sectionFiletypeEntry.grid({"row": 1, "column": 1,
				"columnspan": 2})

		# Lastly the buttons that manage the config
		self.__globalButtonFrame = Frame(self)
		self.__globalButtonFrame.grid({"row": 10, "column": 2})

		self.__writeConfigButton = Button(self.__globalButtonFrame,
				text="Write Config", callback = self._writeConfigButtonCallback)
		self.__writeConfigButton.grid({"row": 0, "column": 0})

	def getCorpusOutputFile(self):
		"""Return the filename to save the config to."""
		fd = FileDialog(self)
		return fd.getFilenameToSave()

	def getDefinedCorpus(self):
		"""Return the corpus described by the GUI."""
		# Store off the current screen entries into their appropriate filetype
		curSelection = self.__firmwareList.getSelected()
		if len(curSelection) > 0:
			self._storeCurrentFirmwareEntries(curSelection[0])
		# Build the corpus object
		name = self.__corpusNameEntry.text
		description = self.__corpusDescriptionEntry.text
		corpus = TestCorpus(name, description)
		for firmwareKey in self.firmwareDict:
			corpus.appendFirmware(self.firmwareDict[firmwareKey])
		return corpus

	def _clearFirmwareScreenEntries(self):
		self.__firmwareNameEntry.text = ""
		self.__firmwareFileNameEntry.text = ""
		self.sectionDict = dict()
		self.__sectionList.populate(list())
		self._clearSectionScreenEntries()

	def _clearSectionScreenEntries(self):
		self.__sectionFiletypeEntry.text = ""

	def _firmwareSelectionChangeCallback(self, oldSelection, newSelection):
		"""Gets called when the firmware listbox selection changes."""
		# Save the data on screen as the old file type
		if len(oldSelection) > 0:
			self._storeCurrentFirmwareEntries(oldSelection[0])

		self._clearFirmwareScreenEntries()
	
		# Load the new selection file type data to screen
		if len(newSelection) > 0:
			firmware = self.firmwareDict[newSelection[0]]
			self.__firmwareNameEntry.text = firmware.name
			self.__firmwareFileNameEntry.text = firmware.filename
			# Generate the section dictionary
			self.sectionDict = dict([(sec.bounds, sec) for sec in firmware.sections])
			self.__sectionList.populate(list(self.sectionDict.keys()))

	def _sectionSelectionChangeCallback(self, oldSelection, newSelection):
		"""Gets called when the section listbox selection changes."""
		# Save the data on screen as the old file type
		if len(oldSelection) > 0:
			self._storeCurrentSectionEntries(oldSelection[0])
	
		# Load the new selection file type data to screen
		if len(newSelection) > 0:
			section = self.sectionDict[newSelection[0]]
			self.__sectionFiletypeEntry.text = section.filetype
		else:
			self.__sectionFiletypeEntry.text = ""

	def _storeCurrentFirmwareEntries(self, firmwareKey):
		"""Store the current screen info into the firmwareDict, at the key."""
		curSelection = self.__sectionList.getSelected()
		if len(curSelection) > 0:
			self._storeCurrentSectionEntries(curSelection[0])
		firmwareDef = dict()
		firmwareDef["Name"] = self.__firmwareNameEntry.text
		firmwareDef["Filename"] = self.__firmwareFileNameEntry.text
		firmwareDef["Sections"] = list(self.sectionDict.values())
		self.firmwareDict[firmwareKey] = Firmware(firmwareDef)

	def _storeCurrentSectionEntries(self, sectionKey):
		"""Store the current section info on the screen."""
		if sectionKey in self.sectionDict:
			sectionDef = self.sectionDict[sectionKey]
			sectionDef.filetype = self.__sectionFiletypeEntry.text
			self.sectionDict[sectionKey] = sectionDef

	def _deleteFirmwareButtonCallback(self):
		# Delete the selected firmware
		firmware = self.__firmwareList.getSelected()
		self.__firmwareList.removeSelected()
		for fw in firmware:
			self.firmwareDict.pop(fw)
		self._clearFirmwareScreenEntries()

	def _addFirmwareButtonCallback(self):
		# If firmware was entered in the box that isn't already on screen, add it
		fd = FileDialog(self)
		firmwareName = fd.getFilenameToOpen()
		firmwarePath = os.path.realpath(firmwareName)
		basename = os.path.basename(firmwarePath)
		if (firmwareName != "") and (basename not in self.firmwareDict):
			self.firmwareDict[basename] = Firmware({"Name": basename,
					"Filename": firmwarePath})
			self.__firmwareList.append(basename)

	def _deleteSectionCallback(self):
		"""Delete the selected section."""
		curSelection = self.__sectionList.getSelected()
		self.__sectionList.removeSelected()
		for sec in curSelection:
			self.sectionDict.pop(sec)
		self._clearSectionScreenEntries()

	def _addSectionCallback(self):
		"""Add a section to the section list."""
		setupDict = dict()
		setupDict["Start"] = int(self.__sectionStartEntry.text)
		setupDict["End"] = int(self.__sectionEndEntry.text)
		fw = FirmwareSection(setupDict)
		if fw.bounds not in self.sectionDict:
			self.sectionDict[fw.bounds] = fw
			self.__sectionList.append(fw.bounds)

	def _writeConfigButtonCallback(self):
		# Tell the coordinator to write out the configuration
		self.coordinator.outputCorpus()


class TestCorpusDescriberCoordinator():
	def __init__(self, window=None):
		# Initialize class variables
		self.window = window

	def outputCorpus(self):
		corpus = self.window.getDefinedCorpus()
		outputFile = self.window.getCorpusOutputFile()
		if outputFile != "":
			corpus.writeOut(outputFile)

class TestCorpusDescriberSubwindow(Toplevel):
	def __init__(self, parent, closeCallback=None):
		super(TestCorpusDescriberSubwindow, self).__init__(parent,
				title="Firmware Disassembler - Test Corpus Describer",
				closeCallback=closeCallback)

		# Initialize the subsystem
		self.coordinator = TestCorpusDescriberCoordinator()
		self.window = TestCorpusDescriberWindow(parent=self,
				coordinator=self.coordinator)
		self.coordinator.window = self.window

class TestCorpusDescriber(Root):
	def __init__(self):
		super(TestCorpusDescriber, self).__init__(
				title="Firmware Disassembler - Test Corpus Describer")

		# Initialize the subsystem
		self.coordinator = TestCorpusDescriberCoordinator()
		self.window = TestCorpusDescriberWindow(parent=self,
				coordinator=self.coordinator)
		self.coordinator.window = self.window

		self.window.mainloop()

if __name__ == "__main__":
	testCorpusDescriber=TestCorpusDescriber()
