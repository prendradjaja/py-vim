( NORMAL
, INSERT
, OPERATOR_PENDING
, OPERATOR
, MOTION
, INCLUSIVE
, EXCLUSIVE
, LINEWISE
, SELF_INSERT
) = range(9)

SELF_INSERTABLE_CHARS = \
( 'abcdefghijklmnopqrstuvwxyz'
+ 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
+ '0123456789'
+ '!@#$%^&*()'
+ '~`"<>,.;:/=?+-|[]{}'
+ "'"
)
