# NectaPy

A Python package for accessing NECTA (National Examinations Council of Tanzania) examination results.

### Installation

```bash
pip install NectaPy
```

### Usage

```python
from NectaPy import st_result, sc_result, st_compare, st_mentioned
```

### Get student result

```python
# Possible levels: 'sfna', 'psle', 'ftna', 'csee', 'acsee', 'gatce', 'dsee', 'gatscce'
# Use st_result when finding a single student's result.
result = st_result('S4177/0003/2023', 'csee')
print(result)
```

### Get school results

```python
# Possible levels: 'sfna', 'psle', 'ftna', 'csee', 'acsee', 'gatce', 'dsee', 'gatscce'
# Use sc_result when you need to see the results of all students at a given school.
school_results = sc_result('S1001/2023', 'csee')
print(school_results)
```

### Compare student results

```python
# Possible levels: 'sfna', 'psle', 'ftna', 'csee', 'acsee', 'gatce', 'dsee', 'gatscce'
# Use st_compare when you need to compare students of the same level but from different schools or years, or the same school and year.
comparison_results = st_compare(['S0010/0001/2024', 'S3200/0100/2023', 'S0012/0005/2022'], 'csee')
print(comparison_results)
```

### Get mentioned students results

```python
# Possible levels: 'sfna', 'psle', 'ftna', 'csee', 'acsee', 'gatce', 'dsee', 'gatscce'
# Use st_mentioned when you need to find different students at the same time, who can be from different or the same year, level, or school.
mentioned_results = st_mentioned([('S1266/0001/2020', 'csee'), ('S2265/0001/2022', 'ftna'), ('S1066/0001/2017', 'csee')])
print(mentioned_results)
```

### Supported Examinations

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

### Features

- Easy to use API
- Supports all major NECTA examinations
- Returns results in dictionary format
- Handles errors gracefully
- Python 3+ compatible

## Example Output

### Student Result

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

### School Results

```bash
{
    "school_no": "S1001",
    "school_name": "S1001 MBESA SECONDARY SCHOOL ",
    "results": [
        {
            "CNO": "S1001/0001",
            "PReM NO": "xxxxxxx",
            "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
            "GENDER": "XX",
            "SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
        },
        // ...more student results...
    ]
}
```

### Compare Student Results

```bash
{
    "student1": {
        "CNO": "S0010/0001",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    },
    "student2": {
        "CNO": "P3200/0100",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    },
    "student3": {
        "CNO": "S0012/0005",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    }
}
```

### Mentioned Students Results

```bash
{
    "student1": {
        "CNO": "S1266/0001",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    },
    "student2": {
        "CNO": "S2265/0001",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    },
    "student3": {
        "CNO": "S1066/0001",
        "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
        "SEX": "M",
        "DIV": "I",
        "PTS": "17",
        "DETAILED SUBJECTS": "CIVICS-'B' HIST-'A' GEO-'A' KISW-'B' ENGL-'A' PHY-'B' CHEM-'A' BIO-'B' B/MATH-'B'"
    }
}
```

## License

MIT License
