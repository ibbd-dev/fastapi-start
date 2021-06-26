# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module implements the Requests API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: Apache2, see LICENSE for more details.
"""
import fire


class Calculator(object):
    """A simple calculator class.\n
    more
    """

    def double(self, number):
        """
        函数注释
        :param
        """
        return 2 * number


def hello():
    """
    函数注释1
    函数注释2
    """


if __name__ == '__main__':
    fire.Fire({'hello': hello})
