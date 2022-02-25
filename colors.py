# Formatting codes for console output
RED = "\x1b[31m"
GRN = "\x1b[32m"
ORG = "\x1b[33m"
MAG = "\x1b[35m"
CYN = "\x1b[36m"
CRR = "\x1b[100H"
ERS = "\x1b[2K"
RES = "\x1b[0m"

def CRB(by: int):
	return f"\x1b[{by}D"