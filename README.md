# DeepFocus

نظام لإدارة العمل العميق والإنتاجية: ينظّم المستخدم مهامه (Deep Work أو Shallow Work)، ويسجّل جلسات تركيز بمؤقت، ويرى ملخصاً لأرقامه في لوحة التحكم.

## المزايا

- تسجيل حساب ودخول وخروج، وصفحة Profile (صورة ونبذة وتعديل الاسم والإيميل).
- إضافة المهام وعرضها وتعديلها وحذفها، مع نوع وأولوية وحالة وصورة اختيارية.
- كل مستخدم يرى مهامه وجلساته فقط.
- بحث بعنوان المهمة، وفلاتر النوع والأولوية والحالة، وترقيم الصفحات.
- مؤقت جلسات تركيز يحفظ المدة المنجزة، وسجل للجلسات.
- لوحة تحكم: عدد المهام والمنجزة ونسبة الإنجاز ودقائق التركيز اليوم وآخر 7 أيام وآخر الجلسات.
- إيميل ترحيب عند التسجيل.

## المتطلبات

- Python 3.12
- Django 6.1.3 (و Pillow)

## خطوات التشغيل

    git clone https://github.com/hadi-al-sous-projects/habit-tracker.git
    cd deepfocus
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

## العنوان

http://127.0.0.1:8000

## ملاحظات

- إيميل الترحيب يظهر في الـ terminal أثناء التطوير وليس بريداً حقيقياً.
- الواجهة في هذه النسخة بسيطة بدون تنسيق، والتنسيق مؤجل لنسخة لاحقة.
- قاعدة البيانات SQLite ولا ترفع على GitHub.

## هيكل الملفات

    deepfocus/
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ├── deepfocus/      (الإعدادات والروابط الرئيسية)
    ├── accounts/       (المستخدمون والـ Profile)
    ├── tasks/          (المهام والجلسات ولوحة التحكم)
    └── templates/      (القوالب)
