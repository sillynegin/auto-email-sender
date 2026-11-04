<div align="center">

# 💌 Auto Email Sender

**A cute little Python tool that sends emails automatically** ✨

![Python](https://img.shields.io/badge/Python-3.10+-ff69b4?style=for-the-badge&logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-14%20passed-ffb6c1?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-dda0dd?style=for-the-badge)

🌸 [English](#-about) · [فارسی](#-توضیحات-فارسی) 🌸

</div>

---

## 🎀 About

Auto Email Sender sends an email to any recipient using SMTP.
The email goes out from the account in your `.env` file, and the user's own email is added as **Reply-To** 💕 so replies land right back in their inbox.

## ✨ Features

| | Feature |
|---|---|
| 💌 | Sends emails via SMTP (Gmail, Outlook, Yahoo...) |
| 💬 | Reply-To support, so replies go to the user |
| 🔐 | Credentials stay safe in `.env`, never in the code |
| 🌍 | Supports Persian / UTF-8 text |
| 🧪 | Unit tests with `pytest` (no real emails sent) |

## 🌷 Setup

```bash
git clone https://github.com/sillynegin/auto-email-sender.git
cd auto-email-sender
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file (copy `.env.example`) and fill it in:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

> 💡 **Gmail tip:** enable 2-step verification and create an **App Password**. Your normal password won't work.

## 🚀 Usage

```bash
python email_sender.py
```

Or with arguments:

```bash
python email_sender.py --from-user me@example.com --to friend@example.com --subject "Hello" --body "Hi there!"
```

## 🧪 Tests

```bash
python -m pytest
```

## 📄 License

MIT 💖

---

<div dir="rtl">

## 🌸 توضیحات (فارسی)

این پروژه یک ابزار کوچولو و ساده با پایتون است که با پروتکل SMTP برای یک گیرنده ایمیل می‌فرستد 💌

### ✨ ویژگی‌ها

- 💌 ارسال ایمیل از حساب تنظیم‌شده در فایل `.env`
- 💬 ثبت ایمیل کاربر به‌عنوان `Reply-To` تا جواب‌ها به خودش برسد
- 🔐 رمز و ایمیل فرستنده داخل کد نیست و امن نگه‌داری می‌شود
- 🌍 پشتیبانی از متن فارسی
- 🧪 تست‌های خودکار با `pytest`

### 🌷 نصب و اجرا

1. ساخت محیط مجازی: `python -m venv venv`
2. فعال‌سازی (ویندوز): `venv\Scripts\activate`
3. نصب پکیج‌ها: `pip install -r requirements.txt`
4. ساخت فایل `.env` از روی `.env.example` و پر کردن اطلاعات
5. اجرا: `python email_sender.py`

</div>

<div align="center">

Made with 💖 by [sillynegin](https://github.com/sillynegin)

</div>