from kaiser import get_kaiser
from cca import get_cca
from blueshield import get_blueshield
from uhc import get_uhc
import matplotlib.pyplot as plt

def get_plans(json_data):
  colors = {}
  plans = {}
  try:
    plans.update(get_kaiser(json_data))
    print("kaiser suceeded")
  except ValueError as e:
    print(e)
  try:
    plans.update(get_blueshield(json_data))
    print("blueshield suceeded")
  except ValueError as e:
    print(e)
  try:
    plans.update(get_cca(json_data))
    print("cca suceeded")
  except ValueError as e:
    print(e)
  try:
    plans.update(get_uhc(json_data))
    print("uhc suceeded")
  except ValueError as e:
    print(e)
  names = list(plans.keys())
  costs = list(plans.values())
  for plan in names:
    if "Covered California" in plan:
      colors.update({plan: "blueviolet"})
    elif "Blue Shield California" in plan:
      colors.update({plan: "deepskyblue"})
    elif "Kaiser" in plan:
      colors.update({plan: "navy"})
  colors = [colors[plan] for plan in names]
  plt.figure(figsize=(10, 10))
  plt.barh(names, costs, color=colors)
  plt.ylabel('Insurance Plan')
  plt.xlabel('Cost in $')
  plt.title('Insurance Plan Cost Comparison')
  plt.xticks(rotation=90, fontsize=10)
  plt.tight_layout()
  plt.show()