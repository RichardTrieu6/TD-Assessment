# 10 000 in CAD
bal = 10000

# [bid, ask]
usdcad_start = [1.3716,1.13718]
usdchf_start = [0.8019,0.8020]
usdmxn_start = [18.838,18.8460]

usdcad_end = [1.3816,1.13818]
usdchf_end = [0.8119,0.812]
usdmxn_end = [18.238,18.8260]

# CAD -> USD -> CHF

# CAD -> USD
bal = bal / usdcad_start[0]

# USD -> CHF
bal = bal * usdchf_start[1]

# Need CHFMXN bid and ask price
# Can derive by cancelling out units with usdmxn and usdchf 

chfmxn_start = [18.838 / 0.8019, 18.8460 / 0.8020]     

chfmxn_end = [18.238 / 0.8119, 18.8260 / 0.812]

# CHF -> MXN
bal = bal * chfmxn_start[1]

# Convert back to CAD: MXN -> CHF using end prices
bal = bal / chfmxn_end[0]

#CHF -> USD
bal = bal / usdchf_end[0]

#USD -> CAD
bal = bal * usdcad_end[1]

print(bal)

# End price of $8574.82 assuming 0% carry cost

# With 6% annual carry cost
carry_cost = 10000 * 0.06 * (7/365)
final_bal_with_carry = bal - carry_cost
print(final_bal_with_carry)
# Final balance with the carry cost is 8563.32S

