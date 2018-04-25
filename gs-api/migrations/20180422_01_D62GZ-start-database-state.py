"""
Start database state.
"""

from yoyo import step


__depends__ = {}


steps = [
    step(
        """
        CREATE TABLE `applications` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` text NOT NULL,
            `image` text NULL,
            `description` text NULL,
            `link` text NULL,
            `label` text NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        """DROP TABLE applications"""
    ),

    step("""INSERT `applications` VALUES (1, 'Customer application (A)', null, null, 'http://localhost:8081', null)"""),
    step("""INSERT `applications` VALUES (2, 'Customer application (B)', null, null, 'http://localhost:8082', null)"""),

    step(
        """
        CREATE TABLE `access` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user` int(11) DEFAULT NULL,
            `permissions` text NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        """DROP TABLE access"""
    ),

    step("""INSERT `access` VALUES (null, 1, 'first, second')"""),

    step(
        """
        CREATE TABLE `companies` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `company_name` text,
            `company_id` int(11) DEFAULT NULL,
            `user` int(11) DEFAULT NULL,
            `access` int(11) DEFAULT NULL,
            `application` int(11) DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        """DROP TABLE companies"""
    ),

    step(
        """
        CREATE TABLE `users` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_name` text,
            `password` text,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        """DROP TABLE users"""
    ),

    step("""INSERT `users` VALUES (1, 'demo', 'demo')"""),

    step(
        """
        CREATE TABLE `many_to_many_users_applications` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_id` int(11) NOT NULL,
            `application_id` int(11) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        """DROP TABLE many_to_many_users_applications"""
    ),

    step("""INSERT `many_to_many_users_applications` VALUES (null, 1, 1)"""),
    step("""INSERT `many_to_many_users_applications` VALUES (null, 1, 2)""")
]
