# Discord Account Cleaner

أداة تنظيف شاملة لحساب Discord (حذف الأصدقاء، الرسائل، التطبيقات المصرحة، الخوادم).
Discord comprehensive account cleaner (friends, DMs, authorized apps, servers).

---

## Warning / تنبيه هام

**يمنع منعاً باتاً إزالة حقوق المطور.**
**Removal of developer rights/credits is strictly prohibited.**

- **Programmer:** `@umw_m`

---

## Arabic Guide / الدليل العربي

### 1. المتطلبات
- Python 3.8+
- تثبيت الحزم المطلوبة:
`
pip install -r requirements.txt
`

### 2. طريقة التشغيل
1. تثبيت الحزم المطلوبة:
   `
   pip install -r requirements.txt
   `
2. تشغيل الأداة:
   `
   python main.py
   `
   - سيطلب منك `Enter Your Token :` ادخل توكن الديسكورد
   - اختر العملية:
     - `1- Friend` حذف الأصدقاء
     - `2- DM` حذف الرسائل الخاصة
     - `3- Authorized Apps` حذف التطبيقات المصرحة
     - `4- Close DMs` إغلاق الخاص
     - `5- Leave Servers` مغادرة السيرفرات
     - `6- Delete Owner Servers` حذف سيرفراتك
     - `7- Nuke All` تنظيف شامل

### 3. المخرجات
- `Deleted : username` عند النجاح
- `Failed : username (code)` عند الفشل
- `Rate limit` يتم التعامل معه تلقائيا

---

## English Guide / الدليل الإنجليزي

### 1. Requirements
- Python 3.8+
- Install dependencies:
`
pip install -r requirements.txt
`

### 2. Installation & Execution
1. Install requirements:
   `
   pip install -r requirements.txt
   `
2. Run the checker:
   `
   python main.py
   `
   - Enter `Token`
   - Choose operation 1-7

### 3. Output
- `Deleted` on success
- `Failed` on error
- Automatic rate limit handling

---

## Rights & Credits / الحقوق

- **Programmer / المطور:** `@umw_m`
- **Tool Dev:** `Legend ~ .gg/cupspy`
- **تنبيه:** يمنع منعاً باتاً إزالة حقوق المطور أو تعديلها.
- **Notice:** Removal or modification of developer credits is strictly prohibited.