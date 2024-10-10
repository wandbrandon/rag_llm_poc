claims_member1 = {
    "A2000": {
        "claim_id": "A2000",
        "claim_status": "Approved",
        "claim_amount": 1000,
        "claim_date": "2022-01-01",
    },
    "B4231": {
        "claim_id": "B4231",
        "claim_status": "Pending",
        "claim_amount": 2000,
        "claim_date": "2022-01-02",
    },
    "C1234222X": {
        "claim_id": "C1234222222222X",
        "claim_status": "Denied",
        "claim_amount": 3000,
        "claim_date": "2022-01-03",
    },
}

claims_member2 = {
    "2022-01-03": {
        "claim_id": "A5999",
        "claim_status": "Approved",
        "claim_amount": 1500,
        "claim_date": "2022-01-04",
    },
    "2022-01-03": {
        "claim_id": "B4231",
        "claim_status": "Pending",
        "claim_amount": 2000,
        "claim_date": "2022-01-02",
    },
    "2022-01-03": {
        "claim_id": "C1234222X",
        "claim_status": "Denied",
        "claim_amount": 3000,
        "claim_date": "2022-01-03",
    },
}

member_data = {
    ("A1234", "06091999"): {
        "member_id": "A1234",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "06-09-1999",
        "zip_code": "32608",
        "claims": claims_member1,
    },
    "B5678": {
        "member_id": "B5678",
        "first_name": "Jane",
        "last_name": "Smith",
        "dob": "02-02-1991",
        "zip_code": "11112",
        "claims": claims_member2,
    },
}

findcare_zip = {
    "32608": {
        "provider": "Dr. John",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
        "phone": "18005551234",
    },
    "11112": {
        "provider": "Dr. Jane",
        "address": "456 Elm St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
        "phone": "18005551234",
    },
}

ani = {
    9544392981: {
        "riskflag": "Pass",
        "name": "John Doe",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
    },
    18005551234: {
        "riskflag": "Fail",
        "name": "Jane Doe",
        "address": "456 Elm St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
    },
}

dnis = {
    12000: {
        "claimsEnabled": True,
        "findcareEnabled": True,
    },
    29999: {
        "claimsEnabled": False,
        "findcareEnabled": True,
    },
}
