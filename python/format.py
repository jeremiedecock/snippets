#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# See: https://docs.python.org/2/library/string.html#format-specification-mini-language

import math

def main():

    # "{field_name:format_spec}".format(...)
    #
    # format_spec ::=  [[fill]align][sign][#][0][width][,][.precision][type]
    #
    # fill        ::=  <any character>
    # align       ::=  "<" | ">" | "=" | "^"
    # sign        ::=  "+" | "-" | " "
    # width       ::=  integer
    # precision   ::=  integer
    # type        ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
    #
    # The '#' option is only valid for integers, and only for binary, octal, or
    # hexadecimal output. If present, it specifies that the output will be
    # prefixed by '0b', '0o', or '0x', respectively.
    #
    # The ',' option signals the use of a comma for a thousands separator. For
    # a locale aware separator, use the 'n' integer presentation type instead.

    # Fill and align:

    #  '<' : Forces the field to be left-aligned within the available space
    #        (this is the default for most objects).
    #  '>' : Forces the field to be right-aligned within the available space
    #        (this is the default for numbers).
    #  '=' : Forces the padding to be placed after the sign (if any) but before
    #        the digits. This is used for printing fields in the form ‘+000000120’.
    #        This alignment option is only valid for numeric types.
    #  '^' : Forces the field to be centered within the available space.

    print("{:.<9}".format(3))
    print("{:.<9}".format(11))

    print("{:.>9}".format(3))
    print("{:.>9}".format(11))

    print("{:.=9}".format(3))
    print("{:.=9}".format(11))

    print("{:.^9}".format(3))
    print("{:.^9}".format(11))

    print()

    # Sign:

    #  '+'   : indicates that a sign should be used for both positive as well
    #          as negative numbers.
    #  '-'   : indicates that a sign should be used only for negative numbers
    #          (this is the default behavior).
    #  space : indicates that a leading space should be used on positive
    #          numbers, and a minus sign on negative numbers.

    print("{:+}".format(3))
    print("{:+}".format(-3))

    print("{:-}".format(3))
    print("{:-}".format(-3))

    print("{: }".format(3))
    print("{: }".format(-3))

    print()

    # Width

    print("{}".format(3))
    print("{}".format(11))

    print("{:3}".format(3))
    print("{:3}".format(11))

    print()

    # Precision

    print("{}".format(math.pi))
    print("{:.2f}".format(math.pi))

    print()

    # Type:

    # The available integer presentation types are:
    #  'b'  : Binary format. Outputs the number in base 2.
    #  'c'  : Character. Converts the integer to the corresponding unicode character before printing.
    #  'd'  : Decimal Integer. Outputs the number in base 10.
    #  'o'  : Octal format. Outputs the number in base 8.
    #  'x'  : Hex format. Outputs the number in base 16, using lower- case letters for the digits above 9.
    #  'X'  : Hex format. Outputs the number in base 16, using upper- case letters for the digits above 9.
    #  'n'  : Number. This is the same as 'd', except that it uses the current locale setting to insert the appropriate number separator characters.
    #  None : The same as 'd'.

    print("{:}".format(21))
    print("{:b}".format(21))
    print("{:#b}".format(21))
    #print("{:c}".format(21))
    print("{:d}".format(21))
    print("{:o}".format(21))
    print("{:#o}".format(21))
    print("{:x}".format(21))
    print("{:X}".format(21))
    print("{:#x}".format(21))
    print("{:#X}".format(21))
    print("{:n}".format(21))

    print()

    # Type:

    # The available presentation types for floating point and decimal values are:
    #  'e'  : Exponent notation. Prints the number in scientific notation using
    #         the letter ‘e’ to indicate the exponent. The default precision is 6.
    #  'E'  : Exponent notation. Same as 'e' except it uses an upper case ‘E’
    #         as the separator character.
    #  'f'  : Fixed point. Displays the number as a fixed-point number. The
    #         default precision is 6.
    #  'F'  : Fixed point. Same as 'f'.
    #  'g'  : General format. For a given precision p >= 1, this rounds the
    #         number to p significant digits and then formats the result in
    #         either fixed-point format or in scientific notation, depending on
    #         its magnitude.
    #         The precise rules are as follows: suppose that the result
    #         formatted with presentation type 'e' and precision p-1 would have
    #         exponent exp. Then if -4 <= exp < p, the number is formatted with
    #         presentation type 'f' and precision p-1-exp. Otherwise, the
    #         number is formatted with presentation type 'e' and precision p-1.
    #         In both cases insignificant trailing zeros are removed from the
    #         significand, and the decimal point is also removed if there are
    #         no remaining digits following it.
    #         Positive and negative infinity, positive and negative zero, and
    #         nans, are formatted as inf, -inf, 0, -0 and nan respectively,
    #         regardless of the precision.
    #         A precision of 0 is treated as equivalent to a precision of 1.
    #         The default precision is 6.
    #  'G'  : General format. Same as 'g' except switches to 'E' if the number
    #         gets too large. The representations of infinity and NaN are
    #         uppercased, too.
    #  'n'  : Number. This is the same as 'g', except that it uses the current
    #         locale setting to insert the appropriate number separator
    #         characters.
    #  '%'  : Percentage. Multiplies the number by 100 and displays in fixed
    #         ('f') format, followed by a percent sign.
    #  None : The same as 'g'.

    print("{}".format(math.pi))
    print("{:e}".format(math.pi))
    print("{:E}".format(math.pi))
    print("{:f}".format(math.pi))
    print("{:F}".format(math.pi))
    print("{:g}".format(math.pi))
    print("{:G}".format(math.pi))
    print("{:n}".format(math.pi))
    print("{:%}".format(math.pi))

if __name__ == '__main__':
    main()
