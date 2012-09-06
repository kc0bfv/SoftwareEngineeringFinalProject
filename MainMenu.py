#!/usr/bin/env python3

from GenericWidgets import Frame, Root, Button, Image
import Icon
from TrainingCorpusDescriber import TrainingCorpusDescriberSubwindow
from TestCorpusDescriber import TestCorpusDescriberSubwindow

class MainMenuWindow(Frame):
	def __init__(self, parent, coordinator=None):
		# Call the parent constructors
		super(MainMenuWindow, self).__init__(parent, fill=True)

		# Initialize class variables
		self.coordinator = coordinator

		# Setup the window objects
		self.__icon = Image(self, imagedata=Icon.iconData)
		self.__icon.grid({"row": 0, "column": 0, "rowspan": 5})

		self.__invokeTesterButton = Button(self, text="Invoke Tester",
				callback=self.__testerButtonCallback)
		self.__invokeTesterButton.grid({"row": 0, "column": 1, "rowspan": 2,
				"sticky": "nsew"})

		self.__invokeTrainerButton = Button(self, text="Invoke Trainer",
				callback=self.__trainerButtonCallback)
		self.__invokeTrainerButton.grid({"row": 0, "column": 2, "rowspan": 2,
				"sticky": "nsew"})
		
		self.__invokeTestCorpusDescButton = Button(self, text="Invoke Test" + 
				"\nCorpus Describer", callback=self.__testCorpusButtonCallback)
		self.__invokeTestCorpusDescButton.grid({"row": 2, "column": 1,
				"rowspan": 2, "sticky": "nsew"})
		
		self.__invokeTrainCorpusDescButton = Button(self, text="Invoke Training"+ 
				"\nCorpus Describer", callback=self.__trainCorpusButtonCallback)
		self.__invokeTrainCorpusDescButton.grid({"row": 2, "column": 2,
				"rowspan": 2, "sticky": "nsew"})

		self.__invokeFWDisassemblerButton = Button(self,
				text="Firmware Disassembler",
				callback=self.__fwDisassemblerButtonCallback)
		self.__invokeFWDisassemblerButton.grid({"row": 4, "column": 1,
				"columnspan": 2, "rowspan": 2, "sticky": "nsew"})

	def __testerButtonCallback(self):
		self.coordinator.invokeTester()

	def __trainerButtonCallback(self):
		self.coordinator.invokeTrainer()

	def __testCorpusButtonCallback(self):
		self.coordinator.invokeTestCorpusDesc()

	def __trainCorpusButtonCallback(self):
		self.coordinator.invokeTrainCorpusDesc()

	def __fwDisassemblerButtonCallback(self):
		self.coordinator.invokeFirmwareDisassembler()

class MainMenuCoordinator():
	def __init__(self, window=None):
		# Initialize class variables
		self.window = window
		self.tester = None
		self.trainer = None
		self.trainingCorpusDescriber = None
		self.testCorpusDescriber = None
		self.firmwareDisassembler = None

	def invokeTester(self):
		pass

	def invokeTrainer(self):
		pass

	def invokeTestCorpusDesc(self):
		if self.testCorpusDescriber is None:
			self.testCorpusDescriber = TestCorpusDescriberSubwindow(
					self.window,
					closeCallback=self._testCorpusDescriberClosedCallback)

	def invokeTrainCorpusDesc(self):
		if self.trainingCorpusDescriber is None:
			self.trainingCorpusDescriber = TrainingCorpusDescriberSubwindow(
					self.window,
					closeCallback=self._trainingCorpusDescriberClosedCallback)

	def invokeFirmwareDisassembler(self):
		pass

	def _trainingCorpusDescriberClosedCallback(self):
		self.trainingCorpusDescriber = None

	def _testCorpusDescriberClosedCallback(self):
		self.testCorpusDescriber = None

class MainMenu(Root):
	def __init__(self):
		super(MainMenu, self).__init__(title="Firmware Disassembler - Main Menu")

		# Initialize the subsystem
		self.coordinator = MainMenuCoordinator()
		self.window = MainMenuWindow(parent=self, coordinator=self.coordinator)
		self.coordinator.window = self.window

		self.window.mainloop()

if __name__ == "__main__":
	mainMenu=MainMenu()
