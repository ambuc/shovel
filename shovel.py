import yaml
from prettytable import PrettyTable
import prettytable
import calendar

class bcolors:
    HEADER = '\033[95m'; OKBLUE = '\033[94m'; OKGREEN = '\033[92m';   WARNING = '\033[93m'
    FAIL   = '\033[91m';   ENDC = '\033[0m';     BOLD = '\033[1m';  UNDERLINE = '\033[4m'

def getInterest(prin, rate):
    if period == "Yearly":
        return prin*(1+rate)-prin
    else: #Monthly
        return prin*(1+(rate/12.0))-prin

def calcWeights(loans):
    interests, weights = [], []
    [ interests.append( getInterest(l['prin'], l['rate']) ) for l in loans ]
    total = sum(interests)
    [ weights.append( i / total ) for i in interests ]
    return weights

def calcPayments(loans, payment):
    payments = []
    weights = calcWeights(loans)
    for i in range(len(loans)):
	#we take the minimum of our recommended weighting and the potential accumulation of the next year
        #this lets us surge a bit on the last year to tackle any remaining interest
        p = min( loans[i]['prin'] + getInterest( loans[i]['prin'], 
                                                 loans[i]['rate'] ), 
                  weights[i]*payment)
	if rounding:
            p = 12*int(p/12.0)
	payments.append(p)
    return payments

def increment(loans, payment):
    payments = calcPayments(loans, payment)
    for i in range(len(loans)):
        loan = loans[i]
        loan['prin'] = loan['prin']+getInterest(loan['prin'], loan['rate']) - payments[i]
        if loan['prin'] < 10:
            loan['prin'] = 0
    return loans, payments

def pNeg(n):
    if n == 0: return format(n, ".2f")
    else: return bcolors.FAIL + format(n, ".2f") + bcolors.ENDC

def pPos(n):
    if n == 0: return format(n, ".2f")
    else: return bcolors.OKGREEN + format(n, ".2f") + bcolors.ENDC

def pWarn(n): return bcolors.WARNING+n+bcolors.ENDC
def pOK(n): return bcolors.OKBLUE+n+bcolors.ENDC
def pHeader(n): return bcolors.HEADER+n+bcolors.ENDC

def newLine(n):
    return [" " for i in range(n)]

def calcLeft(loans):
    return sum([l['prin'] for l in loans])

def schedule(loans):
    payment, month = startingPayment, startingMonth
    year = 0

    t = PrettyTable([""]+[pHeader(l['name']) for l in loans]+[pHeader("Total")], align="r")

    #alignments
    for l in loans:
        t.align[pHeader(l['name'])] = "r"
    t.align[""] = "r"
    t.align[pHeader("Total")] = "r"

    while calcLeft(loans) > 10:
        t.add_row(newLine(2+len(loans)))

        if period == "Monthly":
            yearTitle = "{0} {1}".format(calendar.month_abbr[month], year+startingYear)
            periodPaymentTitle = pHeader("Monthly")+" Payment"
        else:
            yearTitle = "{0}".format(year+startingYear)
            periodPaymentTitle = pHeader("Annual")+" Payment"

        t.add_row(["{0} Principal".format(pWarn(yearTitle))]
                + [pPos(l['prin']) for l in loans]
                + [format(sum([l['prin'] for l in loans]),".2f")])

        t.add_row(["Interest"]
                + ["+{0}".format(format(getInterest(l['prin'], l['rate']),".2f")) for l in loans]
                + [format(sum([getInterest(l['prin'], l['rate']) for l in loans]),".2f")])

        loans, recentPayments  = increment(loans, payment)

        if period == "Yearly":
            t.add_row(["Monthly Payment"]
                    + ["-{0}".format(r/12.0) for r in recentPayments]
                    + [format(sum([r/12.0 for r in recentPayments]),".2f")])

        t.add_row([periodPaymentTitle]
                + ["-{0}".format(pNeg(r)) for r in recentPayments]
                + [pHeader(format(sum([r for r in recentPayments]),".2f"))])

        payment = payment * (1 + growth)

        if period == "Monthly":
            if month == 12:
                month = 1; year = year + 1
            else:
                month = month + 1
        else:
            year = year + 1

    print t

y = yaml.load(open('config.yaml'))

global rounding, period, growth, startingYear, startingMonth, startingPayment
rounding =  y['rounding']
period = y['period'] or "Yearly"
growth = float(y['growth'])/100.0 or 0
startingYear = y['startingYear']
startingMonth = y['startingMonth']
startingPayment = float(y['startingPayment']) or 5000

loans = y['loans']

for loan in loans:
    loan['rate'] /= 100 #percent to decimal

schedule(loans)
