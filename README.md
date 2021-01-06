# python-tail

- example 1

```python
import tail

t = tail.Tail("/tmp/able")
t.follow()

```

- example 2

```python
import tail

def process_line(line):
    line = line.strip("\n")
    print("processing...", line)

t = tail.Tail("/tmp/able", interval_seconds=2.0, start_position="start")
t.register_callback(process_line)
t.follow()

```
