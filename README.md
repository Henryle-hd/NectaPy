# NectaPy

A Python package for accessing NECTA (National Examinations Council of Tanzania) examination results.

## Installation

```bash
pip install NectaPy
```

## Usage

```python
from NectaPy import st_result
```

# Get student result

```python
result = st_result('S4177/0003/2023', 'csee')
print(result)
```

## Supported Examinations

Primary Level:

> - SFNA (Standard 2): 2017-2024
> - PSLE (Standard 7): 2016-2024

Secondary Level:

> - FTNA (Form 2): 2022-2024
> - CSEE (Form 4): 2015-2024
> - ACSEE (Form 6): 2014-2024

College Level:

> - GATCE: 2019-2024
> - DSEE: 2019-2024
> - GATSCCE: 2019-2024

## Features

- Easy to use API
- Supports all major NECTA examinations
- Returns results in dictionary format
- Handles errors gracefully
- Python 3.6+ compatible

## Example Output

```bash
{
    "CNO": "S4177/0003",
    "CANDIDATE NAME": "JOHN DOE",
    "SEX": "M",
    "DIV": "I",
    "PTS": "17",
    "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
}
```

## License

MIT License
