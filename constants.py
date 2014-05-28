from string import ascii_letters as LETTERS, digits as DIGITS

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
( LETTERS
+ DIGITS
+ '!@#$%^&*()'
+ '~`"<>,.;:/=?+-|[]{}'
+ "'"
)
