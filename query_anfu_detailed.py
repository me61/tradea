# -*- coding: utf-8 -*-
"""
使用 AKShare 查询安孚科技 (603031) 2025年详细年报数据
数据来源：新浪财经（通过 AKShare 接口）
"""

import akshare as ak
import pandas as pd

def query_anfu_financials():
    """查询安孚科技财务报表数据"""
    stock_code = "603031"
    stock_name = "安孚科技"
    
    print(f"正在查询 {stock_name} ({stock_code}) 的财务数据...")
    print("=" * 80)
    
    # 1. 利润表
    print("\n【利润表】")
    df_income = ak.stock_financial_report_sina(stock=stock_code, symbol='利润表')
    
    # 筛选2025年数据
    df_2025_income = df_income[df_income['报告日'].astype(str).str.startswith('2025')]
    
    if not df_2025_income.empty:
        # 显示关键指标
        key_columns_income = ['报告日', '营业总收入', '营业收入', '营业总成本', '营业利润', 
                             '利润总额', '净利润', '归属于母公司所有者的净利润', '基本每股收益']
        
        # 只保留存在的列
        available_cols = [col for col in key_columns_income if col in df_2025_income.columns]
        display_df = df_2025_income[available_cols].copy()
        
        # 格式化数值列为亿元
        for col in display_df.columns:
            if col != '报告日' and display_df[col].dtype in ['float64', 'int64']:
                display_df[col] = display_df[col].apply(lambda x: f"{x/100000000:.2f}" if pd.notna(x) else "NaN")
        
        print(display_df.to_string(index=False))
    else:
        print("未找到2025年利润表数据")
    
    # 2. 资产负债表
    print("\n" + "=" * 80)
    print("\n【资产负债表】")
    df_balance = ak.stock_financial_report_sina(stock=stock_code, symbol='资产负债表')
    
    df_2025_balance = df_balance[df_balance['报告日'].astype(str).str.startswith('2025')]
    
    if not df_2025_balance.empty:
        key_columns_balance = ['报告日', '资产总计', '流动资产合计', '非流动资产合计',
                              '负债合计', '流动负债合计', '非流动负债合计',
                              '归属于母公司股东权益合计', '所有者权益(或股东权益)合计']
        
        available_cols = [col for col in key_columns_balance if col in df_2025_balance.columns]
        display_df_bs = df_2025_balance[available_cols].copy()
        
        for col in display_df_bs.columns:
            if col != '报告日' and display_df_bs[col].dtype in ['float64', 'int64']:
                display_df_bs[col] = display_df_bs[col].apply(lambda x: f"{x/100000000:.2f}" if pd.notna(x) else "NaN")
        
        print(display_df_bs.to_string(index=False))
    else:
        print("未找到2025年资产负债表数据")
    
    # 3. 现金流量表
    print("\n" + "=" * 80)
    print("\n【现金流量表】")
    df_cashflow = ak.stock_financial_report_sina(stock=stock_code, symbol='现金流量表')
    
    df_2025_cashflow = df_cashflow[df_cashflow['报告日'].astype(str).str.startswith('2025')]
    
    if not df_2025_cashflow.empty:
        key_columns_cf = ['报告日', '经营活动产生的现金流量净额', '投资活动产生的现金流量净额',
                         '筹资活动产生的现金流量净额', '现金及现金等价物净增加额',
                         '期末现金及现金等价物余额']
        
        available_cols = [col for col in key_columns_cf if col in df_2025_cashflow.columns]
        display_df_cf = df_2025_cashflow[available_cols].copy()
        
        for col in display_df_cf.columns:
            if col != '报告日' and display_df_cf[col].dtype in ['float64', 'int64']:
                display_df_cf[col] = display_df_cf[col].apply(lambda x: f"{x/100000000:.2f}" if pd.notna(x) else "NaN")
        
        print(display_df_cf.to_string(index=False))
    else:
        print("未找到2025年现金流量表数据")
    
    # 4. 汇总2025年全年数据
    print("\n" + "=" * 80)
    print("\n【2025年全年主要财务指标汇总】")
    
    # 获取2025年年报数据（报告日为20251231）
    annual_income = df_income[df_income['报告日'].astype(str).str.startswith('20251231')]
    annual_balance = df_balance[df_balance['报告日'].astype(str).str.startswith('20251231')]
    annual_cashflow = df_cashflow[df_cashflow['报告日'].astype(str).str.startswith('20251231')]
    
    if not annual_income.empty:
        row = annual_income.iloc[0]
        print(f"\n📊 营收与利润（单位：亿元）:")
        print(f"   • 营业总收入：{row.get('营业总收入', 0)/100000000:.2f}")
        print(f"   • 营业收入：{row.get('营业收入', 0)/100000000:.2f}")
        print(f"   • 营业总成本：{row.get('营业总成本', 0)/100000000:.2f}")
        print(f"   • 营业利润：{row.get('营业利润', 0)/100000000:.2f}")
        print(f"   • 利润总额：{row.get('利润总额', 0)/100000000:.2f}")
        print(f"   • 净利润：{row.get('净利润', 0)/100000000:.2f}")
        print(f"   • 归母净利润：{row.get('归属于母公司所有者的净利润', 0)/100000000:.2f}")
        print(f"   • 基本每股收益：{row.get('基本每股收益', 0):.2f} 元")
    
    if not annual_balance.empty:
        row = annual_balance.iloc[0]
        print(f"\n💰 资产负债（单位：亿元）:")
        print(f"   • 资产总计：{row.get('资产总计', 0)/100000000:.2f}")
        print(f"   • 负债合计：{row.get('负债合计', 0)/100000000:.2f}")
        print(f"   • 所有者权益合计：{row.get('所有者权益(或股东权益)合计', 0)/100000000:.2f}")
        print(f"   • 归属于母公司股东权益：{row.get('归属于母公司股东权益合计', 0)/100000000:.2f}")
    
    if not annual_cashflow.empty:
        row = annual_cashflow.iloc[0]
        print(f"\n💵 现金流量（单位：亿元）:")
        print(f"   • 经营活动现金流净额：{row.get('经营活动产生的现金流量净额', 0)/100000000:.2f}")
        print(f"   • 投资活动现金流净额：{row.get('投资活动产生的现金流量净额', 0)/100000000:.2f}")
        print(f"   • 筹资活动现金流净额：{row.get('筹资活动产生的现金流量净额', 0)/100000000:.2f}")
        print(f"   • 期末现金及等价物余额：{row.get('期末现金及现金等价物余额', 0)/100000000:.2f}")
    
    print("\n" + "=" * 80)
    print(f"数据公告日期：{annual_income.iloc[0].get('公告日期', 'N/A') if not annual_income.empty else 'N/A'}")
    print("数据来源：AKShare - 新浪财经接口")
    print("=" * 80)

if __name__ == "__main__":
    query_anfu_financials()
