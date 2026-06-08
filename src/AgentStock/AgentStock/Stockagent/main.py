import datetime
import pickle
import sqlite3
import json
import time
import os.path as osp
from .database_utils import query_all_stocks, Database_operate, op_update_reward_strategy
from .Person import Person, Broker
from .Stock import Stock, Market_index
from .Market import Market
from .behavior import stock_ops, reflection, generate_gossip
from .constant import persona_path, stock_path, Iterations_Daily, No_Days, Save_Path, Num_quantity, Num_Person, Num_Stock, STOCK_NAME
from .load_json import save_all, load_all
import random
print("main:", No_Days, Num_Person, Num_Stock, STOCK_NAME)
def init_all(load=False):
    if load:
        (
            current_date,
            current_iteration,
            broker,
            market_index,
            market,
            stocks,
            persons,
        ) = load_all()
    else:
        # initialize all objects
        database = Database_operate(osp.join(Save_Path, "data"))
        # clear tables
        cmd = "drop table if exists active_orders"
        database.execute_sql(cmd)
        cmd = "drop table if exists stock"
        database.execute_sql(cmd)
        cmd = "drop table if exists person"
        database.execute_sql(cmd)
        cmd = "drop table if exists account"
        database.execute_sql(cmd)
        cmd = "drop table if exists memory"
        database.execute_sql(cmd)
        cmd = "drop table if exists gossip"
        database.execute_sql(cmd)

        database.init_database()

        stocks = []
        persons = []

        for i in range(Num_Stock):
            stocks.append(Stock(i, database, stock_path))
        market_index = Market_index(stocks, database)
        broker = Broker(stocks, database)

        for i in range(Num_Person):
            persons.append(Person(i, broker, stocks, database, persona_path))
        persons.append(broker)
        market = Market(broker, persons, stocks, database)

    return 0, 0, broker, market_index, market, stocks, persons


def overall_test():
    (
        current_date,
        current_iteration,
        broker,
        market_index,
        market,
        stocks,
        persons,
    ) = init_all(False)#初始化
    for virtual_date in range(No_Days):#8天
       # if market.sum_quantity<Num_quantity:
            if virtual_date == 0:
                broker.ipo(virtual_date)
            market_index.update_market_index(virtual_date)
            generate_gossip(virtual_date, persons, stocks)
            for iter in range(Iterations_Daily):#3
                ops = stock_ops(virtual_date, persons, stocks, market_index, iter)
                #list = ["buy",stock_name_buy,price,quantity]
                rand = random.sample(range(0,Num_Person),Num_Person)
                #print(result)
                for i in rand:
                #for i in range(9):
                    for j in range(2): #这里的j有什么用呢？
                        op = ops[i][j]
                        persons[i].create_order(i, op, virtual_date, iter)#对每个person进行交易并记录
                print("op:",op)
                market.match_order(virtual_date) #？
                market.end_of_market(virtual_date)
                market_index.update_market_index(virtual_date)
                for each_person in persons:
                    if each_person.person_id >= 0:
                        each_person.end_of_iteration(virtual_date, iter)
                #第一天的策略更新不起作用，主要是后面
                #op_update_reward_strategy(virtual_date, persons, iter)
                #reflection(virtual_date, persons, stocks, market_index, iter)
                print("---------------------------")
                save_all(virtual_date, iter, stocks, market_index, persons, market)
    
            # end of a trading day
            market.end_of_day(virtual_date)
            for each_person in persons:
                each_person.end_of_day(virtual_date)#结束当天交易
            for each_stock in stocks:
                each_stock.end_of_day(virtual_date)
            market_index.end_of_day(virtual_date)
        


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    overall_test()
    # time_test()
    # db_op3()
    # pickle_test()
    # pickle_load()
