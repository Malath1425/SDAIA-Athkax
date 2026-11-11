import pandas as pd
from scipy.stats import binomtest

def check_data_quality_and_srm():
    try:
         #df = pd.read_csv('data/dataset.csv')
         # قراءة ملف البيانات من المجلد الرئيسي المشترك
         df = pd.read_csv('../data/dataset.csv')
    except FileNotFoundError:
        print("عذراً، لم يتم العثور على ملف البيانات. تأكد من تشغيل كود اليوم الأول أولاً.")
        return
    
    print("--- 1. فحص جودة البيانات ---")
    print("إجمالي عدد الصفوف:", len(df))
    print("القيم المفقودة (Nulls):\n", df.isnull().sum())
    print("القيم المتكررة (Duplicates):", df.duplicated().sum())
    print("\nتوزيع المجموعات:\n", df['group'].value_counts())
    
    print("\n--- 2. اختبار ثبات التوزيع (SRM Check) ---")
    counts = df['group'].value_counts()
    count_a = counts.get('A', 0)
    count_b = counts.get('B', 0)
    total = count_a + count_b
    
    res = binomtest(count_a, total, p=0.5)
    p_value = res.pvalue
    
    print(f"مجموعة A: {count_a}, مجموعة B: {count_b}")
    print(f"P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("⚠️ تنبيه: يوجد اختلاف كبير (SRM Detected).")
    else:
        print("✅ ممتاز: لا يوجد اختلاف كبير (No SRM).")

if __name__ == "__main__":
    check_data_quality_and_srm()