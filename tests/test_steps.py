from steps import get_multiline_comments


def test_extract_comment_basic():
    def test_docs_strings():
        """First docstring that explains the test setup"""
        assert True
        """ Second Step """
        assert True
        """ Third Step"""
        assert False
        '''Forth Step'''
        assert True

    result = get_multiline_comments(test_docs_strings)
    expected = [
        '"""First docstring that explains the test setup"""',
        '""" Second Step """',
        '""" Third Step"""',
        "'''Forth Step'''"
    ]

    assert result == expected


def test_extract_comment_multiline():
    def test_docs_strings():
        """First docstring that explains the test setup"""
        assert True
        """
        Second Step
        This is my second step

        Wow its got stuff in it
        """
        assert True

    result = get_multiline_comments(test_docs_strings)
    expected = [
        '"""First docstring that explains the test setup"""',
        '''"""
        Second Step
        This is my second step

        Wow its got stuff in it
        """'''
    ]

    assert result == expected

