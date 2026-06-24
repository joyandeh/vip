FROM python:3.12-slim

# تنظیمات محیطی پایتون
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعیین پوشه کاری درون کانتینر
WORKDIR /app

# نصب پیش‌نیازها
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام کدهای پروژه به درون کانتینر
COPY . /app/

# پورت پیش‌فرض جنگو
EXPOSE 8000

# دستور اجرای سرور
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]