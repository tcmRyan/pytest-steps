"""
==========
pytest_steps
==========

py.test plugin to generate test steps based off the docstrings.  The intent is to enable create a
human readable version of the test steps.  This will allow other plugins to do things like send
your test steps to a test case management system.

Usage
-------
"""

import pytest
import inspect
import re


def get_multiline_comments(func):
    comment_pattern = re.compile(r'""".*?"""|\'\'\'.*?\'\'\'', re.DOTALL)
    source = inspect.getsource(func)
    return comment_pattern.findall(source)



class PytestSteps(object):

    def pytest_itemcollected(self, item):
        print self.extract_steps(item.function.__doc__)

    @pytest.hookimpl(tryfirst=True)
    def pytest_report_teststatus(self, report):
        pass

    def extract_steps(self, infostr):
        """
        Parse the docstring to return the list of steps
        :param infostr:
        :return list:
        """
        return [infostr]


def pytest_addoption(parser):
    """
    Parse command line parameters.
    :param parser:
    :return:
    """
    parser.addoption('--collect-steps', action="store_true", dest="collect_steps", default=False,
                     help='Sets if pytest should collect test steps from docstrings')

def pytest_configure(config):
    steps_enable = config.getoption('collect_steps')
    if steps_enable:
        config.pluginmanager.register(PytestSteps(), 'steps')