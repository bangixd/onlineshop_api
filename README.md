# فروشگاه آنلاین - API Backend

این پروژه یک API ساده برای یک فروشگاه آنلاین است که با استفاده از جنگو (Django) و Django REST Framework طراحی شده است. این پروژه شامل سیستم مدیریت کاربران، سبد خرید، سفارشات و محصولات است.

# 🚀 ویژگی‌ها

مدیریت کاربران (ثبت‌نام، ورود با JWT، مشاهده پروفایل)

مدیریت محصولات (CRUD کامل)

مدیریت سبد خرید (افزودن و حذف محصولات)

مدیریت سفارشات (ثبت سفارش از روی سبد خرید)

به‌روزرسانی خودکار موجودی محصولات پس از ثبت سفارش

سیستم احراز هویت JWT

# ⚡ نصب و راه‌اندازی

پروژه را کلون کنید:

```
https://github.com/your-username/your-repo.git
```

وارد دایرکتوری پروژه شوید:

```
cd your-repo 
```

محیط مجازی پایتون ایجاد و فعال کنید:
```
python -m venv venv
source venv/bin/activate  # برای سیستم‌عامل‌های مبتنی بر لینوکس
venv\Scripts\activate  # برای ویندوز
```

وابستگی‌ها را نصب کنید:
```
pip install -r requirements.txt
```

مهاجرت‌های پایگاه داده را اجرا کنید:
```
python manage.py makemigrations
python manage.py migrate
```

ایجاد سوپریوزر (مدیر سیستم):
```
python manage.py createsuperuser
```

سرور توسعه را اجرا کنید:
```
python manage.py runserver
```

# 📌 API Endpointها

احراز هویت JWT:

POST ` /api/auth/login/ ` (ورود و دریافت توکن)

POST ` /api/auth/refresh/ ` (تازه‌سازی توکن)

کاربران:

GET/POST ` /api/users/ `

GET ` /api/users/me/ ` (نمایش پروفایل کاربر)

محصولات:

GET/POST ` /api/products/ `

GET/PUT/DELETE ` /api/products/{id}/ `

سبد خرید:

GET/POST ` /api/cart-items/ `

DELETE ` /api/cart-items/{id}/ `

سفارشات:

GET/POST ` /api/orders/ `

# 💡 نحوه عملکرد

کاربر می‌تواند محصولات را مشاهده کند.

با افزودن محصولات به سبد خرید، سفارش ایجاد می‌شود.

پس از ثبت سفارش:

موجودی محصولات به‌روز می‌شود.

سبد خرید کاربر خالی می‌شود.

# 📌 نویسنده

ابوالفضل سیاح

