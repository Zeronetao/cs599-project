import time
import os
import os.path as osp

current_milli_time = lambda: int(round(time.time() * 1000))


FORMAT = "%Y-%m-%d%H:%M:%S"
STOCK_NAMES = ["0", "1", "2", "3", "4"]

Daily_Price_Limit = 0.7
expense_ratio = 0.02
Fluctuation_Constant = 20.0
verbose = False

# Simulation parameters
Iterations_Daily = 1  # 减少每日迭代次数从2到1
No_Days = 3  # 减少仿真天数从11到3
Num_Person = 4
Num_Stock = 3
STOCK_NAME = ['A', 'B', 'C','D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# 文件配置
SAVE_NAME = "sim01"
persona_name = "persona.json"
stock_name = "stocks.json"
Save_Path = osp.join("save", SAVE_NAME)
Num_quantity = 2500

if not os.path.exists(Save_Path):
    os.makedirs(Save_Path)

persona_path = osp.join(Save_Path, "persona.json")
stock_path = osp.join(Save_Path, "stocks.json")
strategy_flie = osp.join(Save_Path, "strategy.xlsx")

with_photo=[0]
without_ana=[2,4,5,7,8,9,10]
with_stock_infor=[0,1,2,3,4,5,6,7,8,9,10,11]
analysis_num = 3
gossip_num_max = 3
