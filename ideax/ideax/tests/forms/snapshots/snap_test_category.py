# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCategoryForm.test_max_ptbr 1'] = {
    'description': [
        'Ensure this value has at most 200 characters (it has 201).'
    ],
    'title': [
        'Ensure this value has at most 50 characters (it has 51).'
    ]
}
