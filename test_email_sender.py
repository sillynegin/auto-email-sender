import pytest

import email_sender
from email_sender import is_valid_email, build_message, load_config


# ---------- email validation ----------

@pytest.mark.parametrize("address", [
    "user@example.com",
    "first.last@example.co.uk",
    "user+tag@example.com",
])
def test_valid_emails(address):
    assert is_valid_email(address)


@pytest.mark.parametrize("address", [
    "user@",
    "not-an-email",
    "@example.com",
    "user@example",
    "",
])
def test_invalid_emails(address):
    assert not is_valid_email(address)


# ---------- message building ----------

def test_build_message_basic():
    msg = build_message("a@x.com", "b@x.com", "Hi", "Hello")
    assert msg["From"] == "a@x.com"
    assert msg["To"] == "b@x.com"
    assert msg["Subject"] == "Hi"
    assert msg["Reply-To"] is None


def test_build_message_reply_to():
    msg = build_message("a@x.com", "b@x.com", "Hi", "text", reply_to="u@x.com")
    assert msg["Reply-To"] == "u@x.com"


def test_build_message_persian_body():
    msg = build_message("a@x.com", "b@x.com", "Hi", "سلام")
    assert "سلام" in msg.get_content()


# ---------- config ----------

def test_load_config_missing_credentials(monkeypatch):
    # stop load_dotenv from reading the real .env file
    monkeypatch.setattr(email_sender, "load_dotenv", lambda: None)
    monkeypatch.delenv("SENDER_EMAIL", raising=False)
    monkeypatch.delenv("SENDER_PASSWORD", raising=False)
    with pytest.raises(SystemExit):
        load_config()


def test_load_config_ok(monkeypatch):
    monkeypatch.setattr(email_sender, "load_dotenv", lambda: None)
    monkeypatch.setenv("SENDER_EMAIL", "me@x.com")
    monkeypatch.setenv("SENDER_PASSWORD", "secret")
    config = load_config()
    assert config["sender"] == "me@x.com"
    assert config["port"] == 587


# ---------- sending (SMTP is mocked, no real email is sent) ----------

def test_send_email_uses_smtp(monkeypatch):
    calls = {}

    class FakeSMTP:
        def __init__(self, server, port, timeout=None):
            calls["server"] = server
            calls["port"] = port

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self, context=None):
            calls["tls"] = True

        def login(self, user, password):
            calls["login"] = (user, password)

        def send_message(self, msg):
            calls["sent_to"] = msg["To"]

    monkeypatch.setattr(email_sender.smtplib, "SMTP", FakeSMTP)

    config = {"server": "smtp.test.com", "port": 587,
              "sender": "me@x.com", "password": "secret"}
    msg = build_message("me@x.com", "you@x.com", "Hi", "text")
    email_sender.send_email(config, msg)

    assert calls["tls"] is True
    assert calls["login"] == ("me@x.com", "secret")
    assert calls["sent_to"] == "you@x.com"
