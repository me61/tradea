#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询安孚科技(603031)2025年营业收入数据
使用AKShare免费开源金融数据接口
"""

import akshare as ak
import pandas as pd


def query_anfu_revenue_2025():
    """查询安孚科技2025年营业收入"""
    
    # 安孚科技股票代码
    stock_code = "603031"
    
    print("=" * 60)
    print(f"查询 {stock_code} 安孚科技 2025年营业收入数据")
    print("=" * 60)
    
    # 获取公司基本信息
    try:
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        print("\n【公司基本信息】")
        for _, row in stock_info.iterrows():
            print(f"  {row['item']}: {row['value']}")
    except Exception as e:
        print(f"获取公司基本信息失败：{e}")
    
    # 获取财务摘要数据（包含营业收入）
    try:
        financial_data = ak.stock_financial_abstract_ths(symbol=stock_code)
        
        print("\n【财务摘要数据 - 营业收入】")
        print("-" * 60)
        
        # 筛选2025年的数据
        financial_data['报告期'] = pd.to_datetime(financial_data['报告期'])
        data_2025 = financial_data[financial_data['报告期'].dt.year == 2025].copy()
        
        if not data_2025.empty:
            print(f"\n2025年各季度营业收入:")
            for _, row in data_2025.iterrows():
                report_date = row['报告期'].strftime('%Y-%m-%d')
                revenue = row['营业总收入']
                growth = row['营业总收入同比增长率']
                print(f"  {report_date}: {revenue} (同比增长: {growth})")
            
            # 获取全年数据（通常是12月31日的报告期）
            full_year_data = data_2025[data_2025['报告期'].dt.month == 12]
            if not full_year_data.empty:
                annual_revenue = full_year_data.iloc[0]['营业总收入']
                annual_growth = full_year_data.iloc[0]['营业总收入同比增长率']
                
                print("\n" + "=" * 60)
                print(f"【2025年全年营业收入】: {annual_revenue}")
                print(f"【同比增长率】: {annual_growth}")
                print("=" * 60)
                return annual_revenue
        else:
            print("未找到2025年数据")
            return None
            
    except Exception as e:
        print(f"获取财务数据失败：{e}")
        return None


if __name__ == "__main__":
    revenue = query_anfu_revenue_2025()
    
    if revenue:
        print(f"\n✅ 查询成功！安孚科技2025年营业收入为：{revenue}")
    else:
        print("\n❌ 查询失败或无数据")
