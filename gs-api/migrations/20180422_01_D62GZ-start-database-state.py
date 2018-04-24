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
            `image` text NOT NULL,
            `description` text NOT NULL,
            `link` text NOT NULL,
            `label` text NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        """DROP TABLE applications"""
    ),

    # {
    #     applications: [1, 2, 3],
    #     permissions: {
    #         order: [read, write]
    #     }
    # }

    step(
        """
        CREATE TABLE `access` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user` int(11) DEFAULT NULL,
            `permissions` text NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        INSERT `access` VALUES (1, 1, 'first, second');
        """,
        """DROP TABLE access"""
    ),

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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        INSERT `users` VALUES (1, 'demo', 'demo');
        """,
        """DROP TABLE users"""
    )
]
