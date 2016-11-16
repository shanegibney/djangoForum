import unittest
import testFile
suite = unittest.TestLoader().loadTestsFromModule(testFile)
unittest.TextTestRunner().run(suite)
