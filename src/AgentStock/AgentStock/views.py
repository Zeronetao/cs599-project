from django.http import JsonResponse
from .utils.redis_service import RedisService
from django.core.cache import cache
import os
import string
from .Stockagent import constant
from .Stockagent.main import overall_test
import sqlite3

def paraminit(request):
    """
    初始化模拟参数接口
    接收参数: No_Days, Num_Person, Num_Stock
    """
    try:
        # 获取URL参数
        no_days = int(request.GET.get('No_Days', 11))
        num_person = int(request.GET.get('Num_Person', 4))
        num_stock = int(request.GET.get('Num_Stock', 3))
        # print(no_days, num_person, num_stock)
        # 验证参数范围
        if no_days < 1:
            return JsonResponse({
                'status': 'error',
                'message': '模拟天数必须大于1'
            })
        
        if num_person < 1 or num_person > 12:
            return JsonResponse({
                'status': 'error', 
                'message': 'Agent数量必须在1-12之间'
            })
            
        if num_stock < 1 or num_stock > 10:
            return JsonResponse({
                'status': 'error',
                'message': '股票数量必须在1-10之间'
            })

        # 根据 Num_Stock 动态生成 STOCK_NAME
        stock_names = []
        for i in range(num_stock):
            if i < 26:
                stock_names.append(string.ascii_uppercase[i])  # A, B, C, ...
            else:
                stock_names.append(f"STOCK_{i}")  # 超过26个后用 STOCK_0, STOCK_1...

        # 更新系统常量
        constant.No_Days = no_days
        constant.Num_Person = num_person
        constant.Num_Stock = num_stock
        constant.STOCK_NAME = stock_names
        print(no_days, num_person, num_stock, stock_names)
        print("constant:", constant.No_Days, constant.Num_Person, constant.Num_Stock, constant.STOCK_NAME)
        # 生成新的保存路径
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        constant.SAVE_NAME = f"sim_{timestamp}"
        constant.Save_Path = os.path.join("save", constant.SAVE_NAME)
        
        # 确保保存目录存在
        if not os.path.exists(constant.Save_Path):
            os.makedirs(constant.Save_Path)
        
        # 更新路径
        constant.persona_path = os.path.join(constant.Save_Path, "persona.json")
        constant.stock_path = os.path.join(constant.Save_Path, "stocks.json")
        
        # 初始化模拟系统
        try:
            # 调用overall_test函数开始仿真
            overall_test()
            
            return JsonResponse({
                'status': 'success',
                'message': '参数初始化成功，仿真已开始',
                'data': {
                    'No_Days': no_days,
                    'Num_Person': num_person,
                    'Num_Stock': num_stock,
                    'save_path': constant.SAVE_NAME,
                    'simulation_id': timestamp
                }
            })
            
        except Exception as init_error:
            return JsonResponse({
                'status': 'error',
                'message': f'仿真执行失败: {str(init_error)}'
            })
            
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': '参数格式错误，请确保所有参数都是有效的数字'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'服务器内部错误: {str(e)}'
        })


def testcache(request):
    data = cache.get('my_key')
    if not data:
        data = 'expensive_calculation_result'
        cache.set('my_key', data, timeout=60)  # 缓存 60 秒
        print(data)
    return JsonResponse({"message": 'ok'})
    #return JsonResponse({"message": 'ok'})

def redis_test_view(request):
    rds = RedisService()

    rds.set_value('dev:ops:string', 'hello_zsy')
    val = rds.get_value('dev:ops:string')

    # Hash
    rds.set_hash('dev:ops:hash', {'name': 'alice', 'age': '23'})
    hval = rds.get_hash('dev:ops:hash')

    # Set
    rds.add_set('dev:ops:set', 'a', 'b', 'c')
    sval = rds.get_set('dev:ops:set')

    # List
    rds.push_list('dev:ops:list', 'x', 'y', 'z')
    lval = rds.get_list('dev:ops:list')

    # SortedSet
    rds.add_zset('dev:ops:zset', {'one': 1, 'two': 2})
    zval = rds.get_zset('dev:ops:zset')

    return JsonResponse({
        'string': val,
        'hash': hval,
        'set': list(sval),
        'list': lval,
        'zset': zval,
    })


def get_simulation_results(request):
    """
    获取模拟结果数据
    参数: simulation_id (可选，默认使用sim01)
    """
    try:
        simulation_id = request.GET.get('simulation_id', 'sim01')
        db_path = os.path.join('save', simulation_id, 'data.db')
        num_stock = getattr(constant, 'Num_Stock', int(request.GET.get('Num_Stock', 3)))
        if not os.path.exists(db_path):
            # 尝试使用默认的sim01数据库
            fallback_db_path = os.path.join('save', 'sim01', 'data.db')
            if os.path.exists(fallback_db_path):
                db_path = fallback_db_path
                simulation_id = 'sim01'
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'模拟数据库文件不存在: {simulation_id}，且无法找到默认数据库'
                })
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # 获取所有agents的基本信息
            cursor.execute("""
                SELECT DISTINCT person_id, principle 
                FROM person 
                WHERE person_id >= 0
                ORDER BY person_id
            """)
            agents_info = cursor.fetchall()

            agents = []
            for person_id, principle in agents_info:
                # 获取该agent的财富变化曲线
                cursor.execute("""
                    SELECT virtual_date, wealth 
                    FROM person 
                    WHERE person_id = ? 
                    ORDER BY virtual_date
                """, (person_id,))
                wealth_data = cursor.fetchall()
                profit_curve = [float(wealth) for _, wealth in wealth_data]

                # 获取该agent的交易记录
                cursor.execute("""
                    SELECT virtual_date, type, stock_id, quantity, price 
                    FROM active_orders 
                    WHERE person_id = ? AND status = 'finished'
                    ORDER BY virtual_date, timestamp
                """, (person_id,))
                orders = cursor.fetchall()

                actions = []
                # 将stock_id转换为股票名称，从constant获取股票名称
                stock_names = getattr(constant, 'STOCK_NAME', [])
                if not stock_names:  # 如果constant中没有，则按需生成
                    for i in range(num_stock):
                        if i < 26:
                            stock_names.append(string.ascii_uppercase[i])
                        else:
                            stock_names.append(f"STOCK_{i}")
                for virtual_date, order_type, stock_id, quantity, price in orders:
                    stock_name = stock_names[stock_id] if stock_id < len(stock_names) else f'Stock{stock_id}'

                    actions.append({
                        'day': virtual_date + 1,  # 显示从第1天开始
                        'action': order_type.upper(),
                        'stock': stock_name,
                        'amount': quantity,
                        'price': float(price)
                    })

                # 获取该agent的策略描述
                cursor.execute("""
                    SELECT strategy 
                    FROM memory 
                    WHERE person_id = ? 
                    LIMIT 1
                """, (person_id,))
                strategy_result = cursor.fetchone()
                strategy = strategy_result[0] if strategy_result else principle

                agents.append({
                    'id': person_id + 1,
                    'prompt': f'Agent {person_id + 1}: {strategy}',
                    'profitCurve': profit_curve,
                    'actions': actions
                })
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'agents': agents,
                'simulation_id': simulation_id
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'获取模拟结果失败: {str(e)}'
        })


def get_stock_data(request):
    """
    获取股票价格数据
    参数: simulation_id (可选，默认使用sim01)
    """
    try:
        simulation_id = request.GET.get('simulation_id', 'sim01')
        db_path = os.path.join('save', simulation_id, 'data.db')
        
        if not os.path.exists(db_path):
            return JsonResponse({
                'status': 'error',
                'message': f'模拟数据库文件不存在: {simulation_id}'
            })
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
        
        # 获取所有股票的价格历史
            cursor.execute("""
                SELECT stock_id, virtual_date, last_price, begin_price, highest_price, lowest_price
                FROM stock 
                WHERE virtual_date >= 0
                ORDER BY stock_id, virtual_date
            """)
            stock_data = cursor.fetchall()

            stocks = {}
            stock_names = getattr(constant, 'STOCK_NAME', ['A', 'B', 'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])

            for stock_id, virtual_date, last_price, begin_price, highest_price, lowest_price in stock_data:
                # 核心过滤逻辑：跳过stock_id < 0的记录
                if stock_id < 0:
                    continue  # 不处理stock_id为负数的数据
                stock_name = stock_names[stock_id] if stock_id < len(stock_names) else f'Stock{stock_id}'

                if stock_name not in stocks:
                    stocks[stock_name] = {
                        'id': stock_id,
                        'name': stock_name,
                        'prices': []
                    }

                stocks[stock_name]['prices'].append({
                    'day': virtual_date + 1,
                    'open': float(begin_price),
                    'close': float(last_price),
                    'high': float(highest_price),
                    'low': float(lowest_price)
                })
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'stocks': list(stocks.values()),
                'simulation_id': simulation_id
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'获取股票数据失败: {str(e)}'
        })


def get_agent_comparison(request):
    """
    获取Agent对比数据，专门为Agent对比页面设计
    参数: simulation_id (可选，默认使用最新的模拟结果)
    """
    try:
        simulation_id = request.GET.get('simulation_id', 'sim01')
        '''# 如果没有指定simulation_id，使用最新的有效模拟结果
        if not simulation_id:
            save_dir = 'save'
            if os.path.exists(save_dir):
                # 获取所有sim_开头的文件夹，按时间排序
                sim_folders = [f for f in os.listdir(save_dir) if f.startswith('sim_')]
                if sim_folders:
                    sim_folders.sort(reverse=True)  # 按时间倒序
                    # 找到第一个包含data.db文件的文件夹
                    for folder in sim_folders:
                        test_db_path = os.path.join(save_dir, folder, 'data.db')
                        if os.path.exists(test_db_path):
                            simulation_id = folder
                            break
                    else:
                        # 如果没有找到有效的文件夹，使用默认值
                        simulation_id = 'sim01'
                else:
                    simulation_id = 'sim01'  # 默认值
            else:
                simulation_id = 'sim01'
                '''

        db_path = os.path.join('save', simulation_id, 'data.db')
        
        if not os.path.exists(db_path):
            return JsonResponse({
                'status': 'error',
                'message': f'模拟数据库文件不存在: {simulation_id}'
            })

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # 获取所有agents的基本信息
            cursor.execute("""
                SELECT DISTINCT person_id, principle 
                FROM person 
                WHERE person_id >= 0
                ORDER BY person_id
            """)
            agents_info = cursor.fetchall()

            agents = []
            max_days = 0

            for person_id, principle in agents_info:
                # 获取该agent的财富变化曲线
                cursor.execute("""
                    SELECT virtual_date, wealth 
                    FROM person 
                    WHERE person_id = ? 
                    ORDER BY virtual_date
                """, (person_id,))
                wealth_data = cursor.fetchall()
                profit_curve = [float(wealth) for _, wealth in wealth_data]

                # 更新最大天数
                if len(profit_curve) > max_days:
                    max_days = len(profit_curve)

                agents.append({
                    'id': person_id + 1,  # 显示从Agent 1开始
                    'profitCurve': profit_curve,
                    'finalValue': profit_curve[-1] if profit_curve else 100000
                })

            # 生成天数标签
            day_labels = [f'Day {i+1}' for i in range(max_days)]

        return JsonResponse({
            'status': 'success',
            'data': {
                'agents': agents,
                'dayLabels': day_labels,
                'simulation_id': simulation_id
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'获取Agent对比数据失败: {str(e)}'
        })
