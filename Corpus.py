import json

class Corpus:

	"""
		A superclass for Test and Training Corpus.  This should really do more...

		Public Functions:
			Corpus.writeOut(filename) - write the corpus out to a file
		"""

	def writeOut(self, filename):
		"""Write the corpus out to a file."""
		with open(filename, "w") as outputFile:
			json.dump(self._toDict(), outputFile)

	def _toDict(self):
		raise NotImplementedError("Corpus must be inherited.")


class TestCorpus(Corpus):

	"""
		TestCorpus stores the test corpus configuration.

		Public parameters:
			name - the corpus name
			description - a brief description of the corpus
			firmwareDefinitions - a list of Firmware objects, with info about each
				firmware in the test corpus
		"""

	def __init__(self, name="", description="", filename=None):
		"""Construct a test corpus

			Supply filename if you wish to load from a file
			Otherwise, name each parameter
			"""
		self.name = name
		self.description = description
		self.firmwareDefinitions = list()
		if filename is not None:
			# Load the configuration
			config = dict()
			with open(filename, 'r') as testConfigFile:
				config = json.load(testConfigFile)

			# Separate out the important parts for ease
			if "Name" in config:
				self.name = config["Name"]
			if "Description" in config:
				self.description = config["Description"]
			if "Firmware Definitions" in config:
				for fwDef in config["Firmware Definitions"]:
					self.appendFileType(fwDef)

	def _toDict(self):
		"""Return a dictionary representation of the test corpus."""
		outputDict = dict()
		outputDict["Name"] = self.name
		outputDict["Description"] = self.description
		
		fwDefs = list()
		for fwDef in self.firmwareDefinitions:
			fwDefs.append(fwDef._toDict())

		outputDict["Firmware Definitions"] = fwDefs
		return outputDict

	def appendFirmware(self, firmware):
		"""Append a firmware to the corpus.
			
			firmware may be a Firmware object, or something the Firmware constructor
			can handle - like a dictionary representing a Firmware
			"""
		if isinstance(firmware, Firmware):
			self.firmwareDefinitions.append(firmware)
		else:
			self.firmwareDefinitions.append(Firmware(firmware))

class Firmware:

	"""
		Firmware stores one firmware object and its sections

		Public parameters:
			name - a user friendly name for the firmware
			filename - the path to the firmware
			sections - a list of firmware sections
		"""

	def __init__(self, firmwareDef):
		self.name = ""
		self.filename = ""
		self.sections = list()

		if "Name" in firmwareDef:
			self.name = firmwareDef["Name"]
		if "Filename" in firmwareDef:
			self.filename = firmwareDef["Filename"]
		if "Sections" in firmwareDef:
			for section in firmwareDef["Sections"]:
				self.appendFirmwareSection(section)

	def _toDict(self):
		outputDict = dict()
		outputDict["Name"] = self.name
		outputDict["Filename"] = self.filename

		outputDict["Sections"] = list()
		for section in self.sections:
			outputDict["Sections"].append(section._toDict())

		return outputDict

	def appendFirmwareSection(self, section):
		if isinstance(section, FirmwareSection):
			self.sections.append(section)
		else:
			self.sections.append(FirmwareSection(section))

class FirmwareSection:

	"""
		Firmware section describes the bounds and filetype of a segment.

		Public parameters:
			bounds - a tuple of form (start, end), describing bounds.  Bounds are
				of the form [start, end) - the "end" byte is not actually within the
				segment, it's the "start" byte of the next segment
			length - the number of bytes in the segment, it's (end-start)
			filetype - a string specifying the filetype
		"""
		
	def __init__(self, sectionDef):
		self.bounds = (0,0)
		self.filetype = ""

		if ("Start" in sectionDef) and ("End" in sectionDef):
			self.bounds = (sectionDef["Start"], sectionDef["End"])
		if "Filetype" in sectionDef:
			self.filetype = sectionDef["Filetype"]

	def __len__(self):
		return self.bounds[1]-self.bounds[0]

	length = property(__len__)

	def _toDict(self):
		outputDict = dict()
		outputDict["Start"] = self.bounds[0]
		outputDict["End"] = self.bounds[1]
		outputDict["Filetype"] = self.filetype
		return outputDict

class TrainingCorpus(Corpus):

	"""
		TrainingCorpus stores the training corpus configuration.

		Public parameters:
			name - the corpus name
			description - a brief description of the corpus
			nValue - the n value specified in the corpus description
			filetypeDefinitions - a list of FileType objects, with info about each
				filetype in the training corpus
		"""

	def __init__(self, name="", description="", nValue=1, filename=None):
		"""Construct a training corpus
			Supply filename if you wish to load from a file
			Otherwise, name each parameter
			"""
		self.name = name
		self.description = description
		self.nValue = nValue
		self.filetypeDefinitions = list()

		if filename is not None:
			# Load the configuration
			config = dict()
			with open(filename, 'r') as trainingConfigFile:
				config = json.load(trainingConfigFile)

			# Separate out the important parts for ease
			if "Description" in config:
				self.description = config["Description"]
			if "Name" in config:
				self.name = config["Name"]
			if "n Value" in config:
				self.nValue = config["n Value"]
			if "Filetype Definitions" in config:
				for ftDefKey in config["Filetype Definitions"]:
					ftDef = config["Filetype Definitions"][ftDefKey]
					self.appendFileType(ftDef)

	def _toDict(self):
		"""Return a dictionary representation of the training corpus."""
		outputDict = dict()
		outputDict["Name"] = self.name
		outputDict["Description"] = self.description
		outputDict["n Value"] = self.nValue
		
		ftDefs = dict()
		for ftDef in self.filetypeDefinitions:
			ftDefs[ftDef.name] = ftDef._toDict()

		outputDict["Filetype Definitions"] = ftDefs
		return outputDict

	def appendFileType(self, filetype):
		"""Append a filetype to the corpus.
			
			filetype may be a FileType object, or something the FileType constructor
			can handle - like a dictionary representing a FileType
			"""
		if isinstance(filetype, FileType):
			self.filetypeDefinitions.append(filetype)
		else:
			self.filetypeDefinitions.append(FileType(filetype))
	
class FileType:

	"""
		FileType stores the configuration for a single training corpus file type.

		Public parameters:
			name - the name of the filetype
			filetypeFile - the file in which to store the filetype classification data
			ignoreExisting - whether to overwrite the existing file when training
			files - a list of TrainingFile objects, tracking each file in the type
		"""

	def __init__(self, filetypeDef):
		"""Construct a FileType object

			filetypeDef is a dictionary containing fields:
				Name - the name
				Filetype File - the file to store the filetype classification in
				Ignore Existing - whether we should overwrite the existing file
					when training.  This is ignored by some classifiers.
				Files - a list of filenames, or TrainingFile objects
			"""
		# Set defaults
		self.name = ""
		self.filetypeFile = ""
		self.ignoreExisting = False
		self.files = list()

		# Pull out the supplied parameters
		if "Name" in filetypeDef:
			self.name = filetypeDef["Name"]
		if "Filetype File" in filetypeDef:
			self.filetypeFile = filetypeDef["Filetype File"]
		if "Ignore Existing" in filetypeDef:
			self.ignoreExisting = filetypeDef["Ignore Existing"]

		if "Files" in filetypeDef:
			for trainingFile in filetypeDef["Files"]:
				self.appendTrainingFile(trainingFile)

	def _toDict(self):
		outputDict = dict()
		outputDict["Name"]=self.name
		outputDict["Filetype File"] = self.filetypeFile
		outputDict["Ignore Existing"] = self.ignoreExisting
		
		files = list()
		for f in self.files:
			files.append(f.filename)
		
		outputDict["Files"] = files
		return outputDict

	def appendTrainingFile(self, trainingFile):
		if isinstance(trainingFile, TrainingFile):
			self.files.append(trainingFile)
		else:
			self.files.append(TrainingFile(trainingFile))

class TrainingFile:

	"""
		TrainingFile stores the configuration for a file within a filetype

		Public parameters:
			filename - the filename for the training file
		"""

	def __init__(self, filename=""):
		self.filename = filename




class _CorpusTest:
	def __init__(self):
		testObjects = [(TestCorpus, "testTestCorpus.cfg"),
										(TrainingCorpus, "testTrainingCorpus.cfg")]
		for i in testObjects:
			self.testCorpus(i[0], i[1])

	def testCorpus(self, classToTest, filename="TestTrainingCorpus.cfg"):
		tc = classToTest(filename=filename)
		secondFilename = filename+"SECOND"
		tc.writeOut(secondFilename)
		tc2 = classToTest(filename=secondFilename)
		# TODO: run through the objects and make sure it matches what it should
		print("Success, ", filename)

if __name__ == "__main__":
	testCode = _CorpusTest()
