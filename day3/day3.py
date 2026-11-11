import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.stats.proportion import proportions_ztest

def statistical_analysis_and_chart():
    try:
        # قراءة ملف البيانات من المجلد الرئيسي المشترك
        df = pd.read_csv('../data/dataset.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('data/dataset.csv')
        except FileNotFoundError:
            print("عذراً، لم يتم العثور على ملف البيانات. تأكد من وجوده في مجلد data.")
            return
    
    print("--- 1. تحليل معدل التحويل (Conversion Rate Analysis) ---")
    conversion_summary = df.groupby('group')['converted'].agg(['count', 'sum', 'mean']).rename(
        columns={'count': 'total_users', 'sum': 'conversions', 'mean': 'conversion_rate'}
    )
    print(conversion_summary)
    
    # استخراج البيانات لاختبار Z
    conversions = [conversion_summary.loc['B', 'conversions'], conversion_summary.loc['A', 'conversions']]
    nobs = [conversion_summary.loc['B', 'total_users'], conversion_summary.loc['A', 'total_users']]
    
    # إجراء اختبار Z لمقارنة نسب التحويل
    z_stat, p_val = proportions_ztest(conversions, nobs)
    
    rate_a = conversion_summary.loc['A', 'conversion_rate']
    rate_b = conversion_summary.loc['B', 'conversion_rate']
    uplift = (rate_b - rate_a) / rate_a * 100
    
    print(f"\nمعدل التحويل لمجموعة الضبط (A): {rate_a:.4f}")
    print(f"معدل التحويل لمجموعة التجربة (B): {rate_b:.4f}")
    print(f"نسبة التحسن (Uplift): {uplift:.2f}%")
    print(f"Z-statistic: {z_stat:.4f}")
    print(f"P-value: {p_val:.4f}")
    
    if p_val < 0.05:
        print("\n✅ النتيجة: الفروق ذات دلالة إحصائية (Statistically Significant)، الميزة حسنت معدل التحويل بوضوح!")
    else:
        print("\n❌ النتيجة: الفروق ليست ذات دلالة إحصائية كافية.")

    # --- 2. رسم وتصدير الرسم البياني الخاص بتحليل البيانات ---
    # إنشاء مجلد المخرجات تلقائياً
    os.makedirs('../outputs/charts', exist_ok=True)
    os.makedirs('outputs/charts', exist_ok=True)
    
    plt.figure(figsize=(7, 5))
    sns.barplot(x='group', y='converted', data=df, hue='group', palette='viridis', legend=False)
    plt.title('A/B Testing: Conversion Rate by Group')
    plt.ylabel('Conversion Rate')
    plt.xlabel('Group')
    
    # إظهار الرسمة فوراً أمامك في الكولاب
    plt.show()
    
    # حفظ الرسمة في المجلد المطلوب للمشروع
    chart_path = '../outputs/charts/conversion_comparison.png'
    plt.savefig(chart_path, bbox_inches='tight')
    plt.savefig('outputs/charts/conversion_comparison.png', bbox_inches='tight')
    print(f"📊 تم حفظ الرسم البياني بنجاح في المسار: {chart_path}")

if __name__ == "__main__":
    statistical_analysis_and_chart()
