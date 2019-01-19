# cookieCrumble
Parse cookies and their HTTPOnly and/or Secure flag from given URL(s)
## Args:
```
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Single target or file of newline seperated targets
  -o OUTFILE, --outfile OUTFILE
                        File to write 'result info' to; CSV format; defaults
                        to shredder.csv
```

## Example input: input.txt:
```
  https://google.com
  https://github.com/pulls
  https://old.reddit.com/r/programming/
```

## Example usage:
`python3 cookieCrumble.py -t input.txt`

## Example output: crumbled.csv
```
URL,Cookie Name,HTTPOnly?,Secure?
https://old.reddit.com/r/programming/,edgebucket,No,Yes
..,loid,No,Yes
..,session_tracker,No,Yes
https://google.com,1P_JAR,No,No
..,NID,No,No
https://github.com/pulls,_gh_sess,No,Yes
..,has_recent_activity,No,No
```
