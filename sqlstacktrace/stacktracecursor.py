"""Module for substitution database cursors.
"""

from django.db.backends.utils import CursorWrapper
from django.utils.encoding import smart_text

from .stacktrace import get_stacktrace


class StacktraceCursorWrapper(CursorWrapper):
    """Wrapper for substitution the CursorWrapper.
    Added to SQl-query a comment with python stack trace.
    """
    def execute(self, sql, params=()):
        try:
            stacks = get_stacktrace()
            stacktrace = []
            for stack in stacks:
                stacktrace.append(
                    u"""File "{0}", line {1}, in {2}\n\t{3}""".format(
                        *[smart_text(stack_data) for stack_data in stack]).replace("%", "%%"))
            stacktrace = "\n".join(stacktrace)
            stacktrace = stacktrace.replace('/*', '\/\*').replace('*/', '\*\/')
        except:
            stacktrace = u"WITHOUT STACKTRACE"
        sql = u"{sql} \n/* {stacktrace} \n*/".format(stacktrace=stacktrace, sql=smart_text(sql))
        return self.cursor.execute(sql, params)
