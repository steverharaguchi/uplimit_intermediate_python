# Python for Production

## Install all dependencies

- Make you're using Python version >= 3.9.0
- Install all the modules

```
pip install -r requrirements.txt
```

## Generate data

Generate test data (useful for unit testing code)

```
python generate_data.py --type tst
```

Generate small data (useful for quick testing of logic)

```
python generate_data.py --type sml
```

Generate big data (actual data)

```
python generate_data.py --type bg
```
