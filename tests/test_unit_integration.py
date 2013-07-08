import subprocess
import unittest

import cricket

from cricket.pytest import test_discoverer
from cricket.pytest import test_executor

class TestCollection(unittest.TestCase):

    def test_testCollection(self):
        '''
        Confirm that the pytest discovery mechanism is capable of
        finding this test
        '''

        PTD = test_discoverer.PyTestDiscoverer()
        PTD.collect_tests()
        tests = str(PTD).split('\n')

        test_found = False
        for test in tests:
            test_found |= 'test_testCollection' in test
        self.assertTrue(test_found)

if __name__ == '__main__':
    unittest.main()


class TestDiscoverer(unittest.TestCase):

    def test_function_naming(self):
        '''
        Confirm the test discoverer can strip the useful name out of the pytest
        output
        '''

        sample_input = '''<TestCaseFunction 'test_testCollection'>'''
        expected = 'test_testCollection'
        found = cricket.pytest.test_discoverer.get_fname(sample_input)

        self.assertEqual(expected, found)


class TestExecutorCmdLine(unittest.TestCase):

    def test_labels(self):
        '''
        Test that the command-line API is respecting the labels
        being targetted for testing
        '''

        labels = ['tests.test_unit_integration.TestCollection']
        cmdline = ['python', '-m', 'cricket.pytest.test_executor'] + labels

        runner = subprocess.Popen(
            cmdline,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )  

        output = ''
        for line in runner.stdout:
            output += line

        assert 'tests.test_unit_integration.TestCollection' in output
        assert 'tests.test_unit_integration.TestExecutorCmdLine' not in output




# This is a magic test which can be un-commented and run manually.
# It recursively calls the text executor, and fouls up normal
# output, so it had to be disabled as I am not smart enough
# to actually understand and fix the issue

# class TestExecutor(unittest.TestCase):

#     def test_suite_execution(self):
#         '''
#         Note, it's hard to test full suite discovery because
#         it will include this test and infinite loop. So just
#         testing on a single test until I can figure out something
#         smarter.
#         '''

#         run_only = [
#             'tests.test_unit_integration.TestDiscoverer'
#         ]
        
#         PTE = test_executor.PyTestExecutor()
#         PTE.run_only(run_only)
#         PTE.stream_results()