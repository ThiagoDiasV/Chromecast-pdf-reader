import re

m = re.search(r'(PDA-\d{3}nm)'
              r'(\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2})', 'PDA-283nm Results (System (29/3/2019 15:03:04) (Reprocessed)) Retention Time Area Area % Height Height % 2,643 10848463 99,86 1976698 99,94 3,160 15657 0,14 1219 0,06')
print(m.groups())