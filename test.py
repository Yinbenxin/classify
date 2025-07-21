# -*- coding: utf-8 -*-

"""
一个最终完整版的数据生成脚本，为全部65个类别创建具有动态列的、高度真实的CSV文件。
作者: Gemini
版本: 3.0 (Final)
日期: 2025-07-07
特性:
- 完整实现了所有65个类别的数据生成逻辑和Schema配置。
- 引入“核心字段”和“可选字段”，使每个CSV文件的列结构动态变化。
- 随机化列的顺序，增强真实性。
- 即开即用，无需修改。
"""

import os
import csv
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

# --- 全局配置 ---
fake = Faker('zh_CN')
BASE_OUTPUT_DIR = "generated_data_final"
FILES_PER_CATEGORY = 100
MIN_ROWS_PER_FILE = 50
MAX_ROWS_PER_FILE = 200

# --- 辅助数据列表 ---
ETHNIC_GROUPS = ["汉族", "蒙古族", "回族", "藏族", "维吾尔族", "苗族", "彝族", "壮族", "布依族", "朝鲜族", "满族"]
RELATIONSHIPS = ["本人", "配偶", "子女", "父母", "兄弟姐妹"]
DISEASES = ["急性上呼吸道感染", "高血压", "II型糖尿病", "肺炎", "急性阑尾炎", "慢性胃炎", "冠状动脉心脏病", "过敏性鼻炎"]
ALLERGIES = ["无", "青霉素", "头孢菌素", "磺胺类药物", "海鲜", "花粉", "芒果", "花生"]
EDUCATION_DEGREES = ["博士研究生", "硕士研究生", "本科", "大专", "高中", "中专"]
BANK_TRANSACTION_TYPES = ["存款", "取款", "转账", "消费", "还款", "理财申购", "工资发放"]
LOGISTICS_STATUS = ["已揽收", "运输中", "派送中", "已签收", "异常件", "已退回"]
ECOMMERCE_ACTIONS = ["浏览商品", "搜索关键词", "添加至购物车", "提交订单", "完成支付", "发表评论", "申请退款"]
VEHICLE_MAINTENANCE_ITEMS = ["更换机油机滤", "四轮定位", "更换轮胎", "钣金喷漆", "清洗节气门", "更换火花塞"]
HOTEL_CHANNELS = ["官方App", "OTA平台(携程)", "OTA平台(飞猪)", "电话预定", "前台直接入住"]

# --- 数据生成器 (为每个类别提供所有可能字段) ---

def get_master_data_01_personal_basic_info():
    return {"姓名": fake.name(), "生日": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'), "性别": random.choice(["男", "女"]), "民族": random.choice(ETHNIC_GROUPS), "国籍": "中国", "家庭关系": random.choice(RELATIONSHIPS), "住址": fake.address(), "个人电话号码": fake.phone_number(), "电子邮件地址": fake.email()}
def get_master_data_02_personal_identity():
    doc_type = random.choice(['身份证', '护照', '驾驶证', '工作证', '社保卡', '居住证'])
    issue_date = fake.date_this_decade()
    expiry_date = issue_date + timedelta(days=365 * random.randint(5, 20))
    if doc_type == '身份证': id_num, issuer = fake.ssn(), f"{fake.province()}省{fake.city()}市公安局某某分局"
    elif doc_type == '护照': id_num, issuer = 'E' + str(random.randint(10000000, 99999999)), "国家移民管理局"
    else: id_num, issuer = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=18)), fake.company() + "印发"
    return {"姓名": fake.name(), "证件类型": doc_type, "证件号码": id_num, "签发机关": issuer, "有效期限": f"{issue_date.strftime('%Y.%m.%d')}-{expiry_date.strftime('%Y.%m.%d')}"}
def get_master_data_03_personal_health():
    return {"记录ID": uuid.uuid4(), "姓名": fake.name(), "病症": random.choice(DISEASES), "以往病史": random.choice(DISEASES + ["无"]), "药物食物过敏信息": random.choice(ALLERGIES), "身高(cm)": random.randint(150, 190), "体重(kg)": round(random.uniform(45.0, 95.0), 1), "肺活量(ml)": random.randint(2500, 5500), "家族病史": random.choice(["高血压", "糖尿病", "无"]), "生育信息": random.choice(["已育", "未育"])}
def get_master_data_04_personal_education_work():
    start_date = fake.date_of_birth(minimum_age=22, maximum_age=40); end_date = start_date + timedelta(days=365 * 4)
    return {"姓名": fake.name(), "工作单位": fake.company(), "职位": fake.job(), "学历": random.choice(EDUCATION_DEGREES), "学位": random.choice(["学士", "硕士", "博士", "无"]), "教育经历": f"{start_date.year}-{end_date.year} {fake.city()}大学", "工作经历": fake.sentence(nb_words=8), "培训记录": fake.sentence(nb_words=6), "成绩单": f"平均绩点: {round(random.uniform(2.5, 4.0), 2)}"}
def get_master_data_05_personal_property():
    return {"账户持有人": fake.name(), "银行账户": fake.bban(), "交易流水号": uuid.uuid4(), "交易类型": random.choice(BANK_TRANSACTION_TYPES), "交易金额": round(random.uniform(-50000.0, 50000.0), 2), "交易时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "房产信息": f"{fake.city()}{fake.street_name()}{random.randint(1,200)}号", "征信分数": random.randint(400, 850), "虚拟货币": f"{round(random.uniform(0.1, 5), 4)} BTC"}
def get_master_data_06_personal_communication():
    return {"主叫号码": fake.phone_number(), "被叫号码": fake.phone_number(), "通话开始时间": fake.date_time_this_month().strftime('%Y-%m-%d %H:%M:%S'), "通话时长(秒)": random.randint(10, 1800), "通信类型": random.choice(["语音通话", "短信", "彩信", "电子邮件"]), "短信内容": fake.sentence() if random.random() > 0.5 else None}
def get_master_data_07_contacts_info():
    return {"姓名": fake.name(), "电话": fake.phone_number(), "电子邮件": fake.email(), "分组": random.choice(["家人", "同事", "朋友", "未分组"]), "备注": fake.word(), "好友列表": f"好友_{fake.name()}", "群列表": f"群_{fake.word()}"}
def get_master_data_08_online_records():
    return {"用户ID": uuid.uuid4(), "访问URL": fake.uri(), "访问时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "操作类型": random.choice(ECOMMERCE_ACTIONS), "停留时长(秒)": random.randint(5, 600), "收藏列表": fake.uri() if random.random()>0.7 else None, "软件使用记录": f"{fake.word()}.exe"}
def get_master_data_09_device_info():
    return {"硬件序列号": uuid.uuid4(), "设备MAC地址": fake.mac_address(), "软件列表": f"{fake.word()}.app,{fake.word()}.app", "IMEI": fake.imei(), "Android_ID": fake.android_platform_token(), "IDFA": fake.ios_platform_token(), "SIM卡IMSI": f"4600{random.randint(0,9)}{fake.random_number(digits=12)}"}
def get_master_data_10_location_info():
    return {"用户ID": uuid.uuid4(), "经度": fake.longitude(), "纬度": fake.latitude(), "时间戳": fake.iso8601(), "行踪轨迹描述": fake.address(), "精准定位信息": random.choice(["GPS", "Wi-Fi", "基站"]), "住宿信息": fake.company() + "酒店" if random.random()>0.8 else None}
def get_master_data_11_banking():
    return {"客户ID": fake.random_number(digits=10), "账户流水号": uuid.uuid4(), "交易类型": random.choice(BANK_TRANSACTION_TYPES), "金额": round(random.uniform(-100000, 500000), 2), "交易时间": fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'), "风险评级": random.choice(["低", "中", "高"]), "反洗钱(AML)标记": random.choice([True, False]), "对方账户": fake.bban(), "摘要": fake.word()}
def get_master_data_12_securities():
    return {"股票代码": f"{random.randint(0, 600000):06d}.{random.choice(['SH', 'SZ'])}", "时间": fake.date_time_this_month().strftime('%Y-%m-%d %H:%M:%S'), "开盘价": round(random.uniform(5, 150), 2), "收盘价": round(random.uniform(5, 150), 2), "成交量(手)": random.randint(1000, 1000000), "投资者ID": uuid.uuid4(), "委托类型": random.choice(["限价买入", "市价卖出"]), "上市公司财报": f"{fake.year()}年报"}
def get_master_data_13_insurance():
    return {"保单号": f"P{fake.random_number(digits=12)}", "投保人": fake.name(), "被保人": fake.name(), "险种": random.choice(["健康险", "意外险", "寿险", "车险"]), "保费(元)": round(random.uniform(200, 20000), 2), "保险金额(元)": round(random.uniform(10000, 1000000), 2), "理赔状态": random.choice(["未出险", "理赔中", "已赔付", "已拒赔"]), "健康告知": random.choice(["无异常", "有住院史"])}
def get_master_data_14_fintech():
    return {"支付流水号": uuid.uuid4(), "用户ID": fake.random_number(digits=10), "商户名称": fake.company(), "支付方式": random.choice(["微信支付", "支付宝", "银行卡"]), "金额": round(random.uniform(1, 5000), 2), "状态": "支付成功", "时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "P2P借贷记录": f"借款{random.randint(5,20)}万元"}
def get_master_data_15_trust_leasing():
    return {"合同编号": f"TR{fake.random_number(digits=10)}", "产品名称": f"{fake.word()}信托{random.randint(1,10)}号", "受益人": fake.name(), "合同金额": round(random.uniform(100000, 5000000), 2), "租赁物信息": f"设备-{random.choice(['A','B'])}-{random.randint(100,999)}", "起租日": fake.date_this_decade().strftime('%Y-%m-%d')}
def get_master_data_16_vc_pe():
    return {"项目公司": fake.company(), "融资轮次": random.choice(["天使轮", "A轮", "B轮", "C轮", "Pre-IPO"]), "投资金额(万美元)": random.randint(50, 5000), "投后估值(万美元)": random.randint(500, 50000), "投资日期": fake.date_this_decade().strftime('%Y-%m-%d'), "所属行业": fake.bs(), "尽职调查数据": "财务、法务尽调完成"}
def get_master_data_17_public_security_justice():
    return {"案件编号": f"AJ{datetime.now().year}{fake.random_number(digits=8)}", "案件类型": random.choice(["刑事案件", "民事纠纷", "交通违法"]), "报案时间": fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'), "当事人": fake.name(), "处理状态": random.choice(["立案", "侦查中", "已结案"]), "人口户籍": fake.address(), "车辆管理": fake.license_plate(), "出入境记录": random.choice(["有", "无"])}
def get_master_data_18_market_regulation():
    return {"统一社会信用代码": fake.credit_card_number(card_type='mastercard'), "企业名称": fake.company(), "注册资本(万元)": random.randint(100, 10000), "成立日期": fake.date_of_birth(minimum_age=1, maximum_age=30).strftime('%Y-%m-%d'), "经营范围": fake.bs(), "行政处罚记录": random.choice(["无", f"罚款{random.randint(1,10)}万元"]), "知识产权": f"专利号:{fake.random_number(digits=10)}"}
def get_master_data_19_taxation_finance():
    return {"纳税人识别号": fake.credit_card_number(card_type='visa'), "发票代码": f"{fake.random_number(digits=10)}", "发票号码": f"{fake.random_number(digits=8)}", "开票日期": fake.date_this_year().strftime('%Y-%m-%d'), "含税金额": round(random.uniform(100, 100000), 2), "税率": random.choice([0.03, 0.06, 0.09, 0.13]), "财政收支": f"收入{random.randint(1000,5000)}万"}
def get_master_data_20_civil_social_security():
    return {"登记证号": f"MZ{fake.random_number(digits=10)}", "业务类型": random.choice(["婚姻登记", "社会救助申请", "养老金发放"]), "当事人": fake.name(), "发生日期": fake.date_this_decade().strftime('%Y-%m-%d'), "金额(元)": round(random.uniform(500, 5000), 2), "医保缴纳记录": "连续缴纳"}
def get_master_data_21_public_health():
    return {"上报卡号": uuid.uuid4(), "传染病名称": random.choice(["流行性感冒", "水痘", "肺结核"]), "发病日期": fake.date_this_year().strftime('%Y-%m-%d'), "上报单位": f"{fake.city()}疾病预防控制中心", "疫苗接种记录": f"{random.choice(['甲肝','乙肝','新冠'])}疫苗", "医保基金运行数据": f"支出{random.randint(1,10)}亿"}
def get_master_data_22_education_research():
    return {"学号": fake.random_number(digits=12), "姓名": fake.name(), "课程名称": random.choice(["高等数学", "大学物理", "线性代数"]), "成绩": random.randint(60, 100), "科研项目名称": f"关于{fake.word()}的研究", "项目经费(万元)": random.randint(10, 200), "学术论文": fake.sentence()}
def get_master_data_23_natural_resources_env():
    return {"监测点ID": f"ENV{random.randint(100,999)}", "时间": fake.iso8601(), "PM2.5": random.randint(10, 200), "噪音(dB)": random.randint(30, 90), "水质PH值": round(random.uniform(6.0, 8.5), 1), "天气": random.choice(["晴", "多云", "雨"]), "污染源排放": f"SO2: {round(random.uniform(1,20),1)}mg/m³"}
def get_master_data_24_urban_management():
    return {"设施ID": f"UM-{random.choice(['Light','Well'])}-{random.randint(1000,9999)}", "设施类型": random.choice(["智能路灯", "井盖", "公共停车场"]), "状态": random.choice(["正常", "故障", "维修中"]), "上报时间": fake.iso8601(), "位置": fake.street_name(), "人流密度监测": f"{random.randint(1,100)}人/百平米"}
def get_master_data_25_emergency_management():
    return {"事件编号": f"EM{datetime.now().year}{fake.random_number(digits=6)}", "事件类型": random.choice(["安全生产事故", "自然灾害"]), "发生时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "报告单位": fake.company(), "应急物资储备": f"{random.choice(['帐篷','食品','药品'])} {random.randint(10,100)}件", "灾害评估": "中等"}
def get_master_data_26_national_statistics():
    return {"统计周期": f"{fake.year()}{random.choice(['Q1','Q2','Q3','Q4'])}", "指标名称": random.choice(["国内生产总值(GDP)", "居民消费价格指数(CPI)", "工业生产者出厂价格指数(PPI)"]), "数值": round(random.uniform(-2, 10), 2), "单位": random.choice(["%", "万亿元"]), "人口普查数据": f"总人口 {round(random.uniform(14,14.2),2)}亿"}
def get_master_data_27_electronics_semiconductor():
    return {"批次号": f"B{fake.random_number(digits=12)}", "产品型号": f"Chip-{random.choice(['A','B','C'])}{random.randint(100,999)}", "晶圆制造良率(%)": round(random.uniform(85.0, 99.5), 2), "封装测试数据": random.choice(["PASS", "FAIL"]), "SMT产线数据": "正常", "电子元器件BOM表": f"BOM-{fake.random_number(digits=6)}"}
def get_master_data_28_heavy_industry_equipment():
    return {"设备ID": f"DEV-{fake.random_number(digits=5)}", "时间戳": fake.iso8601(), "温度(C)": round(random.uniform(20, 100), 1), "压力(Pa)": round(random.uniform(1, 10), 2), "转速(rpm)": random.randint(1000, 3000), "设备健康监测(PHM)": random.choice(['正常', '预警']), "供应链订单": f"ORD-{fake.random_number(digits=8)}"}
def get_master_data_29_chemical_new_materials():
    return {"反应釜编号": f"R{random.randint(1,20)}", "生产批号": f"P{fake.random_number(digits=8)}", "生产配方ID": uuid.uuid4(), "温度(℃)": round(random.uniform(50, 200), 2), "压力(MPa)": round(random.uniform(0.1, 1.5), 2), "危化品仓储": f"库位 {random.choice(['A','B'])}-{random.randint(1,5)}"}
def get_master_data_30_raw_materials_mining():
    return {"矿区编号": f"MINE-{random.choice(['A','B','C'])}", "勘探数据": f"P{random.randint(1,100)}", "矿石品位(%)": round(random.uniform(0.5, 15), 2), "设备运行日志": random.choice(["运行", "停机"]), "安全监控": random.choice(["瓦斯正常", "粉尘超标"]), "大宗商品价格": f"{round(random.uniform(500,1000),2)} USD/T"}
def get_master_data_31_vehicle_randd_manufacturing():
    return {"车辆识别代号(VIN)": fake.vin(), "零部件清单": f"BOM-{fake.random_number(digits=8)}", "生产线节拍(秒)": random.randint(50, 70), "整车质检(VQ)结果": random.choice(["合格", "返修"]), "下线时间": fake.date_time_this_month().strftime('%Y-%m-%d %H:%M:%S'), "碰撞仿真数据": "PASS"}
def get_master_data_32_sales_distribution():
    return {"经销商代码": f"DLR{random.randint(1000,9999)}", "车型": f"Model {random.choice(['X','Y','Z'])}", "汽车销量": random.randint(10, 200), "销售日期": fake.date_this_month().strftime('%Y-%m-%d'), "消费者画像": f"{random.choice(['青年','中年'])},{random.choice(['男','女'])},{fake.job()}", "经销商库存": random.randint(20,500)}
def get_master_data_33_after_sales_service():
    return {"工单号": f"WO{fake.random_number(digits=10)}", "车辆识别代号(VIN)": fake.vin(), "维保项目": random.choice(VEHICLE_MAINTENANCE_ITEMS), "零配件更换数据": f"Part-{fake.random_number(digits=6)}", "索赔数据": round(random.uniform(200, 5000), 2), "客户满意度调查": random.randint(1, 5)}
def get_master_data_34_connected_vehicles():
    return {"车辆识别代号(VIN)": fake.vin(), "时间戳": fake.iso8601(), "经度": fake.longitude(), "纬度": fake.latitude(), "速度(km/h)": random.randint(0, 120), "驾驶行为数据": random.choice(["正常", "急加速", "急刹车", "超速"]), "车载传感器(Lidar)数据": "正常"}
def get_master_data_35_passenger_transport():
    return {"票号": f"{random.choice(['T','F'])}{fake.random_number(digits=12)}", "班次": f"{random.choice(['G','D','CA','MU'])}{random.randint(100,9999)}", "始发站": fake.city(), "终点站": fake.city(), "出发时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "旅客姓名": fake.name(), "正点率": f"{random.randint(90,100)}%"}
def get_master_data_36_freight_logistics():
    return {"运单号": f"EXP{fake.random_number(digits=12)}", "发件人": fake.name(), "收件人": fake.name(), "货物追踪": random.choice(LOGISTICS_STATUS), "车辆载货率(%)": random.randint(60, 100), "冷链温度监控(℃)": round(random.uniform(2, 8), 1) if random.random() > 0.8 else None}
def get_master_data_37_warehousing():
    return {"SKU": f"SKU{fake.random_number(digits=8)}", "商品名称": fake.word(), "操作类型": random.choice(["入库", "出库", "盘点"]), "数量": random.randint(1, 500), "库位管理": f"{random.choice(['A','B','C'])}-{random.randint(1,5)}-{random.randint(1,10)}", "WMS系统日志": "操作成功"}
def get_master_data_38_mobility_services():
    return {"订单号": uuid.uuid4(), "服务类型": random.choice(["网约车", "共享单车", "共享汽车"]), "用户ID": fake.random_number(digits=10), "开始时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "行程费用(元)": round(random.uniform(5, 150), 2), "行程时长(分钟)": random.randint(5, 120)}
def get_master_data_39_electricity_power():
    return {"智能电表号(AMI)": fake.random_number(digits=12), "时间点": (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:00:00'), "用电量(kWh)": round(random.uniform(0.1, 5), 3), "电网负荷(MW)": random.randint(30000, 80000), "发电厂出力数据(MW)": random.randint(100,1000), "输配电线路状态": "正常"}
def get_master_data_40_oil_gas():
    return {"油井ID": f"OILWELL-{random.randint(1,100)}", "管道压力(MPa)": round(random.uniform(4, 10), 2), "管道流量(m³/h)": random.randint(100, 1000), "加油站ID": f"GAS-{random.randint(1,500)}", "油品": "95号汽油", "销量(升)": round(random.uniform(1000, 5000), 2)}
def get_master_data_41_water_utilities():
    return {"智能水表号": fake.random_number(digits=12), "读数(m³)": round(random.uniform(100, 2000), 2), "时间": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'), "供水管网漏损监测": random.choice(["正常", "疑似泄漏"]), "污水处理水质(COD)": round(random.uniform(10, 50), 1)}
def get_master_data_42_renewable_energy():
    return {"电场ID": f"RE-{random.choice(['WIND','SOLAR'])}-{random.randint(1,50)}", "时间戳": fake.iso8601(), "发电功率(MW)": round(random.uniform(10, 200), 2), "天气预测": random.choice(["晴", "多云"]), "储能设备充放电数据(MWh)": round(random.uniform(-50, 50), 2), "碳交易数据(吨)": random.randint(100,1000)}
def get_master_data_43_ecommerce():
    return {"用户ID": uuid.uuid4(), "商品ID": fake.random_number(digits=8), "用户行为日志": random.choice(ECOMMERCE_ACTIONS), "订单交易": f"ORD{fake.random_number(digits=10)}" if random.random() > 0.5 else None, "访问时间": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "用户评价": fake.sentence(), "购物车数据": "商品ID: " + str(fake.random_number(digits=8))}
def get_master_data_44_offline_retail():
    return {"POS机销售流水": f"POS{fake.random_number(digits=10)}", "门店ID": f"STORE{random.randint(1,100)}", "商品条码": fake.ean(length=13), "数量": random.randint(1, 5), "会员消费记录": fake.random_number(digits=8) if random.choice([True,False]) else None, "客流统计": random.randint(100, 2000)}
def get_master_data_45_cpg():
    return {"产品名称": random.choice(["可乐", "方便面", "洗发水"]), "渠道分销数据": random.choice(["大卖场", "便利店", "线上旗舰店"]), "市场份额(%)": round(random.uniform(5, 40), 1), "品牌推广活动效果": random.choice(["优", "良", "中"]), "消费者调研问卷ID": uuid.uuid4()}
def get_master_data_46_medical_institutions():
    return {"电子病历号(EMR)": f"EMR{fake.random_number(digits=10)}", "患者姓名": fake.name(), "诊断": random.choice(DISEASES), "检验(LIS)结果": "白细胞计数 " + str(round(random.uniform(4.0, 10.0), 1)), "医学影像(CT)号": f"CT{fake.random_number(digits=8)}", "住院记录(HIS)": "住院中", "处方数据": "阿莫西林"}
def get_master_data_47_life_sciences_pharma():
    return {"临床试验编号": f"CLI-{fake.random_number(digits=6)}", "基因测序数据ID": f"GENE{fake.random_number(digits=8)}", "药物研发数据": f"Target-{fake.word().upper()}", "药品流通数据": f"批号 {fake.random_number(digits=8)}", "不良反应报告ID": uuid.uuid4()}
def get_master_data_48_medical_devices():
    return {"设备序列号": uuid.uuid4(), "设备类型": random.choice(["监护仪", "呼吸机", "MRI"]), "设备使用日志": "正常运行", "性能参数": f"心率: {random.randint(60,100)}, 血氧: {random.randint(95,100)}", "植入式设备监测数据": "信号良好", "销售与维护记录": "已售"}
def get_master_data_49_health_management():
    return {"用户ID": uuid.uuid4(), "可穿戴设备": "智能手环", "体征数据": f"步数: {random.randint(2000, 20000)}", "体检报告": "正常", "营养膳食记录": "均衡", "心理咨询记录": "无"}
def get_master_data_50_real_estate():
    return {"楼盘名称": f"{fake.city_name()}一号", "户型图": f"{random.randint(2,5)}室{random.randint(1,2)}厅", "购房者数据": fake.name(), "房产交易价格(万元)": random.randint(100, 2000), "中介带看记录": random.choice(["有", "无"]), "地块信息": f"地块编号 {fake.random_number(digits=6)}"}
def get_master_data_51_construction_engineering():
    return {"项目编号": f"PROJ{fake.random_number(digits=6)}", "建筑信息模型(BIM)数据ID": uuid.uuid4(), "工程项目进度(%)": random.randint(1, 100), "建材采购与消耗": f"混凝土 {random.randint(100,1000)}方", "施工安全日志": random.choice(["一切正常", "发现安全隐患"])}
def get_master_data_52_property_management():
    return {"住户信息": f"{random.randint(1,30)}-{random.randint(1,5)}-{random.randint(101,3002)}", "物业费收缴记录": random.choice(["已缴清", "欠费"]), "门禁数据": fake.date_time_this_month().strftime('%Y-%m-%d %H:%M:%S'), "监控数据": "正常", "公共设施维修保养记录": "电梯已保养"}
def get_master_data_53_news_publishing():
    return {"文章ID": uuid.uuid4(), "文章点击率(%)": round(random.uniform(1, 20), 2), "读者画像": f"{random.choice(['青年','中年'])},{fake.job()}", "订阅数据": random.choice([True, False]), "舆情监测数据": "中性"}
def get_master_data_54_media_streaming():
    return {"用户ID": uuid.uuid4(), "影片名称": fake.sentence(nb_words=3), "收视率(%)": round(random.uniform(0.1, 5), 2), "票房数据(万元)": random.randint(1000, 50000), "流媒体用户播放行为": random.choice(["播放", "暂停", "快进"]), "付费会员数据": random.choice([True, False])}
def get_master_data_55_gaming():
    return {"玩家ID": uuid.uuid4(), "登录信息": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'), "游戏内行为": random.choice(["任务", "消费", "社交"]), "虚拟道具交易": f"{round(random.uniform(0, 1000), 2)}元", "玩家社交关系": "添加好友"}
def get_master_data_56_sports():
    return {"运动员ID": fake.random_number(digits=6), "赛场表现数据": f"完赛时间 {random.randint(2,5)}:{random.randint(0,59)}:{random.randint(0,59)}", "生理数据": f"心率 {random.randint(120,180)}", "赛事票务": "已售罄", "体育用品销售(元)": round(random.uniform(100,2000),2), "博彩赔率数据": f"1:{round(random.uniform(1.1,5.0),2)}"}
def get_master_data_57_hotel_accommodation():
    return {"订单号": uuid.uuid4(), "预订渠道数据": random.choice(HOTEL_CHANNELS), "入住率(%)": random.randint(50, 100), "平均房价(ADR)": round(random.uniform(200, 3000), 2), "客户评价": random.randint(1, 5), "会员积分": random.randint(100,10000)}
def get_master_data_58_catering():
    return {"订单号": uuid.uuid4(), "菜品销量": random.randint(1, 30), "外卖订单": random.choice(["有", "无"]), "顾客翻台率": round(random.uniform(1, 5), 1), "食材采购": f"{fake.word()} {random.randint(10,50)}kg", "库存": f"{fake.word()} {random.randint(1,20)}kg"}
def get_master_data_59_tourism():
    return {"OTA订单号": uuid.uuid4(), "线路产品数据": f"{fake.city()}5日游", "景点客流量": random.randint(1000, 20000), "游客来源地": fake.province(), "游客目的地": fake.city(), "消费金额(元)": round(random.uniform(500, 8000), 2)}
def get_master_data_60_farming():
    return {"地块编号": f"FARM-{random.randint(1,100)}", "土壤墒情(%)": round(random.uniform(20, 80), 1), "气象数据": f"{random.choice(['晴','雨'])}, {random.randint(15,35)}℃", "无人机遥感影像ID": uuid.uuid4(), "作物长势监测": random.choice(["良好", "一般", "差"]), "农产品价格(元/kg)": round(random.uniform(2,30),2)}
def get_master_data_61_animal_husbandry():
    return {"牲畜ID": f"ANML-{fake.random_number(digits=6)}", "牲畜谱系": "荷斯坦牛", "健康档案": "正常", "智能项圈活动数据": random.randint(1000, 8000), "产出量(kg)": round(random.uniform(20, 40), 1), "饲料消耗(kg)": round(random.uniform(40, 80), 1)}
def get_master_data_62_fishery_aquaculture():
    return {"渔船捕捞日志ID": uuid.uuid4(), "水产养殖区水质监测(溶氧mg/L)": round(random.uniform(5, 10), 1), "鱼群声呐探测": f"{random.randint(1000,5000)}条", "饲料投喂数据(kg)": round(random.uniform(50, 200), 1)}
def get_master_data_63_legal_services():
    return {"案件卷宗号": f"LAW-{fake.random_number(digits=8)}", "客户名称": fake.company(), "服务类型": random.choice(["法律咨询", "合同审查", "诉讼代理"]), "工时记录(小时)": round(random.uniform(1, 20), 1), "法律文书库": "律师函"}
def get_master_data_64_consulting_auditing():
    return {"项目编号": f"CON-{fake.random_number(digits=6)}", "客户行业": fake.bs(), "市场研究报告ID": uuid.uuid4(), "企业财务审计底稿": "已归档", "咨询项目交付成果": "PPT报告, Excel模型"}
def get_master_data_65_human_resources():
    return {"候选人ID": uuid.uuid4(), "应聘职位": fake.job(), "招聘渠道效能分析": random.choice(["优", "良", "中"]), "候选人简历库": "已入库", "薪酬调查报告": f"{random.randint(10,50)}k-{random.randint(20,80)}k", "员工满意度调研": round(random.uniform(1,5),1)}

# --- 类别模式(Schema)定义 (完整版) ---
CATEGORY_SCHEMAS = {
    "01_personal_basic_info": {"name": "个人基本资料", "core": ["姓名", "性别"], "optional": ["生日", "民族", "国籍", "家庭关系", "住址", "个人电话号码", "电子邮件地址"], "generator": get_master_data_01_personal_basic_info},
    "02_personal_identity": {"name": "个人身份信息", "core": ["姓名", "证件类型", "证件号码"], "optional": ["签发机关", "有效期限"], "generator": get_master_data_02_personal_identity},
    "03_personal_health": {"name": "个人健康生理信息", "core": ["记录ID", "姓名", "病症"], "optional": ["以往病史", "药物食物过敏信息", "身高(cm)", "体重(kg)", "肺活量(ml)", "家族病史", "生育信息"], "generator": get_master_data_03_personal_health},
    "04_personal_education_work": {"name": "个人教育工作信息", "core": ["姓名", "工作单位", "职位"], "optional": ["学历", "学位", "教育经历", "工作经历", "培训记录", "成绩单"], "generator": get_master_data_04_personal_education_work},
    "05_personal_property": {"name": "个人财产信息", "core": ["账户持有人", "银行账户", "交易流水号"], "optional": ["交易类型", "交易金额", "交易时间", "房产信息", "征信分数", "虚拟货币"], "generator": get_master_data_05_personal_property},
    "06_personal_communication": {"name": "个人通信信息", "core": ["主叫号码", "被叫号码", "通信类型"], "optional": ["通话开始时间", "通话时长(秒)", "短信内容"], "generator": get_master_data_06_personal_communication},
    "07_contacts_info": {"name": "联系人信息", "core": ["姓名", "电话"], "optional": ["电子邮件", "分组", "备注", "好友列表", "群列表"], "generator": get_master_data_07_contacts_info},
    "08_online_records": {"name": "个人上网记录", "core": ["用户ID", "访问URL"], "optional": ["访问时间", "操作类型", "停留时长(秒)", "收藏列表", "软件使用记录"], "generator": get_master_data_08_online_records},
    "09_device_info": {"name": "个人常用设备信息", "core": ["设备MAC地址"], "optional": ["硬件序列号", "软件列表", "IMEI", "Android_ID", "IDFA", "SIM卡IMSI"], "generator": get_master_data_09_device_info},
    "10_location_info": {"name": "个人位置信息", "core": ["用户ID", "经度", "纬度", "时间戳"], "optional": ["行踪轨迹描述", "精准定位信息", "住宿信息"], "generator": get_master_data_10_location_info},
    "11_banking": {"name": "银行业", "core": ["客户ID", "账户流水号", "交易类型", "金额", "交易时间"], "optional": ["风险评级", "反洗钱(AML)标记", "对方账户", "摘要"], "generator": get_master_data_11_banking},
    "12_securities": {"name": "证券业", "core": ["股票代码", "时间", "收盘价"], "optional": ["开盘价", "成交量(手)", "投资者ID", "委托类型", "上市公司财报"], "generator": get_master_data_12_securities},
    "13_insurance": {"name": "保险业", "core": ["保单号", "投保人", "被保人", "险种"], "optional": ["保费(元)", "保险金额(元)", "理赔状态", "健康告知"], "generator": get_master_data_13_insurance},
    "14_fintech": {"name": "金融科技", "core": ["支付流水号", "用户ID", "金额"], "optional": ["商户名称", "支付方式", "状态", "时间", "P2P借贷记录"], "generator": get_master_data_14_fintech},
    "15_trust_leasing": {"name": "信托与租赁", "core": ["合同编号", "产品名称", "合同金额"], "optional": ["受益人", "租赁物信息", "起租日"], "generator": get_master_data_15_trust_leasing},
    "16_vc_pe": {"name": "风险投资与私募股权", "core": ["项目公司", "融资轮次", "投资金额(万美元)"], "optional": ["投后估值(万美元)", "投资日期", "所属行业", "尽职调查数据"], "generator": get_master_data_16_vc_pe},
    "17_public_security_justice": {"name": "公安司法", "core": ["案件编号", "案件类型", "当事人"], "optional": ["报案时间", "处理状态", "人口户籍", "车辆管理", "出入境记录"], "generator": get_master_data_17_public_security_justice},
    "18_market_regulation": {"name": "市场监管", "core": ["统一社会信用代码", "企业名称"], "optional": ["注册资本(万元)", "成立日期", "经营范围", "行政处罚记录", "知识产权"], "generator": get_master_data_18_market_regulation},
    "19_taxation_finance": {"name": "税务财政", "core": ["纳税人识别号", "发票号码", "含税金额"], "optional": ["发票代码", "开票日期", "税率", "财政收支"], "generator": get_master_data_19_taxation_finance},
    "20_civil_social_security": {"name": "民政社保", "core": ["业务类型", "当事人", "发生日期"], "optional": ["登记证号", "金额(元)", "医保缴纳记录"], "generator": get_master_data_20_civil_social_security},
    "21_public_health": {"name": "卫生健康", "core": ["上报卡号", "传染病名称", "发病日期"], "optional": ["上报单位", "疫苗接种记录", "医保基金运行数据"], "generator": get_master_data_21_public_health},
    "22_education_research": {"name": "教育科研", "core": ["学号", "姓名", "课程名称", "成绩"], "optional": ["科研项目名称", "项目经费(万元)", "学术论文"], "generator": get_master_data_22_education_research},
    "23_natural_resources_env": {"name": "自然资源与环保", "core": ["监测点ID", "时间"], "optional": ["PM2.5", "噪音(dB)", "水质PH值", "天气", "污染源排放"], "generator": get_master_data_23_natural_resources_env},
    "24_urban_management": {"name": "城市管理", "core": ["设施ID", "设施类型", "状态"], "optional": ["上报时间", "位置", "人流密度监测"], "generator": get_master_data_24_urban_management},
    "25_emergency_management": {"name": "应急管理", "core": ["事件编号", "事件类型", "发生时间"], "optional": ["报告单位", "应急物资储备", "灾害评估"], "generator": get_master_data_25_emergency_management},
    "26_national_statistics": {"name": "国家统计", "core": ["统计周期", "指标名称", "数值"], "optional": ["单位", "人口普查数据"], "generator": get_master_data_26_national_statistics},
    "27_electronics_semiconductor": {"name": "电子与半导体", "core": ["批次号", "产品型号"], "optional": ["晶圆制造良率(%)", "封装测试数据", "SMT产线数据", "电子元器件BOM表"], "generator": get_master_data_27_electronics_semiconductor},
    "28_heavy_industry_equipment": {"name": "重工与装备制造", "core": ["设备ID", "时间戳"], "optional": ["温度(C)", "压力(Pa)", "转速(rpm)", "设备健康监测(PHM)", "供应链订单"], "generator": get_master_data_28_heavy_industry_equipment},
    "29_chemical_new_materials": {"name": "化工与新材料", "core": ["反应釜编号", "生产批号"], "optional": ["生产配方ID", "温度(℃)", "压力(MPa)", "危化品仓储"], "generator": get_master_data_29_chemical_new_materials},
    "30_raw_materials_mining": {"name": "原材料与采矿", "core": ["矿区编号", "矿石品位(%)"], "optional": ["勘探数据", "设备运行日志", "安全监控", "大宗商品价格"], "generator": get_master_data_30_raw_materials_mining},
    "31_vehicle_randd_manufacturing": {"name": "整车研发与制造", "core": ["车辆识别代号(VIN)", "下线时间"], "optional": ["零部件清单", "生产线节拍(秒)", "整车质检(VQ)结果", "碰撞仿真数据"], "generator": get_master_data_31_vehicle_randd_manufacturing},
    "32_sales_distribution": {"name": "销售与分销", "core": ["经销商代码", "车型", "汽车销量"], "optional": ["销售日期", "消费者画像", "经销商库存"], "generator": get_master_data_32_sales_distribution},
    "33_after_sales_service": {"name": "汽车售后市场", "core": ["工单号", "车辆识别代号(VIN)", "维保项目"], "optional": ["零配件更换数据", "索赔数据", "客户满意度调查"], "generator": get_master_data_33_after_sales_service},
    "34_connected_vehicles": {"name": "车联网与智能驾驶", "core": ["车辆识别代号(VIN)", "时间戳", "经度", "纬度"], "optional": ["速度(km/h)", "驾驶行为数据", "车载传感器(Lidar)数据"], "generator": get_master_data_34_connected_vehicles},
    "35_passenger_transport": {"name": "客运服务", "core": ["票号", "班次", "始发站", "终点站"], "optional": ["出发时间", "旅客姓名", "正点率"], "generator": get_master_data_35_passenger_transport},
    "36_freight_logistics": {"name": "货运与物流", "core": ["运单号", "货物追踪"], "optional": ["发件人", "收件人", "车辆载货率(%)", "冷链温度监控(℃)"], "generator": get_master_data_36_freight_logistics},
    "37_warehousing": {"name": "仓储服务", "core": ["SKU", "操作类型", "数量"], "optional": ["商品名称", "库位管理", "WMS系统日志"], "generator": get_master_data_37_warehousing},
    "38_mobility_services": {"name": "出行服务", "core": ["订单号", "服务类型", "用户ID"], "optional": ["开始时间", "行程费用(元)", "行程时长(分钟)"], "generator": get_master_data_38_mobility_services},
    "39_electricity_power": {"name": "电力行业", "core": ["智能电表号(AMI)", "时间点", "用电量(kWh)"], "optional": ["电网负荷(MW)", "发电厂出力数据(MW)", "输配电线路状态"], "generator": get_master_data_39_electricity_power},
    "40_oil_gas": {"name": "石油天然气", "core": ["油井ID", "管道压力(MPa)", "管道流量(m³/h)"], "optional": ["加油站ID", "油品", "销量(升)"], "generator": get_master_data_40_oil_gas},
    "41_water_utilities": {"name": "水务行业", "core": ["智能水表号", "读数(m³)"], "optional": ["时间", "供水管网漏损监测", "污水处理水质(COD)"], "generator": get_master_data_41_water_utilities},
    "42_renewable_energy": {"name": "新能源", "core": ["电场ID", "时间戳", "发电功率(MW)"], "optional": ["天气预测", "储能设备充放电数据(MWh)", "碳交易数据(吨)"], "generator": get_master_data_42_renewable_energy},
    "43_ecommerce": {"name": "线上电商", "core": ["用户ID", "用户行为日志"], "optional": ["商品ID", "订单交易", "访问时间", "用户评价", "购物车数据"], "generator": get_master_data_43_ecommerce},
    "44_offline_retail": {"name": "线下商超", "core": ["POS机销售流水", "门店ID", "商品条码"], "optional": ["数量", "会员消费记录", "客流统计"], "generator": get_master_data_44_offline_retail},
    "45_cpg": {"name": "快速消费品", "core": ["产品名称", "渠道分销数据"], "optional": ["市场份额(%)", "品牌推广活动效果", "消费者调研问卷ID"], "generator": get_master_data_45_cpg},
    "46_medical_institutions": {"name": "医疗机构", "core": ["电子病历号(EMR)", "患者姓名", "诊断"], "optional": ["检验(LIS)结果", "医学影像(CT)号", "住院记录(HIS)", "处方数据"], "generator": get_master_data_46_medical_institutions},
    "47_life_sciences_pharma": {"name": "生命科学与制药", "core": ["临床试验编号", "药物研发数据"], "optional": ["基因测序数据ID", "药品流通数据", "不良反应报告ID"], "generator": get_master_data_47_life_sciences_pharma},
    "48_medical_devices": {"name": "医疗器械", "core": ["设备序列号", "设备类型"], "optional": ["设备使用日志", "性能参数", "植入式设备监测数据", "销售与维护记录"], "generator": get_master_data_48_medical_devices},
    "49_health_management": {"name": "健康管理", "core": ["用户ID", "可穿戴设备", "体征数据"], "optional": ["体检报告", "营养膳食记录", "心理咨询记录"], "generator": get_master_data_49_health_management},
    "50_real_estate": {"name": "地产开发与销售", "core": ["楼盘名称", "房产交易价格(万元)"], "optional": ["户型图", "购房者数据", "中介带看记录", "地块信息"], "generator": get_master_data_50_real_estate},
    "51_construction_engineering": {"name": "建筑工程", "core": ["项目编号", "工程项目进度(%)"], "optional": ["建筑信息模型(BIM)数据ID", "建材采购与消耗", "施工安全日志"], "generator": get_master_data_51_construction_engineering},
    "52_property_management": {"name": "物业管理", "core": ["住户信息", "物业费收缴记录"], "optional": ["门禁数据", "监控数据", "公共设施维修保养记录"], "generator": get_master_data_52_property_management},
    "53_news_publishing": {"name": "新闻出版", "core": ["文章ID", "文章点击率(%)"], "optional": ["读者画像", "订阅数据", "舆情监测数据"], "generator": get_master_data_53_news_publishing},
    "54_media_streaming": {"name": "广播影视与流媒体", "core": ["用户ID", "影片名称"], "optional": ["收视率(%)", "票房数据(万元)", "流媒体用户播放行为", "付费会员数据"], "generator": get_master_data_54_media_streaming},
    "55_gaming": {"name": "游戏产业", "core": ["玩家ID", "登录信息"], "optional": ["游戏内行为", "虚拟道具交易", "玩家社交关系"], "generator": get_master_data_55_gaming},
    "56_sports": {"name": "体育产业", "core": ["运动员ID", "赛场表现数据"], "optional": ["生理数据", "赛事票务", "体育用品销售(元)", "博彩赔率数据"], "generator": get_master_data_56_sports},
    "57_hotel_accommodation": {"name": "酒店住宿", "core": ["订单号", "平均房价(ADR)"], "optional": ["预订渠道数据", "入住率(%)", "客户评价", "会员积分"], "generator": get_master_data_57_hotel_accommodation},
    "58_catering": {"name": "餐饮行业", "core": ["订单号", "菜品销量"], "optional": ["外卖订单", "顾客翻台率", "食材采购", "库存"], "generator": get_master_data_58_catering},
    "59_tourism": {"name": "旅游服务", "core": ["OTA订单号", "线路产品数据"], "optional": ["景点客流量", "游客来源地", "游客目的地", "消费金额(元)"], "generator": get_master_data_59_tourism},
    "60_farming": {"name": "种植业", "core": ["地块编号", "作物长势监测"], "optional": ["土壤墒情(%)", "气象数据", "无人机遥感影像ID", "农产品价格(元/kg)"], "generator": get_master_data_60_farming},
    "61_animal_husbandry": {"name": "畜牧业", "core": ["牲畜ID", "健康档案", "产出量(kg)"], "optional": ["牲畜谱系", "智能项圈活动数据", "饲料消耗(kg)"], "generator": get_master_data_61_animal_husbandry},
    "62_fishery_aquaculture": {"name": "渔业水产养殖", "core": ["渔船捕捞日志ID", "水产养殖区水质监测(溶氧mg/L)"], "optional": ["鱼群声呐探测", "饲料投喂数据(kg)"], "generator": get_master_data_62_fishery_aquaculture},
    "63_legal_services": {"name": "法律服务", "core": ["案件卷宗号", "客户名称"], "optional": ["服务类型", "工时记录(小时)", "法律文书库"], "generator": get_master_data_63_legal_services},
    "64_consulting_auditing": {"name": "咨询与审计", "core": ["项目编号", "客户行业"], "optional": ["市场研究报告ID", "企业财务审计底稿", "咨询项目交付成果"], "generator": get_master_data_64_consulting_auditing},
    "65_human_resources": {"name": "人力资源", "core": ["候选人ID", "应聘职位"], "optional": ["招聘渠道效能分析", "候选人简历库", "薪酬调查报告", "员工满意度调研"], "generator": get_master_data_65_human_resources}
}

# --- 核心文件生成逻辑 ---
def select_dynamic_headers(core_fields, optional_fields):
    if not optional_fields: num_to_pick = 0
    else: num_to_pick = random.randint(1, len(optional_fields))
    picked_optionals = random.sample(optional_fields, num_to_pick)
    final_headers = core_fields + picked_optionals
    random.shuffle(final_headers)
    return final_headers

def create_csv_files_for_category(category_key, schema):
    category_name = schema["name"]
    category_dir = os.path.join(BASE_OUTPUT_DIR, f"{category_key}_{category_name}")
    os.makedirs(category_dir, exist_ok=True)
    for i in range(1, FILES_PER_CATEGORY + 1):
        headers_for_this_file = select_dynamic_headers(schema["core"], schema["optional"])
        file_path = os.path.join(category_dir, f"{category_name}_{i}.csv")
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers_for_this_file)
                writer.writeheader()
                num_rows = random.randint(MIN_ROWS_PER_FILE, MAX_ROWS_PER_FILE)
                for _ in range(num_rows):
                    full_data_row = schema["generator"]()
                    row_to_write = {header: full_data_row.get(header) for header in headers_for_this_file}
                    writer.writerow(row_to_write)
            print(f"  -> 已生成文件: {os.path.basename(file_path)} (含 {len(headers_for_this_file)} 列)")
        except IOError as e: print(f"错误: 无法写入文件 {file_path}。原因: {e}")
        except Exception as e: print(f"在生成 {file_path} 时发生未知错误: {e}")

def main():
    start_time = datetime.now()
    print(f"--- 开始生成模拟数据 (最终完整版) [{start_time.strftime('%Y-%m-%d %H:%M:%S')}] ---")
    print(f"将在 '{BASE_OUTPUT_DIR}' 目录下创建数据...")
    print(f"总计类别数: {len(CATEGORY_SCHEMAS)}")
    print(f"每个类别文件数: {FILES_PER_CATEGORY}")
    print("-" * 60)
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    total_files = 0
    for index, (key, schema) in enumerate(CATEGORY_SCHEMAS.items()):
        print(f"\n({index + 1}/{len(CATEGORY_SCHEMAS)}) 正在处理类别: {schema['name']}")
        try:
            create_csv_files_for_category(key, schema)
            total_files += FILES_PER_CATEGORY
        except Exception as e: print(f"!! 在处理类别 '{schema['name']}' 时发生严重错误: {e}")
    end_time = datetime.now()
    duration = end_time - start_time
    print("-" * 60)
    print("--- 所有数据生成任务已完成！ ---")
    print(f"总计生成文件数: {total_files}")
    print(f"任务耗时: {duration}")
    print(f"数据已保存在 '{os.path.abspath(BASE_OUTPUT_DIR)}' 目录中。")

if __name__ == "__main__":
    main()