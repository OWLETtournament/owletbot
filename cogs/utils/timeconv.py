# This code uses parts of pytimeparse (https://pypi.org/project/pytimeparse/)
# The pytimeparse license is included below

"""
timeparse.py
(c) Will Roberts <wildwilhelm@gmail.com>  1 February, 2014
Implements a single function, `timeparse`, which can parse various
kinds of time expressions.
"""

# MIT LICENSE
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from discord.ext import commands

SIGN = r'(?P<sign>[+|-])?'
# YEARS = r'(?P<years>\d+)\s*(?:ys?|yrs?.?|years?)'
# MONTHS = r'(?P<months>\d+)\s*(?:mos?.?|mths?.?|months?)'
WEEKS = r'(?P<weeks>[\d.]+)\s*(?:w|wks?|weeks?)'
DAYS = r'(?P<days>[\d.]+)\s*(?:d|dys?|days?)'
HOURS = r'(?P<hours>[\d.]+)\s*(?:h|hrs?|hours?)'
MINS = r'(?P<mins>[\d.]+)\s*(?:m|(mins?)|(minutes?))'
SECS = r'(?P<secs>[\d.]+)\s*(?:s|secs?|seconds?)'
SEPARATORS = r'[,/]'
SEC_CLOCK = r':(?P<secs>\d{2}(?:\.\d+)?)'
MIN_CLOCK = r'(?P<mins>\d{1,2}):(?P<secs>\d{2}(?:\.\d+)?)'
HOUR_CLOCK = r'(?P<hours>\d+):(?P<mins>\d{2}):(?P<secs>\d{2}(?:\.\d+)?)'
DAY_CLOCK = (r'(?P<days>\d+):(?P<hours>\d{2}):'
             r'(?P<mins>\d{2}):(?P<secs>\d{2}(?:\.\d+)?)')


def opt(x):
    return r'(?:{x})?'.format(x=x, SEPARATORS=SEPARATORS)
OPT = opt


def opt_sep(x):
    return r'(?:{x}\s*(?:{SEPARATORS}\s*)?)?'.format(x=x, SEPARATORS=SEPARATORS)
OPT_SEP = opt_sep


TIME_FORMATS = [
    r'{WEEKS}\s*{DAYS}\s*{HOURS}\s*{MINS}\s*{SECS}'.format(
        # YEARS=OPT_SEP(YEARS),
        # MONTHS=OPT_SEP(MONTHS),
        WEEKS=OPT_SEP(WEEKS),
        DAYS=OPT_SEP(DAYS),
        HOURS=OPT_SEP(HOURS),
        MINS=OPT_SEP(MINS),
        SECS=OPT(SECS)),
    r'{MIN_CLOCK}'.format(
        MIN_CLOCK=MIN_CLOCK),
    r'{WEEKS}\s*{DAYS}\s*{HOUR_CLOCK}'.format(
        WEEKS=OPT_SEP(WEEKS),
        DAYS=OPT_SEP(DAYS),
        HOUR_CLOCK=HOUR_CLOCK),
    r'{DAY_CLOCK}'.format(
        DAY_CLOCK=DAY_CLOCK),
    r'{SEC_CLOCK}'.format(
        SEC_CLOCK=SEC_CLOCK),
    # r'{YEARS}'.format(
        #YEARS=YEARS),
    # r'{MONTHS}'.format(
        #MONTHS=MONTHS),
    ]

COMPILED_SIGN = re.compile(r'\s*' + SIGN + r'\s*(?P<unsigned>.*)$')
COMPILED_TIMEFORMATS = [re.compile(r'\s*' + timefmt + r'\s*$', re.I)
                        for timefmt in TIMEFORMATS]

MULTIPLIERS = dict([
        # ('years',  60 * 60 * 24 * 365),
        # ('months', 60 * 60 * 24 * 30),
        ('weeks',   60 * 60 * 24 * 7),
        ('days',    60 * 60 * 24),
        ('hours',   60 * 60),
        ('mins',    60),
        ('secs',    1)
        ])


class ConvertStrToTime(commands.Converter):
    async def convert(self, ctx, argument):
        def parse(sval):
            match = COMPILED_SIGN.match(sval)
            sign = -1 if match.groupdict()['sign'] == '-' else 1
            sval = match.groupdict()['unsigned']
            for timefmt in COMPILED_TIMEFORMATS:
                match = timefmt.match(sval)
                if match and match.group(0).strip():
                    mdict = match.groupdict()
                    # if all of the fields are integer numbers
                    if all(v.isdigit() for v in list(mdict.values()) if v):
                        return sign * sum([MULTIPLIERS[k] * int(v, 10) for (k, v) in
                                           list(mdict.items()) if v is not None])
                    # if SECS is an integer number
                    elif ('secs' not in mdict or
                          mdict['secs'] is None or
                          mdict['secs'].isdigit()):
                        # we will return an integer
                        return (
                                sign * int(sum([MULTIPLIERS[k] * float(v) for (k, v) in
                                                list(mdict.items()) if k != 'secs' and v is not None])) +
                                (int(mdict['secs'], 10) if mdict['secs'] else 0))
                    else:
                        # SECS is a float, we will return a float
                        return sign * sum([MULTIPLIERS[k] * float(v) for (k, v) in
                                           list(mdict.items()) if v is not None])
        try:
            return parse(argument)
        except Exception as e:
            raise commands.BadArgument('Your argument was most likely not an integer.')
