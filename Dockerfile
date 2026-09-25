FROM python:3.10-slim

# সার্ভারে Java (JRE) এবং প্রয়োজনীয় টুলস ইনস্টল করা
RUN apt-get update && \
    apt-get install -y default-jre wget && \
    apt-get clean

# ওয়ার্কিং ফোল্ডার সেটআপ
WORKDIR /app

# পাইথনের প্রয়োজনীয় লাইব্রেরি ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# বটের সব ফাইল সার্ভারে কপি করা
COPY . .

# বট রান করার মূল কমান্ড
CMD ["python", "bot.py"]
