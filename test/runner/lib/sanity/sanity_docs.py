"""Sanity test for documentation of sanity tests."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from lib.sanity import (
    SanitySingleVersion,
    SanityMessage,
    SanityFailure,
    SanitySuccess,
    sanity_get_tests,
)

from lib.config import (
    SanityConfig,
)

from lib.data import (
    data_context,
)


class SanityDocsTest(SanitySingleVersion):
    """Sanity test for documentation of sanity tests."""
    ansible_only = True

    @property
    def can_ignore(self):  # type: () -> bool
        """True if the test supports ignore entries."""
        return False

    @property
    def can_skip(self):  # type: () -> bool
        """True if the test supports skip entries."""
        return False

    # noinspection PyUnusedLocal
    def test(self, args, targets):  # pylint: disable=locally-disabled, unused-argument
        """
        :type args: SanityConfig
        :type targets: SanityTargets
        :rtype: TestResult
        """
        sanity_dir = 'docs/docsite/rst/dev_guide/testing/sanity'
        sanity_docs = set(part[0] for part in (os.path.splitext(os.path.basename(path)) for path in data_context().content.get_files(sanity_dir))
                          if part[1] == '.rst')
        sanity_tests = set(sanity_test.name for sanity_test in sanity_get_tests())

        missing = sanity_tests - sanity_docs

        results = []

        results += [SanityMessage(
            message='missing docs for ansible-test sanity --test %s' % r,
            path=os.path.join(sanity_dir, '%s.rst' % r),
        ) for r in sorted(missing)]

        if results:
            return SanityFailure(self.name, messages=results)

        return SanitySuccess(self.name)
