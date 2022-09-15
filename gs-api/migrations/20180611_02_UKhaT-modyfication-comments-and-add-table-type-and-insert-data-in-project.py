"""
modyfication comments and add table type and insert data in project
"""

from yoyo import step

__depends__ = {'20180611_01_5VN1q-replace-column-type-for-project-and-add-comments'}

steps = [
    step("""
        CREATE TABLE `type_for_project` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `type` text NULL,
            `pryority` int(11) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE type_for_project"
    ),
    step("""
        CREATE TABLE `m2m_project_comment` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `project_id` int(11) NULL,
            `comment_id` int(11) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE m2m_project_comment"
    ),
    step("""
        CREATE TABLE `m2m_project_type` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `project_id` int(11) NULL,
            `type_id` int(11) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE m2m_project_type"
    ),
    step("""
        ALTER TABLE project DROP COLUMN `type`
        """
    #    "ALTER TABLE `project` ADD `type` int(11)"
    ),
        step("""
        ALTER TABLE `project` DROP COLUMN `comment_for_project`
        """
    #    "ALTER TABLE `project` ADD `comment_for_project` int(11)"
    ),

    step("INSERT `m2m_project_comment` VALUES (0, 1, 1)"),
    step("INSERT `m2m_project_comment` VALUES (0, 1, 2)"),
    step("INSERT `m2m_project_comment` VALUES (0, 1, 3)"),
    step("INSERT `m2m_project_comment` VALUES (0, 1, 4)"),

    step("INSERT `m2m_project_comment` VALUES (0, 2, 1)"),
    step("INSERT `m2m_project_comment` VALUES (0, 2, 2)"),
    step("INSERT `m2m_project_comment` VALUES (0, 2, 3)"),
    step("INSERT `m2m_project_comment` VALUES (0, 2, 4)"),

    step("INSERT `m2m_project_comment` VALUES (0, 3, 1)"),
    step("INSERT `m2m_project_comment` VALUES (0, 3, 2)"),
    step("INSERT `m2m_project_comment` VALUES (0, 3, 3)"),
    step("INSERT `m2m_project_comment` VALUES (0, 3, 4)"),

    step("INSERT `m2m_project_comment` VALUES (0, 4, 1)"),
    step("INSERT `m2m_project_comment` VALUES (0, 4, 2)"),
    step("INSERT `m2m_project_comment` VALUES (0, 4, 3)"),
    step("INSERT `m2m_project_comment` VALUES (0, 4, 4)"),

    step("INSERT `type_for_project` VALUES (0, 'L', 1)"),
    step("INSERT `type_for_project` VALUES (0, 'B', 2)"),
    step("INSERT `type_for_project` VALUES (0, 'T', 3)"),
    step("INSERT `type_for_project` VALUES (0, 'W', 4)"),
    step("INSERT `type_for_project` VALUES (0, 'S', 5)"),

    step("INSERT `m2m_project_type` VALUES (0, 1, 1)"),
    step("INSERT `m2m_project_type` VALUES (0, 1, 2)"),
    step("INSERT `m2m_project_type` VALUES (0, 1, 3)"),
 
    step("INSERT `m2m_project_type` VALUES (0, 2, 2)"),
    step("INSERT `m2m_project_type` VALUES (0, 2, 3)"),
    step("INSERT `m2m_project_type` VALUES (0, 2, 4)"),

    step("INSERT `m2m_project_type` VALUES (0, 3, 3)"),
    step("INSERT `m2m_project_type` VALUES (0, 3, 4)"),
    step("INSERT `m2m_project_type` VALUES (0, 3, 5)"),

    step("INSERT `m2m_project_type` VALUES (0, 4, 4)"),
    step("INSERT `m2m_project_type` VALUES (0, 4, 5)"),
    step("INSERT `m2m_project_type` VALUES (0, 4, 3)")
]
