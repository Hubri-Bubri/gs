"""
Start database state.
"""

from yoyo import step

__depends__ = {}


steps = [
    step(
        """CREATE TABLE user (
            id INT,
            login VARCHAR(20),
            password VARCHAR(20),
            PRIMARY KEY (id))
        """,
        """DROP TABLE user"""
    )
]
