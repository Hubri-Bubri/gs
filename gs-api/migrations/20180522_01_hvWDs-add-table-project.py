"""
Add table project
"""

from yoyo import step

__depends__ = {'20180422_01_D62GZ-start-database-state'}

steps = [
    step("""
        CREATE TABLE `project` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `user_id` int(11) NOT NULL,
            `project number` text NULL,
            `date` text NULL,
            `street` text NULL,
            `city` text NULL,
            `zip` int(11) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE project"
    ),
    step("INSERT `project` VALUES (0, 1, '0001-2016', '2016-01-11', 'Frankfurter Strasse 39_0312', 'Darmstadt', 64293)"),
    step("INSERT `project` VALUES (0, 1, '0002-2016', '2016-02-12', 'In den Leppsteinswiesen 8', 'Rossdorf', 64380)"),
    step("INSERT `project` VALUES (0, 1, '0001-2017', '2017-03-13', 'Asternweg 15', 'Darmstadt', 64291)"),
    step("INSERT `project` VALUES (0, 1, '0002-2017', '2017-04-14', 'Weidigweg 8?1361', 'Darmstadt', 64297)"),
    step("INSERT `project` VALUES (0, 1, '0001-2018', '2018-05-15', 'Heidelberger Landstraße 389', 'Darmstadt', 64297)"),
    step("INSERT `project` VALUES (0, 1, '0002-2018', '2018-06-16', 'Mainzer Landstraße 50', 'Frankfurt', 60325)"),
    step("INSERT `project` VALUES (0, 1, '0001-2019', '2019-07-17', 'August-Mety-Weg 15', 'Darmstadt', 64297)"),
    step("INSERT `project` VALUES (0, 1, '0002-2019', '2019-08-18', 'Kurt-Schumacher-Strasse 60', 'Darmstadt', 64297)")
]