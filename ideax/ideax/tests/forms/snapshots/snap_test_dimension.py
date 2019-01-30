# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestDimensionForm.test_max_ptbr 1'] = {
    'description': [
        'Ensure this value has at most 500 characters (it has 501).'
    ],
    'title': [
        'Ensure this value has at most 200 characters (it has 201).'
    ]
}
