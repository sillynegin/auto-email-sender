"""Simple automatic email sender using SMTP.

The email is sent from the account configured in .env.
The user's own email is added as Reply-To, so replies go back to the user.
"""
import argparse
import logging
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def is_valid_email(address: str) -> bool:
    return bool(EMAIL_PATTERN.match(address))


def load_config() -> dict:
    load_dotenv()
    config = {
        "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "sender": os.getenv("SENDER_EMAIL"),
        "password": os.getenv("SENDER_PASSWORD"),
    }
    if not config["sender"] or not config["password"]:
        sys.exit("SENDER_EMAIL and SENDER_PASSWORD must be set in the .env file.")
    return config


def build_message(sender, receiver, subject, body, reply_to=None) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body, charset="utf-8")
    return msg


def send_email(config: dict, msg: EmailMessage) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP(config["server"], config["port"], timeout=30) as server:
        server.starttls(context=context)
        server.login(config["sender"], config["password"])
        server.send_message(msg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an automatic email.")
    parser.add_argument("--from-user", help="the user's own email (used as Reply-To)")
    parser.add_argument("--to", help="recipient email")
    parser.add_argument("--subject", help="email subject")
    parser.add_argument("--body", help="email body text")
    parser.add_argument("--body-file", help="read body from a text file")
    return parser.parse_args()


def ask_email(prompt: str, preset: str = None) -> str:
    address = preset or input(prompt).strip()
    if not is_valid_email(address):
        sys.exit(f"Invalid email: {address}")
    return address


def main() -> None:
    args = parse_args()
    config = load_config()

    user_email = ask_email("Your email: ", args.from_user)
    receiver = ask_email("Recipient email: ", args.to)
    subject = args.subject or input("Subject: ").strip()

    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    else:
        body = args.body or input("Message: ").strip()

    body = f"Sent on behalf of: {user_email}\n\n{body}"
    msg = build_message(config["sender"], receiver, subject, body, reply_to=user_email)

    try:
        send_email(config, msg)
        log.info("Email sent to %s.", receiver)
    except smtplib.SMTPAuthenticationError:
        log.error("Authentication failed. Check your email or App Password.")
    except (smtplib.SMTPException, OSError) as e:
        log.error("Sending failed: %s", e)


if __name__ == "__main__":
    main()