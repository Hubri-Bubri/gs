Database migration
==================

``yoyo apply --database mysql://root:8888@localhost/gs .``
``yoyo rollback --database mysql://root:8888@localhost/gs .``


Query for users
===============

.. code-block:: sql
    SELECT
        users.id,
        users.userName,
        companies.access,
        applications.name,
        applications.image,
        applications.description,
        applications.label,
        applications.link
    FROM users JOIN companies ON companies.user=users.id
    JOIN applications ON applications.id=companies.application
    WHERE users.userName='{name}'
    AND users.password='{passw}'
    AND companies.companyId='{appid}'
