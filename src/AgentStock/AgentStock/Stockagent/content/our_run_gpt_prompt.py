from .gpt_structure import generate_prompt, ChatGPT_safe_generate_response, ChatGPT_3images_generate_response
import ast
import re
import random
import numpy as np
import pandas as pd
import os
from ..database_utils import save_persona_order, save_plt_news_orders, save_plot_stocks
from ..constant import with_photo, with_stock_infor


def integrate_gossip(virtual_date, persona, gossip_num_max):
    all_gossip = ""
    gossip = persona.query_gossip(virtual_date)
    gossip_num = np.random.randint(0, gossip_num_max + 1)
    if gossip_num == 0:
        all_gossip = "None"
    else:
        selected_gossip = random.sample(gossip, gossip_num)
        for g in selected_gossip:
            all_gossip += "- " + g["gossip"] + "\n"
    return all_gossip



def integrate_gossip_info(virtual_date, persona):
    memory = persona.query_memory(virtual_date - 1)
    gossip_info = ""
    for m in memory:
        import os
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gossip_info_file = os.path.join(current_dir, "our_prompt_template", "gossip_info.txt")
        f = open(
            gossip_info_file,
            "r"
        )
        gossip_info_template = f.read()
        prompt_input = [
            m["Virtual_date"],
            m["Iteration"],
            m["Stock_op"],
            m["Financial_situation"],
            m["Stock_prices"],
            m["Analysis_for_stocks"],
            m["Strategy"]]
        for count, input in enumerate(prompt_input):
            gossip_info_template = gossip_info_template.replace(
                f"!<INPUT {count}>!", str(input)
            )
            if (
                "<commentblockmarker>###</commentblockmarker>"
                in gossip_info_template
            ):
                gossip_info_template = gossip_info_template.split(
                    "<commentblockmarker>###</commentblockmarker>"
                )[1]
        gossip_info += gossip_info_template
    return gossip_info


def integrate_stock_info(virtual_date, stocks_list):
    stock_info = ""
    for stock in stocks_list:
        import os
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stock_info_file = os.path.join(current_dir, "our_prompt_template", "stock_information.txt")
        f = open(
            stock_info_file,
            "r",
            encoding="utf-8",
        )
        stock_info_template = f.read()
        stock_infos = stock.query_prompt_values(virtual_date)
        for count, (key, value) in enumerate(stock_infos.items()):
            if key == "current_price_change":
                value = "+{:.2f}".format(value) if value >= 0 else "-{:.2f}".format(value)
            stock_info_template = stock_info_template.replace(
                f"!<INPUT {count}>!", str(value)
            )
            if (
                "<commentblockmarker>###</commentblockmarker>"
                in stock_info_template
            ):
                stock_info_template = stock_info_template.split(
                    "<commentblockmarker>###</commentblockmarker>"
                )[1]
        stock_info += stock_info_template
    return stock_info


def integrate_hold_info(virtual_date, persona):
    hold_list = persona.query_prompt(virtual_date)
    if len(hold_list) == 0:
        total_value = 0
        hold_info = "you do not hold any stock right now."
    else:
        hold_info = "you are holding the following stocks:"
        total_value = 0
        for hold in hold_list:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if persona.person_id not in with_stock_infor and virtual_date>=2:
                hold_info_file = os.path.join(current_dir, "our_prompt_without_price", "hold_information.txt")
                f = open(hold_info_file,"r")     
            else:
                hold_info_file = os.path.join(current_dir, "our_prompt_template", "hold_information.txt")
                f = open(hold_info_file, "r")
            hold_info_template = f.read()
            total_value += hold["total_value"]
            for count, (key, value) in enumerate(hold.items()):
                if key == "captital_gain":
                    value = "{:.2f}% PROFIT".format(value) if value >= 1e-12 else "{:.2f}% LOSS".format(abs(value))
                elif key == "Current_price_change":
                    value = "+{:.2f}".format(value) if value >= 0 else "-{:.2f}".format(value)
                hold_info_template = hold_info_template.replace(
                    f"!<INPUT {count}>!", str(value)
                )
                if (
                    "<commentblockmarker>###</commentblockmarker>"
                    in hold_info_template
                ):
                    hold_info_template = hold_info_template.split(
                        "<commentblockmarker>###</commentblockmarker>"
                    )[1]
            hold_info += hold_info_template
    begin = "Your total portfolio balance is ${:.2f}, ".format(total_value)
    hold_info = begin + hold_info
    return hold_info

def text_strategy_reward(virtual_date, p):
    file_path = r"C:\Users\mtm\Desktop\strategy.xlsx"
    df = pd.read_excel(file_path)
    prompt = ""
    for index, row in df.iterrows():
        prompt += f"{index + 1}. The investment strategy: {row['strategy']}\n   Reward: {row['reward']}\n\n"
    return prompt

    

def integrate_long_reflect_info(virtual_date, persona):
    iteration=0
    pre_reflect_info = ""
    while virtual_date>=0 and iteration<3:
        memory = persona.query_memory(virtual_date)
        for m in [memory[-1]]:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            reflect_info_file = os.path.join(current_dir, "our_prompt_template", "reflect_info.txt")
            f = open(
                reflect_info_file,
                "r"
            )
            pre_reflect_info_template = f.read()
            prompt_input = [
                m["Virtual_date"],
                m["Iteration"],
                m["Stock_op"],
                m["Financial_situation"],
                m["Market_change"],
                m["Stock_prices"],
                m["Gossip"],
                m["Strategy"]]
            for count, input in enumerate(prompt_input):
                pre_reflect_info_template = pre_reflect_info_template.replace(
                    f"!<INPUT {count}>!", str(input)
                )
                if (
                    "<commentblockmarker>###</commentblockmarker>"
                    in pre_reflect_info_template
                ):
                    pre_reflect_info_template = pre_reflect_info_template.split(
                        "<commentblockmarker>###</commentblockmarker>"
                    )[1]
            pre_reflect_info += pre_reflect_info_template
        virtual_date-=1
        iteration+=1
    return pre_reflect_info

def integrate_reflect_info(virtual_date, persona):
    memory = persona.query_memory(virtual_date)
    pre_reflect_info = ""
    for m in memory:
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reflect_info_file = os.path.join(current_dir, "our_prompt_template", "reflect_info.txt")
        f = open(
            reflect_info_file,
            "r"
        )
        pre_reflect_info_template = f.read()
        prompt_input = [
            m["Virtual_date"],
            m["Iteration"],
            m["Stock_op"],
            m["Financial_situation"],
            m["Market_change"],
            m["Stock_prices"],
            m["Gossip"],
            m["Strategy"]]
        for count, input in enumerate(prompt_input):
            pre_reflect_info_template = pre_reflect_info_template.replace(
                f"!<INPUT {count}>!", str(input)
            )
            if (
                "<commentblockmarker>###</commentblockmarker>"
                in pre_reflect_info_template
            ):
                pre_reflect_info_template = pre_reflect_info_template.split(
                    "<commentblockmarker>###</commentblockmarker>"
                )[1]
        pre_reflect_info += pre_reflect_info_template
    return pre_reflect_info


def update_strategy(virtual_date, persona, w_s, better_strategy_reward):#, long_w_s, long_w_s
    def create_prompt_input(virtual_date, persona, w_s, better_strategy_reward):
        reflect_info = integrate_reflect_info(virtual_date, persona)
        prompt_input = [
            reflect_info,
            w_s[0],
            w_s[1],
            better_strategy_reward
        ]
        return prompt_input

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):#用于查询GPT是否生成新的投资
        try:
            match = re.search(r"New investment strategy:\s*(.*?)$", gpt_response)
            if match:
                return True
            else:
                return False
        except Exception:
            return False

    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "reflect.txt")
    prompt_input = create_prompt_input(virtual_date, persona, w_s, better_strategy_reward)#, long_w_s
    prompt = generate_prompt(prompt_input, prompt_template)


    example_output = (
        "New investment strategy: [New investment strategy]"
    )
    special_instruction = ""
    fail_safe = get_fail_safe()
    output = ChatGPT_safe_generate_response(
        persona.person_id,
        prompt,
        example_output,
        special_instruction,
        100,
        fail_safe,
        __chat_func_validate,
        __chat_func_clean_up,
        True,
    ) 
    if output is not False:
        with open("relect_result.txt", "w") as file:
            file.write(output)
        print(output)
        return output

def long_reflect(virtual_date, persona):
    def create_prompt_input(virtual_date, persona):
        long_reflect_info = integrate_long_reflect_info(virtual_date, persona)
        prompt_input = [
            long_reflect_info
        ]
        return prompt_input

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            return True
        except Exception:
            return False

    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "pre_long_reflection.txt")#只有一个input
    prompt_input = create_prompt_input(virtual_date, persona)
    prompt = generate_prompt(prompt_input, prompt_template)


    example_output = (
        "Weakness: [Weakness]. Strength: [Strength]"
    )
    special_instruction = ""
    fail_safe = get_fail_safe()
    output = ChatGPT_safe_generate_response(
        persona.person_id,
        prompt,
        example_output,
        special_instruction,
        100,
        fail_safe,
        __chat_func_validate,
        __chat_func_clean_up,
        True,
    )
    if output is not False:
        return output

def pre_reflect(virtual_date, persona):
    def create_prompt_input(virtual_date, persona):
        pre_reflect_info = integrate_reflect_info(virtual_date, persona)
        prompt_input = [
            pre_reflect_info
        ]
        return prompt_input

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            match = re.search(r"Weakness:\s*(.*?).\s*Strength:\s*(.*?)$", gpt_response)
            if match:
                return True
            else:
                return False
        except Exception:
            return False

    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "pre_reflect.txt")
    prompt_input = create_prompt_input(virtual_date, persona)
    prompt = generate_prompt(prompt_input, prompt_template)


    example_output = (
        "Weakness: [Weakness]. Strength: [Strength]"
    )
    special_instruction = ""
    fail_safe = get_fail_safe()
    output = ChatGPT_safe_generate_response(
        persona.person_id,
        prompt,
        example_output,
        special_instruction,
        100,
        fail_safe,
        __chat_func_validate,
        __chat_func_clean_up,
        True,
    )
    if output is not False:
        with open("pre_reflect_result.txt", "w") as file:
            file.write(output)
        # print(output)
        return output


def run_gpt_generate_gossip(virtual_date, persona):
    def create_prompt_input(virtual_date, persona):
        gossip_input = integrate_gossip_info(virtual_date, persona)
        prompt_input = [
            gossip_input
        ]
        return prompt_input
    def plt_stock_infor(virtual_date, person_id):
        #保存了个人的股票交易图
        save_persona_order(person_id, virtual_date)
        save_plt_news_orders(virtual_date)
        save_plot_stocks(virtual_date)

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            return True
        except Exception:
            return False

    if virtual_date>=2:
        plt_stock_infor(virtual_date, persona.person_id)
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "gossip.txt")
    prompt_input = create_prompt_input(virtual_date, persona)
    prompt = generate_prompt(prompt_input, prompt_template)


    example_output = (
    )
    special_instruction = ""
    fail_safe = get_fail_safe()
    if persona.person_id in with_photo and virtual_date>=2:
        output = ChatGPT_3images_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )
    else:
        output = ChatGPT_safe_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )#gpt_response or false
    if output is not False:
        # print(output)
        return output


def analysis(virtual_date, persona, stocks_list, market_index, analysis_num, gossip_num_max):
    def create_prompt_input(virtual_date, persona, stocks_list, market_index, analysis_num, gossip_num_max):
        gossip = integrate_gossip(virtual_date, persona, gossip_num_max)
        market_index = "Current market index change: {:.2f}%".format(
            market_index.query_market_index_intraday_percentage(virtual_date) * 100
        )
        stock_info = integrate_stock_info(virtual_date, stocks_list)
        hold_info = integrate_hold_info(virtual_date, persona)
        prompt_input = [
            stock_info,
            market_index,
            gossip,
            hold_info,
            persona.principle,
            analysis_num
        ]
        return prompt_input, gossip

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        gpt_response = gpt_response.replace("The analysis results: \n", "")
        gpt_response = gpt_response.replace("The analysis results:\n", "")
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            match = re.search(
                r'^The analysis results:\s*((?:-\s.*(?:\n)?)+)$',
                gpt_response, re.MULTILINE)
            if match:
                matched_string = match.group()
                lines = matched_string.strip().split('\n')
                num_items = len(lines) - 1
                if num_items <= analysis_num:
                    return True
        except Exception:
            return False

    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "analysis.txt")
    prompt_input, gossip = create_prompt_input(virtual_date, persona, stocks_list, market_index, analysis_num, gossip_num_max)
    prompt = generate_prompt(prompt_input, prompt_template)
    

    #with open("analysis.txt", "w") as file:
     #  file.write(prompt)

    example_output = (
        "The analysis results: \n[analysis results]"
    )
    special_instruction = """Each analysis result should be started with "-", and ended with line break."""
    fail_safe = get_fail_safe()
    output = ChatGPT_safe_generate_response(
        persona.person_id,
        prompt,
        example_output,
        special_instruction,
        100,
        fail_safe,
        __chat_func_validate,
        __chat_func_clean_up,
        True,
    )


    if output is not False:
        # print(output)
        return output, gossip


def run_gpt_prompt_choose_buy_stock(virtual_date, persona, stocks_list, analysis_results):
    def create_prompt_input(virtual_date, persona, stocks_list, analysis_results):
        stock_info = integrate_stock_info(virtual_date, stocks_list)
        if persona.person_id not in with_stock_infor and virtual_date>=2:
            prompt_input = [
                persona.cash,
                persona.identity["minimum_living_expense"] * 10,
                persona.principle,
            ]
        else:
             prompt_input = [
                persona.cash,
                persona.identity["minimum_living_expense"] * 10,
                stock_info,
                analysis_results,
                persona.principle,
            ]
        return prompt_input
    def plt_stock_infor(virtual_date, person_id):
        #保存了个人的股票交易图
        save_persona_order(person_id, virtual_date)
        save_plt_news_orders(virtual_date)
        save_plot_stocks(virtual_date)

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):#整理格式
        gpt_response = gpt_response.strip("[]").split("], [")
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):#判断是否有此股票or是否买卖
        try:
            if "hold" in gpt_response or "Hold" in gpt_response:
                return "True"
            else:
                match = re.search(
                    r"^\s*Operation:\s*buy,\s*Stock name:\s*(?:Stock\s+)?\s*([A-Z]),\s*Investment Amount:\s*\$?(\d+(\.\d+)?),\s*Best Buying Price:\s*\$?(\d+(\.\d+)?)\s*$",#r"^\s*Operation:\s*(buy|sell),\s*Stock name:\s*([A-Z]),\s*The number of shares:\s*(\d+),\s*Best Price:\s*\$?(\d+(\.\d+)?)\s*$",
                    gpt_response, re.IGNORECASE
                )
                if match:
                    return True
        except Exception:
            return False

    if persona.cash < persona.identity["minimum_living_expense"] * 10:
        return "Operation: hold"

    if virtual_date>=2:
        plt_stock_infor(virtual_date, persona.person_id)
    
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if persona.person_id not in with_stock_infor and virtual_date>=2:
        prompt_template = os.path.join(current_dir, "our_prompt_without_price", "buy_based_on_analysis.txt")
    else:
        prompt_template = os.path.join(current_dir, "our_prompt_template", "buy_based_on_analysis.txt")
    prompt_input = create_prompt_input(virtual_date, persona, stocks_list, analysis_results)
    prompt = generate_prompt(prompt_input, prompt_template)
    example_output = (
        "Operation: buy, Stock name: [Stock Name], "
        "Investment Amount: [Specific Amount], Best "
        "Buying Price: [Recommended Buying Price] "
    )

    # with open("test.txt", "w") as file:
    #     file.write(prompt)

    special_instruction = "\n Please output strictly according to the requirements. \n You can only buy one type of stock at a time."
    fail_safe = get_fail_safe()
    if persona.person_id in with_photo and virtual_date>=2:
        output = ChatGPT_3images_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )
    else:
        output = ChatGPT_safe_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )#gpt_response or false
    
    if output is not False:
        print(output)
        return output[0]


def run_gpt_prompt_choose_sell_stock(
    virtual_date, persona, hold_list, analysis_results, verbose=False):
    def create_prompt_input(virtual_date, persona, analysis_results, test_input=None):
        hold_info = integrate_hold_info(virtual_date, persona)
        prompt_input = [
            persona.cash,
            persona.identity["minimum_living_expense"] * 10,
            hold_info,
            analysis_results,
            persona.principle,
        ]
        return prompt_input

    def get_fail_safe():
        return "error"

    def __chat_func_clean_up(gpt_response, prompt=""):
        gpt_response = gpt_response.strip("[]").split("], [")
        return gpt_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            if "hold" in gpt_response or "Hold" in gpt_response:
                return True
            else:
                match = re.search(
                    r"^\s*Operation:\s*sell,\s*Stock name:\s*(?:Stock\s+)?\s*([A-Z]),\s*The number of shares:\s*(\d+),\s*Best Selling Price:\s*\$?(\d+(\.\d+)?)\s*$",
                    gpt_response, re.IGNORECASE
                )
                if match:
                    return True
        except Exception:
            return False

    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_template = os.path.join(current_dir, "our_prompt_template", "sell_based_on_analysis.txt")
    # check does the person hold any stocks
    hold_list = persona.query_prompt(virtual_date)
    if len(hold_list) == 0:
        # stop query, return holding option
        return "Operation: hold"
    prompt_input = create_prompt_input(
        virtual_date, persona, analysis_results, test_input=None
    )
    prompt = generate_prompt(prompt_input, prompt_template)
    example_output = (
        "Operation: sell, Stock name: [Stock Name], The number "
        "of shares: [Specific Number of Shares], Best Selling "
        "Price: [Recommended Selling Price]"
    )

    # with open("test.txt", "w") as file:
    #     file.write(prompt)

    special_instruction = " \n Please output strictly according to the requirements. \n You can only sell one type of stock at a time."
    fail_safe = get_fail_safe()
    if persona.person_id in with_photo and virtual_date>=2:
        output = ChatGPT_3images_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )
    else:
        output = ChatGPT_safe_generate_response(
           persona.person_id,
           prompt,
           example_output,
           special_instruction,
           100,
           fail_safe,
           __chat_func_validate,
           __chat_func_clean_up,
           True,
       )#gpt_response or false
    if output is not False:
        print(output)
        return output[0]



# if __name__ == "__main__":
    # run_gpt_prompt_activity_choose("Mo")
    # run_gpt_prompt_stock_operations("Mo")
    # run_gpt_prompt_secret_news("Mo")
    # generate_focal_points("Mo")
    # run_reflect("Mo")
