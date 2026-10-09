import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

# تم وضع توكن بوتك الخاص هنا
import os
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. أمر البداية لتوجيه المستخدم
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "مرحباً بك في بوت تحويل النقاط إلى دولارات والنقاط!\n\n"
        "الرجاء إرسال معرف بينانس الخاص بك (Binance UID) أولاً، ثم اتبع التعليمات."
    )

# 2. استقبال معرف بينانس وتحويله لخطوة شراء النجوم
@dp.message(F.text.regexp(r'^\d+$'))
async def save_binance_uid(message: Message):
    user_uid = message.text
    
    prices = [LabeledPrice(label="100 Telegram Stars", amount=100)]
    
    await message.answer_invoice(
        title="شراء 100 نجمة",
        description="شراء 100 نجمة تليجرام واستلام مكافأتك",
        payload="stars_100_payload",
        currency="XTR",
        prices=prices,
    )

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment(message: Message):
    await message.answer(
        "تم استلام النجوم بنجاح! شكراً لك. 🌟\n"
        "جاري مراجعة طلبك وتحويل المكافأة إلى حساب بينانس الخاص بك."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
