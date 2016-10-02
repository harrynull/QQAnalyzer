# QQAnalyzer
A tool used to analyze QQ group's messages.



## Usage

usage: qqanalyzer.py \[-h\]\[-cache_input CACHE_INPUT\] \[--bom\]\[--no-bom\] \[--no-cache\]\[-qq QQ\] \[-min_unit MIN_UNIT\] input {user,all,week}

Analyze QQ groups' messages

###positional arguments:

  input                 the input file: QQ exported *.txt message file

  {user,all,week}       mode you want to use

###optional arguments:

  -h, --help					show this help message and exit

  -cache_input CACHE_INPUT			the cache file

  --bom						use bom in the output file

  --no-bom					do not use bom in the output file

  --no-cache					ignore the cache file(if has)

  -qq QQ					only analyze specific qq, only available in all andweek mode

  -min_unit MIN_UNIT				only analyze specific qq, only available in all mode,the default value is 1 week, the unit is second
