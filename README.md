# shovel
Use this to dig yourself out of the proverbial hole.

## Student loan payment scheduler

```javascript
$ python shovel.py 
+-----------------+---------+---------+---------+--------+---------+
|                 |  Loan01 |  Loan02 |  Loan03 | Loan04 |   Total |
+-----------------+---------+---------+---------+--------+---------+
|                 |         |         |         |        |         |
|  2017 Principal | 1000.00 |  500.00 |  100.00 | 100.00 | 1700.00 |
|        Interest |  +50.00 |  +75.00 |  +40.00 |  +5.00 |  170.00 |
| Monthly Payment |  -24.51 |  -36.76 |  -11.67 |  -2.45 |   75.39 |
|  Annual Payment | -294.12 | -441.18 | -140.00 | -29.41 |  904.71 |
|                 |         |         |         |        |         |
|  2018 Principal |  755.88 |  133.82 |    0.00 |  75.59 |  965.29 |
|        Interest |  +37.79 |  +20.07 |   +0.00 |  +3.78 |   61.65 |
| Monthly Payment |  -51.09 |  -12.82 |   -0.00 |  -5.11 |   69.02 |
|  Annual Payment | -613.07 | -153.90 |   -0.00 | -61.31 |  828.28 |
|                 |         |         |         |        |         |
|  2019 Principal |  180.60 |    0.00 |    0.00 |  18.06 |  198.66 |
|        Interest |   +9.03 |   +0.00 |   +0.00 |  +0.90 |    9.93 |
| Monthly Payment |  -15.80 |   -0.00 |   -0.00 |  -1.58 |   17.38 |
|  Annual Payment | -189.63 |   -0.00 |   -0.00 | -18.96 |  208.60 |
+-----------------+---------+---------+---------+--------+---------+
```

The `shovel.py` script reads a coniguration file, `config.yaml`.

```yaml
period: Yearly          #recalculation frequency. "Yearly" or "Monthly".

# If your period is monthly, 
#  - your starting payment should be in terms of how much per month you can afford, and
#  - your growth           should be in terms of how much salary growth you expect each month.

startingPayment: 1000   #how much to begin paying down initially per period
growth: 0               #by what percent to increase the payment each period.

startingYear: 2017      #the year repayment started. 
startingMonth: 1        #the month repayment started.

loans: 
  - name: Loan01        #use unique identifiers please :) 
    prin: 1000          #principal amount of loan
    rate: 5.00          #rate on loan
  - name: Loan02
    prin: 500
    rate: 15.00
  - name: Loan03
    prin: 100
    rate: 40.00
  - name: Loan04
    prin: 100
    rate: 5.00
```

### Notes:
 - The engine expects a payment you can afford per-month (`startingPayment`), and distributes it across the loans, weighted by the potential interest from each loan.
 - There is an option (`growth`) to inflate each month's or year's payment by a constant rate, to track with expected salary growth over the next `n` years. Zero by default.

### Bugs:
- Values for `startingPayment` smaller than (???) cause the script to never finish. This reflects the possibility of a desired repayment schedule to never converge; that is, if the amount you pay each month is smaller than the amount of interest accumulated, you'll never pay off the loans. This could be caught in some user-friendly way.
 
### Todo:
- [ ] Support for staggered loan start dates
- [ ] Support for maximum loan lifetime
- [ ] Better end-of-life handling / sub-dollar handling

