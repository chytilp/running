### Commands:

```
$ export PYTHONPATH="${PYTHONPATH}:~/pokusy/python/running/"

$ python3.11 ./src/main.py --route prok dates

$ python3.11 ./src/main.py --route prok date 2026-04-09

$ python3.11 ./src/main.py --route prok section 1.km

$ python3.11 ./src/main.py --route prok --mark 2026-02-24 section 1.km

$ python3.11 ./src/main.py --route prok aggregation total

$ python3.11 ./src/main.py --route prok --mark 2026-02-24 aggregation total

$ python3.11 ./src/main.py --route prok grades --section 1.km

$ python3.11 ./src/main.py --route prok grades --aggregation first5

$ python3.11 ./src/main.py --route prok dashboard

$ python3.11 ./src/main.py --route prok compare 2025-09-08,2026-04-09
```