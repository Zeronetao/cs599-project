from content.our_run_gpt_prompt import (
    run_gpt_prompt_choose_stock,
    run_gpt_prompt_cash_amount,
    run_gpt_prompt_stock_operations,
    run_gpt_prompt_focal_pt)
from constant import persona_path, stock_path
import json


def stock_ops(virtual_date, persons, stocks):
    # obtain the stock operations
    ops = []
    for p in persons:
        if p.person_id > -1:
            op = run_gpt_prompt_choose_stock(virtual_date, p, stocks)
            op = run_gpt_prompt_stock_operations(virtual_date, p, stocks)
            ops.append(op)
    return ops


def extract_memory(virtual_date_list, p, stocks, news=None, secret_news=None):
    stocks_memory = ""
    persons_memory = ""
    for vd in virtual_date_list:
        for s in stocks:
            stocks_memory += s.query_daily_return(vd) + "\n"
        persons_memory += p.query_account(vd) + "\n"
        persons_memory += stocks_memory
    return persons_memory


def obtain_guidance(virtual_date_list, persons, stocks):
    # obtain the guidance to update principle
    focals = []
    for p in persons:
        if p.person_id > -1:
            memory = extract_memory(virtual_date_list, p, stocks)
            foc = run_gpt_prompt_focal_pt(p, memory, n=3)
            focals.append(foc)


if __name__ == "__main__":
    json_path = "test.json"
    with open(json_path, 'r') as file:
        persona = json.load(file)
        print(persona)
