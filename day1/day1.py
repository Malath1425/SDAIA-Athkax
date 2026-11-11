import pandas as pd
import numpy as np
import os

def generate_data():
    # تثبيت العشوائية لضمان تكرار نفس النتائج بدقة
    np.random.seed(2026)
    n = 20000  # عدد المستخدمين في التجربة
    
    user_ids = [f"u_{i}" for i in range(n)]
    # توزيع المستخدمين عشوائياً بنسبة 50% لكل مجموعة (A: مجموعة الضبط، B: مجموعة التجربة)
    groups = np.random.choice(['A', 'B'], size=n, p=[0.5, 0.5])
    
    # توليد بيانات ما قبل التجربة (تستخدم لاحقاً لتقليل التباين باستخدام طريقة CUPED)
    pre_spend = np.random.exponential(scale=50, size=n)
    
    # توليد معدل التحويل (Conversion) مع أثر حقيقي للمجموعة B
    conversion = []
    for g in groups:
        if g == 'A':
            conv = np.random.binomial(1, p=0.10) # 10% معدل التحويل للضبط
        else:
            conv = np.random.binomial(1, p=0.12) # 12% معدل التحويل للتجربة (تحسن بنسبة 2%)
        conversion.append(conv)
        
    # إنشاء إطار البيانات (DataFrame)
    df = pd.DataFrame({
        'user_id': user_ids,
        'group': groups,
        'pre_experiment_spend': pre_spend,
        'converted': conversion
    })
    
    # إنشاء مجلد باسم data تلقائياً داخل بيئة الكولاب وحفظ الملف بداخله
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/dataset.csv', index=False)
    
    print("تم توليد بيانات التجربة بنجاح!")
    print(f"إجمالي عدد الصفوف والعملاء: {df.shape}")
    print("\nعينة مختارة من البيانات:")
    #display(df.head())
    print(df.head())

if __name__ == "__main__":
    generate_data()