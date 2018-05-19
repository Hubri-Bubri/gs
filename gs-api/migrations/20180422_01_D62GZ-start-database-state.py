from yoyo import step


__depends__ = {}


steps = [
    step(
        """
        CREATE TABLE `application` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` text NOT NULL,
            `description` text NULL,
            `link` text NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE application"
    ),

    step("INSERT `application` VALUES (1, 'Business', NULL, 'http://localhost:8081')"),
    step("INSERT `application` VALUES (2, 'Dashboard', NULL, 'http://localhost:8082')"),

    step(
        """
        CREATE TABLE `user_permission_schema` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_id` int(11) DEFAULT NULL,
            `application_id` int(11) DEFAULT NULL,
            `company_id` int(11) DEFAULT NULL,
            `domen` text NOT NULL,
            `target` text NOT NULL,
            `permission` text NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE user_permission_schema"
    ),

    step("INSERT `user_permission_schema` VALUES (NULL, 1, 1, 1, 'view', 'project@master@table-project', '1001')"),
    step("INSERT `user_permission_schema` VALUES (NULL, 1, 1, 1, 'view', 'project@master@table-project@column.descr*', '1001')"),
    step("INSERT `user_permission_schema` VALUES (NULL, 1, 1, 1, 'model', 'application', '1001, 1002')"),

    step(
        """
        CREATE TABLE `role_permission_schema` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `role_id` int(11) DEFAULT NULL,
            `application_id` int(11) DEFAULT NULL,
            `company_id` int(11) DEFAULT NULL,
            `domen` text NOT NULL,
            `target` text NOT NULL,
            `permission` text NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE role_permission_schema"
    ),

    step("INSERT `role_permission_schema` VALUES (NULL, 1, 1, 1, 'view', 'project@master@table-project', '1001')"),
    step("INSERT `role_permission_schema` VALUES (NULL, 1, 1, 1, 'view', 'project@master@table-project@column.descr*', '-1001')"),
    step("INSERT `role_permission_schema` VALUES (NULL, 1, 1, 1, 'model', 'application', '1001, 1002')"),

    step(
        """
        CREATE TABLE `company` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` text NOT NULL,
            `description` text,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE company"
    ),

    step("INSERT `company` VALUES (1, 'Horns and Hooves', NULL)"),
    step("INSERT `company` VALUES (2, 'Cubes and Balls', NULL)"),

    step(
        """
        CREATE TABLE `role` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` text,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE role"
    ),

    step("INSERT `role` VALUES (1, 'Accountant')"),
    step("INSERT `role` VALUES (2, 'User')"),

    step(
        """
        CREATE TABLE `user` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `login` text NOT NULL,
            `password` text NOT NULL,
            `first_name` text,
            `second_name` text,
            `third_name` text,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE user"
    ),

    step("INSERT `user` VALUES (1, 'admin', 'admin', 'Vladimir', 'Putin', 'Vladimirovich')"),

    step(
        """
        CREATE TABLE `m2m_user_company` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_id` int(11) NOT NULL,
            `company_id` int(11) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE m2m_user_company"
    ),

    step("INSERT `m2m_user_company` VALUES (NULL, 1, 1)"),

    step(
        """
        CREATE TABLE `m2m_company_application` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `company_id` int(11) NOT NULL,
            `application_id` int(11) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE m2m_company_application"
    ),

    step("INSERT `m2m_company_application` VALUES (NULL, 1, 1)"),
    step("INSERT `m2m_company_application` VALUES (NULL, 1, 2)"),

    step(
        """
        CREATE TABLE `m2m_user_role` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_id` int(11) NOT NULL,
            `role_id` int(11) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE m2m_user_role"
    ),

    step("INSERT `m2m_user_role` VALUES (NULL, 1, 1)"),
    step("INSERT `m2m_user_role` VALUES (NULL, 1, 2)")
]
