# Run tests with prints 
```
PYTHONPATH=../ pytest test.py -s
```

# Run tests without prints 
```
PYTHONPATH=../ pytest test.py
```

# Run the code
````
# Run on `test` data
PYTHONPATH=../ python main.py --type tst

# Run on `small` data
PYTHONPATH=../ python main.py --type sml

# Run on the `big` data
PYTHONPATH=../ python main.py --type bg
````