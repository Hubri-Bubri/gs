"""
replace column type for project and add comments
"""

from yoyo import step

__depends__ = {'20180610_01_8Wm6v-add-column-for-project'}

steps = [
    step("""
            ALTER TABLE project DROP COLUMN `type`
        """,
        "ALTER TABLE project ADD `type` text"

    ),
    step("""
            ALTER TABLE project ADD `type` int(11), ADD `comment_for_project` int(11);
        """,
        "ALTER TABLE project DROP COLUMN comment_for_project, type"

    ),
    step("""
        CREATE TABLE `comment_for_project` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `comment` text NULL,
            `user_id` int(11) NULL,
            `date` text NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """,
        "DROP TABLE comment_for_project"
    ),
    step("""INSERT `comment_for_project` VALUES (0,
        'No comfort do written conduct at prevent manners on. Celebrated contrasted discretion him sympathize her collecting occasional. Do answered bachelor occasion in of offended no concerns. Supply worthy warmth branch of no ye. Voice tried known to as my to. Though wished merits or be. Alone visit use these smart rooms ham. No waiting in on enjoyed placing it inquiry. '
        , '1', '2016-01-11')"""),
    step("""INSERT `comment_for_project` VALUES (0,
        'Next his only boy meet the fat rose when. Do repair at we misery wanted remove remain income. Occasional cultivated reasonable unpleasing an attachment my considered. Having ask and coming object seemed put did admire figure. Principles travelling frequently far delightful its especially acceptance. Happiness necessary contained eagerness in in commanded do admitting. Favourable continuing difficulty had her solicitude far. Nor doubt off widow all death aware offer. We will up able in both do sing.'
        , '1', '2016-02-12')"""),
    step("""INSERT `comment_for_project` VALUES (0,
        'So delightful up dissimilar by unreserved it connection frequently. Do an high room so in paid. Up on cousin ye dinner should in. Sex stood tried walls manor truth shy and three his. Their to years so child truth. Honoured peculiar families sensible up likewise by on in.'
        , '1', '2016-03-28')"""),
    step("""INSERT `comment_for_project` VALUES (0,
        'Repulsive questions contented him few extensive supported. Of remarkably thoroughly he appearance in. Supposing tolerably applauded or of be. Suffering unfeeling so objection agreeable allowance me of. Ask within entire season sex common far who family. As be valley warmth assure on. Park girl they rich hour new well way you. Face ye be me been room we sons fond.'
        , '1', '2016-04-27')""")
]