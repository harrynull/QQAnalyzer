# QQAnalyzer
A tool used to analyze QQ group's messages.

Please run it with Python3

## Usage

Usage: `qqanalyzer.py \[-h\]\[-cache_input CACHE_INPUT\] \[--bom\]\[--no-bom\] \[--no-cache\]\[-qq QQ\] \[-min_unit MIN_UNIT\] input {user,all,week,hour}`

Analyze QQ groups' messages. Input is the file name of the exported QQ message history.

Modes:
1. `user`: Number of messages by user.
2. `all`: Number of messages by time.
3. `week`: Number of messages by weekdays.
4. `hour`: Number of messages by hours in a day.
