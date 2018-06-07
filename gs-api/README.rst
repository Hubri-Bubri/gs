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



Ideas for security
==================


(user, application, 'view', 'project/master/table/column:name', 'read')
(user, application, 'view', 'project/master/detail/button:ok', 'read')
(user, application, 'database', 'table/column:na*', 'read')
(user, application, 'action', ':data', 'read')

(user_group, dashboard@data@table@column/name, 'read')


# Аналогичное на стороне javascript.
# В первую очередь продумать императивный вариант!

@has_permission(
    {
        'dashboard.order', ['write', 'delete'],
        # AND
        'dashboard.money', ['write']
    },
    # OR
    {'dashboard.video', ['write', 'read']},
    
    {'view@table@column:dashboard/order', ['read']},
    
    {'dashboard/@data.table/order/@member/_*', ['invisible']},

    {'dashboard/@view/@record/order/@member/_*', ['invisible']}
)
def security():
    pass
