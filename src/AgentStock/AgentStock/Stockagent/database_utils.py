import sqlite3
import time
import matplotlib
matplotlib.use('Agg')  # 设置matplotlib为非交互式后端，避免弹出窗口
import matplotlib.pyplot as plt

import pandas as pd
import warnings
import base64
import numpy as np
import mplfinance as mpf
import pandas as pd
from .constant import Num_Stock, STOCK_NAME, Num_Person, strategy_flie, current_milli_time

warnings.filterwarnings('ignore')
def op_update_reward_strategy(virtual_date, persons, iter):
    for p in persons:
        if p.person_id > -1:
            if p.reflect_frequency == 0:
                pass
            elif (iter + 1) % p.reflect_frequency == 0:
                strategy=p.principle
                reward=op_reward(p, virtual_date)
                update_strategy_reward(reward, strategy)
            else:
                pass
        
def update_strategy_reward(new_reward, new_strategy):
    file_path = strategy_flie
    df = pd.read_excel(file_path)
    if len(df) > 5:
        # 找到最高得分的reward和对应的strategy的索引
        min_index = df['reward'].idxmin()
        if df.at[min_index, 'reward'] < new_reward:
        # 替换最高得分的reward和strategy
            df.at[min_index, 'reward'] = new_reward
            df.at[min_index, 'strategy'] = new_strategy
    else:
      #  new_data = {
       #                 "strategy":new_strategy,
        #                "reward": new_reward
         #           }
        new_data = pd.DataFrame([{
                "strategy": new_strategy,
                "reward": new_reward
            }])

# 将新数据添加到DataFrame
        #df.append(new_data)#, ignore_index=True)
        df = pd.concat([df, new_data], ignore_index=True)

        #df = pd.concat([df, new_data], ignore_index=True)

    # 将修改后的数据保存回Excel文件
    df.to_excel(file_path, index=False)

def op_reward(persona, virtual_date):
    #获取今天总资产，和昨天总资产
    curr_wealth = persona.wealth
    if virtual_date == 0:
        ini_wealth = [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]
        personid = persona.person_id
        last_wealth = ini_wealth[personid]
    else:
        person = persona.query_person(virtual_date-1)
        for p in person:
            last_wealth = p["wealth"]
    new_reward = (curr_wealth - last_wealth) / last_wealth * 100
    return new_reward

def parse_gossip(gossip):
    return_lists = []
    name_tags = [
        "person_id",
        "virtual_date",
        "gossip"
    ]
    for each in gossip:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def parse_memory(memory):
    return_lists = []
    name_tags = [
        "person_id",
        "virtual_date",
        "iteration",
        "stock_operations",
        "strategy",
        "type",
        "gossip",
        "analysis_for_stocks",
        "analysis_for_strategy",
        "stock_prices",
        "market_change",
        "financial_situation",
    ]
    for each in memory:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def parse_stocks(stock_str):
    return_lists = []
    name_tags = [
        "stock_id",
        "virtual_date",
        "weekday",
        "volume",
        "quantity",
        "last_price",
        "begin_price",
        "highest_price",
        "lowest_price",
    ]
    for each in stock_str:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def parse_orders(order):
    # timestamp int, virtual_date text, weekday int, "iteration" stock_id int, person_id int, type text, price float
    return_lists = []
    name_tags = [
        "timestamp",
        "virtual_date",
        "weekday",
        "iteration",
        "stock_id",
        "person_id",
        "type",
        "price",
        "quantity",
        "status",
    ]
    for each in order:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def parse_persons(persons):
    return_lists = []
    name_tags = [
        "person_id",
        "virtual_date",
        "cash",
        "asset",
        "wealth",
        "work_income",
        "capital_gain",
        "daily_expense",
        "principle",
    ]
    for each in persons:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def parse_accounts(accounts):
    return_lists = []
    name_tags = [
        "person_id",
        "stock_id",
        "virtual_date",
        "weekday",
        "quantity",
        "cost_price",
        "current_price",
        "profit",
        "start_date",
    ]
    for each in accounts:
        return_dic = {}
        for index, name in enumerate(name_tags):
            return_dic[name] = round_two_decimal(each[index])
        return_lists.append(return_dic)
    return return_lists


def round_two_decimal(input):
    if not isinstance(input, float):
        return input
    try:
        res = float("{:.2f}".format(input))
        return res
    except Exception:
        return input


def round_lists_two_decimals(lists, in_percentage=True):
    if in_percentage:
        return_list = [round_two_decimal(elem * 100) for elem in lists]
    else:
        return_list = [round_two_decimal(elem) for elem in lists]
    return return_list


def stock_name_to_id(stocks, name):
    for each_stock in stocks:
        if each_stock.stock_name == name:
            return each_stock.stock_id


def query_all_stocks(db, virtual_date):
    cmd = "select * from stock where virtual_date ={} and stock_id >= 0 order by stock_id".format(
        virtual_date, -1
    )
    db.execute_sql(cmd)
    results = db.fetchall()
    results = parse_stocks(results)
    if len(results) >= 1:
        return results
    else:
        return None
    
def query_order(person_id, virtual_date):
    conn = sqlite3.connect('save/sim01/data.db')
    cursor = conn.cursor()
    cmd = """
    SELECT *
    FROM active_orders
    WHERE person_id = {} 
    AND virtual_date = {}
    """.format(person_id, virtual_date)

    # 执行查询
    cursor.execute(cmd)
    results = cursor.fetchall()
    results=parse_orders(results)
    return_order = []
    for o in results:
        status = o["status"]
        virtual_date = o["virtual_date"]
        stock_id = o["stock_id"]
        person_id = o["person_id"]
        type = o["type"]
        price = o["price"]
        quantity = o["quantity"]
        dic = {
      
        "virtual_date": virtual_date,
        "stock_id": stock_id,
        "person_id": person_id,
        "type": type,
        "price": price,
        "quantity": quantity,
        "status": status,
        }
        for key, value in dic.items():
            dic[key] = round_two_decimal(value)
        return_order.append(dic)
    return return_order

def query_persona_order(person_id, virtual_date, begin_date=-5):
    conn = sqlite3.connect('save/sim01/data.db')
    cursor = conn.cursor()
    cmd = """
    SELECT *
    FROM active_orders
    WHERE person_id = {} 
    AND virtual_date BETWEEN '{}' AND '{}'
    """.format(person_id, begin_date, virtual_date)

    # 执行查询
    cursor.execute(cmd)
    results = cursor.fetchall()
    results=parse_orders(results)
    return_order = []
    for o in results:
        status = o["status"]
        virtual_date = o["virtual_date"]
        stock_id = o["stock_id"]
        person_id = o["person_id"]
        type = o["type"]
        price = o["price"]
        quantity = o["quantity"]
        dic = {
      
        "virtual_date": virtual_date,
        "stock_id": stock_id,
        "person_id": person_id,
        "type": type,
        "price": price,
        "quantity": quantity,
        "status": status,
        }
        for key, value in dic.items():
            dic[key] = round_two_decimal(value)
        return_order.append(dic)
    return return_order

def submit_order(
    db, order_type, person_id, stock_id, virtual_date, iteration, bid_price, quantity
):
    current_time = current_milli_time()
    if quantity <= 0:
        return  # 不下单，跳过

    assert quantity > 0
    time.sleep(0.01)
    weekday = virtual_date % 7  # a week of 7 days
    cmd_insert = "Insert Into active_orders values({},{},{},{},{},{},'{}',{},{},'active')".format(
        current_time,
        virtual_date,
        weekday,
        iteration,
        stock_id,
        person_id,
        order_type,
        bid_price,
        quantity,
    )
    db.execute_sql(cmd_insert)#存入数据库中
    
def stock_(stock_id, start_date=-4, end_date=0):
    # 连接到数据库
    conn = sqlite3.connect('save/sim01/data.db')
    cursor = conn.cursor()
    cmd = """
    SELECT *
    FROM stock
    WHERE stock_id = {} 
    AND virtual_date BETWEEN '{}' AND '{}'
    """.format(stock_id, start_date, end_date)

    # 执行查询
    cursor.execute(cmd)
    results = cursor.fetchall()
    name_tags = [
        "stock_id",
        "virtual_date",
        "weekday",
        "Volume",
        "quantity",
        "Close",
        "Open",
        "High",
        "Low",
    ]
    results = pd.DataFrame(results, columns= name_tags)
    results["date"] = pd.date_range(start='2024-08-06', periods=len(results), freq='D')
    results.set_index('date', inplace=True)

    results = results.drop(columns=['stock_id', 'weekday', 'quantity','virtual_date'])
    return results

def save_plot_stocks(virtual_date):
    for i in range(Num_Stock):
        stock_A=stock_(i, start_date=-4, end_date=virtual_date)
        #stock_B=stock_(1, start_date=-9, end_date=virtual_date)
        #stock_C=stock_(2, start_date=-9, end_date=virtual_date)
        virtual_dates=[i-4 for i in range(len(stock_A))]
        fig, axes =mpf.plot(stock_A, type='candle', style='charles', title='Daily K-line chart of stock {}'.format(STOCK_NAME[i]), ylabel='Price',returnfig=True)
        axes[0].set_xticks(range(len(virtual_dates)))  # 设置 X 轴刻度位置
        axes[0].set_xticklabels(virtual_dates)
        #plt.savefig('stock_{}_price.pdf'.format(STOCK_NAME[i]))
        #plt.close(fig)  # 确保图形关闭，释放内存
        plt.savefig('stock_{}_price.jpg'.format(STOCK_NAME[i]), dpi=500)
        plt.close(fig)

def save_plt_news_orders(virtual_date):
    buy_persons=[]
    sell_persons=[]
    for persona in range(Num_Person):
        stock_A=query_order(persona, virtual_date)
        total_buy_value = sum(item['price'] * item['quantity'] for item in stock_A if item['type'] == 'buy')
        total_sell_value = sum(item['price'] * item['quantity'] for item in stock_A if item['type'] == 'sell')
        buy_persons.append(total_buy_value)
        sell_persons.append(total_sell_value)
    while sum(buy_persons)==0 and sum(sell_persons)==0:
        virtual_date=virtual_date-1
        buy_persons=[]
        sell_persons=[]
        for persona in range(Num_Person):
            stock_A=query_order(persona, virtual_date)
            total_buy_value = sum(item['price'] * item['quantity'] for item in stock_A if item['type'] == 'buy')
            total_sell_value = sum(item['price'] * item['quantity'] for item in stock_A if item['type'] == 'sell')
            buy_persons.append(total_buy_value)
            sell_persons.append(total_sell_value)
    persons = range(0, len(buy_persons))
    # 设置柱的宽度
    bar_width = 0.35
    # 生成图表
    fig, ax = plt.subplots()
    # 条形图
    bar1 = ax.bar(np.array(persons) - bar_width/2, buy_persons, bar_width, label='Buy Assets')
    bar2 = ax.bar(np.array(persons) + bar_width/2, sell_persons, bar_width, label='Sell Assets')
    # 添加标签和标题
    ax.set_xlabel('Person')
    ax.set_ylabel('Assets')
    ax.set_title('Buy and Sell Assets for Each Person at date = {}'.format(virtual_date))
    ax.set_xticks(persons)
    ax.set_xticklabels(persons)
    ax.legend()
    plt.savefig("plot_order.jpg")
    # plt.show()  # 禁用图片显示，避免弹出窗口
    
    
def trans_url(photo_path):
    with open(photo_path, 'rb') as image_file:  # 用 rb 模式打开图像文件
        image_data = image_file.read()  # 读取图像文件内容
    image_base64 = base64.b64encode(image_data).decode('utf-8')  # 将图像内容转换为 base64 编码
    image_url = f'data:image/jpeg;base64,{image_base64}'  # 生成图像的 data URL
    return image_url 

def save_persona_order(persona, virtual_date):
# 提取数据
    buy_persons=[]
    sell_persons=[]
    data=query_persona_order(persona, virtual_date)
    stock_id_mapping = {0: 'A', 1: 'B', 2: 'C'}
    buy_dates = [d['virtual_date'] for d in data if d['type'] == 'buy']
    buy_prices = [d['price'] for d in data if d['type'] == 'buy']
    buy_stock_ids = [stock_id_mapping[d['stock_id']] for d in data if d['type'] == 'buy']
    sell_dates = [d['virtual_date'] for d in data if d['type'] == 'sell']
    sell_prices = [d['price'] for d in data if d['type'] == 'sell']
    sell_stock_ids = [stock_id_mapping[d['stock_id']] for d in data if d['type'] == 'sell']
    # 绘制散点图
    plt.figure(figsize=(10, 6))
    # 绘制买入交易
    if len(buy_dates)==0 and len(sell_dates)==0:
        plt.savefig("plot_person{}_order.jpg".format(persona))
        return True
        
    
    for i in range(len(buy_dates)):
        plt.scatter(buy_dates[i], buy_prices[i], color='blue', marker='o', label='Buy' if i == 0 else "")
        plt.text(buy_dates[i], buy_prices[i], str(buy_stock_ids[i]), fontsize=11, ha='right')
    # 绘制卖出交易
    for i in range(len(sell_dates)):
        plt.scatter(sell_dates[i], sell_prices[i], color='red', marker='x', label='Sell' if i == 0 else "")
        plt.text(sell_dates[i], sell_prices[i], str(sell_stock_ids[i]), fontsize=11, ha='right')
    # 设置图表标题和标签
    plt.title('Stock trading record of the {}th person'.format(persona))
    plt.xlabel('Virtual Date')
    plt.ylabel('Price')
    plt.xticks(np.arange(min(buy_dates + sell_dates), max(buy_dates + sell_dates) + 1, 1))
    plt.legend()
    plt.savefig("plot_person{}_order.jpg".format(persona))
    #plt.grid(True)
    # 显示图表
    # plt.show()  # 禁用图片显示，避免弹出窗口

class Database_operate:
    def __init__(self, db_name):
        self._db_name = db_name
        self._conn = None  # database connections
        self._cur = None  # database cursor

        self.init_database()

    def init_database(self):
        self._conn = sqlite3.connect("{}.db".format(self._db_name))
        self._cur = self._conn.cursor()
        cmdcre_orders = (
            "Create Table active_orders (timestamp Integer NOT NULL, virtual_date Integer, "
            "weekday INTEGER, iteration INTEGER,"
            "stock_id INTEGER, person_id INTEGER, type text check(type IN ('sell','buy')), "
            "price Numeric, quantity INTEGER, "
            "status text check (status IN ('active','closed','finished') ))"
        )
        self.execute_sql(cmdcre_orders)

        cmdcre_stock = (
            "Create Table stock (stock_id Integer NOT NULL, virtual_date Integer, "
            "weekday INTEGER,"
            "volume  Numeric, quantity INTEGER, last_price Numeric, begin_price Numeric,"
            "highest_price Numeric, lowest_price Numeric )"
        )
        self.execute_sql(cmdcre_stock)

        cmdcre_person = (
            "Create Table person (person_id Integer, virtual_date Integer, "
            "cash Numeric, asset Numeric,"
            "wealth Numeric, work_income Numeric,"
            "capital_gain Numeric, daily_expense Numeric,"
            "principle Text)"
        )
        self.execute_sql(cmdcre_person)

        cmdcre_account = (
            "Create Table account (person_id Integer, stock_id Integer, virtual_date Integer, "
            "weekday INTEGER, quantity INTEGER,"
            "cost_price Numeric, current_price Numeric, profit Numeric,"
            "start_date INTEGER)"
        )
        self.execute_sql(cmdcre_account)

        cmdcre_account = (
            "Create Table memory (person_id Integer, virtual_date Integer, iteration INTEGER, "
            "stock_operations Text, strategy Text, type Text check(type IN ('sell','buy','hold','reflect')), gossip Text, "
            "analysis_for_stocks Text, analysis_for_strategy Text, stock_prices Text, market_change Text, financial_situation Text)"
        )
        self.execute_sql(cmdcre_account)

        cmdcre_gossip = (
            "Create Table gossip (person_id Integer, virtual_date Integer, gossip Text)"
        )
        self.execute_sql(cmdcre_gossip)

    def execute_sql(self, cmd: str) -> bool:
        try:
            self._cur.execute(cmd)
            self._conn.commit()
        except Exception as e:
            print("Database ERROR:{}".format(cmd))
            print(e)
            return False
        return True

    def fetchall(self):
        return self._cur.fetchall()

    def close(self):
        self._conn.commit()
        self._conn.close()

    @property
    def cur(self):
        return self._cur
