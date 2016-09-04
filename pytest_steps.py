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

class PytestSteps(object):
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_report_teststatus(self, item, call, __multicall__):
        report = __multicall__.execute()
        setattr(item, "rep_" + report.when, report)
        if report.when == 'call':
            report.test_steps = self.extract_steps(item.function.__doc__)
        return report

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
    group = parser.getgroup('collect steps')
    group.addoption('--collect-steps', action="store_true", dest="collect_steps", default=False,
                     help='Sets if pytest should collect test steps from docstrings')

def pytest_configure(config):
    steps_enable = config.getoption('collect_steps')
    if steps_enable:
        config.pluginmanager.register(PytestSteps(), 'steps')