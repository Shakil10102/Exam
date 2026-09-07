with open('d:/Exam/pre-advising.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('"tri": 1,', "Trimester 1 data"),
    ('"tri": 2,', "Trimester 2 data"),
    ('"tri": 3,', "Trimester 3 data"),
    ('"tri": 4,', "Trimester 4 data"),
    ('"tri": 5,', "Trimester 5 data"),
    ('"tri": 6,', "Trimester 6 data"),
    ('"tri": 7,', "Trimester 7 data"),
    ('"tri": 8,', "Trimester 8 data"),
    ('"tri": 9,', "Trimester 9 data"),
    ('"tri": 10,', "Trimester 10 data"),
    ('"tri": 11,', "Trimester 11 data"),
    ('"tri": 12,', "Trimester 12 data"),
    ('"tri": "GED"', "GED Optionals data"),
    ('"tri": "Elective"', "Elective Tracks data"),
    ('"tri": "BSDS"', "BSDS Specialized data"),
    ('09:00 AM', "Exam Slot T1 Time"),
    ('11:30 AM', "Exam Slot T2 Time"),
    ('02:00 PM', "Midterm Slot T3 Time"),
    ('02:30 PM', "Final Exam Slot T3 Time"),
    ('Azizur Rahman Anik', "BSCSE Advisor #1"),
    ('Farhan Anan Himu', "BSCSE Advisor #60"),
    ('Minhajul Bashir', "BSDS Advisor #1"),
    ('Siana Rizwan', "BSDS Advisor #6"),
    ('checkClashes', "Clash check logic"),
    ('lookupAdvisor', "Advisor lookup logic"),
    ('setExamMode', "Exam mode switch logic"),
    ('filterTrimester', "Trimester pill filter logic")
]

all_passed = True
for target, label in checks:
    if target in content:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        all_passed = False

if all_passed:
    print("\nALL 27 DATA & LOGIC INTEGRITY CHECKS PASSED!")
else:
    print("\nSOME CHECKS FAILED!")
