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
, CHARACTERWISE
, BLOCKWISE
, UNSPECIFIED
, START
, END
) = range(14)

SELF_INSERTABLE_CHARS = \
( LETTERS
+ DIGITS
+ '!@#$%^&*()'
+ '~`"<>,.;:/=?+-|[]{}'
+ "'"
)

NOT_IMPLEMENTED = 'not implemented'
