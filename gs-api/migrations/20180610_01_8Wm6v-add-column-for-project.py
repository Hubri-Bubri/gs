"""
Add column for project
"""

from yoyo import step

__depends__ = {'20180522_01_hvWDs-add-table-project'}

steps = [
    step("""
        ALTER TABLE project ADD `status_set` text, ADD `type` text
        """,
        "ALTER TABLE project DROP COLUMN status_set, type"
    )
]