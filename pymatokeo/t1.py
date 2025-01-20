import json
temp="""{
    "S0484/0001":
    {
        "General":{
            "Gender":"F",
            "AGG":29,
            "Division":"IV"
        },
        "Detailed":{
            "CIV":"D",
            "HIST":"D",
            "GEO":"D",
            "KISW":"D",
            "ENG":"D",
            "PHY":"D",
            "CHEM":"D",
            "BIO":"D",
            "B_MATH":"D"
        }
    }
}"""

data=json.loads(temp)
print(data['S0484/0001']['General'])


temp=[('S0484/0001','F','26','IV',"HIST - 'F' PHY - 'F' CHEM - 'D' B/MATH - 'F' '")]