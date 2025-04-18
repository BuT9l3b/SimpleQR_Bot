import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineQuery, InlineQueryResultCachedPhoto, BufferedInputFile, InlineQueryResultArticle, InputTextMessageContent
from config.settings import BOT_TOKEN, BOT_NAME, STORAGE_CHANNEL
from app.qr.generator import QRCodeGenerator
from app.qr.decoder import QRCodeDecoder
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def fetch_qr(bot: Bot, qr_image_bytes: bytes, storage_chat_id: str) -> str:
    """Upload QR code to a storage channel and return its file_id."""
    qr_input_file = BufferedInputFile(qr_image_bytes, filename="qr_code.png")
    sent_message = await bot.send_photo(
        chat_id=storage_chat_id,  # ID канала или чата для хранения
        photo=qr_input_file
    )
    return sent_message.photo[-1].file_id


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    await message.answer(
        "👋 Welcome to QR Code Bot!\n\n"
        "I can help you with:\n"
        "🔹 Generating QR codes from text or links\n"
        "🔹 Decoding QR codes from images\n\n"
        "Just send me any text or link to generate a QR code, "
        "or send me an image with a QR code to decode it!"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle /help command"""
    help_text = (
        "🤖 QR Code Bot Help\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "Features:\n"
        "1. Generate QR code:\n"
        "   - Send any text or link\n"
        "   - Bot will generate a QR code\n\n"
        "2. Decode QR code:\n"
        "   - Send an image with QR code\n"
        "   - Bot will decode and show content\n\n"
        "3. Inline mode:\n"
        "   - Type @bot_username in any chat\n"
        "   - Enter text to generate QR code"
    )
    await message.answer(help_text)


@dp.message(F.text)
async def handle_message(message: types.Message):
    """Handle text messages for QR code generation"""
    try:
        # Generate QR code
        qr_generator = QRCodeGenerator()
        qr_image = await qr_generator.generate_qr(message.text)
        
        # Convert BytesIO to InputFile
        qr_input_file = BufferedInputFile(qr_image.getvalue(), filename="qr_code.png")
        
        # Send QR code
        await message.answer_photo(
            photo=qr_input_file,
            caption=f"QR Code for: {message.text}"
        )
        
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        await message.answer("❌ Sorry, I couldn't generate the QR code. Please try again.")


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    """Handle photo messages for QR code decoding"""
    try:
        # Get the largest photo
        photo = message.photo[-1]
        
        # Download photo
        file = await bot.get_file(photo.file_id)
        photo_data = await bot.download_file(file.file_path)
        
        # Decode QR code
        qr_decoder = QRCodeDecoder()
        success, result = await qr_decoder.decode_qr(photo_data)
        
        if success:
            await message.answer(f"📝 Decoded QR code content:\n\n{result}")
        else:
            await message.answer("❌ No QR code found in the image or unable to decode it.")
            
    except Exception as e:
        logger.error(f"Error decoding QR code: {e}")
        await message.answer("❌ Sorry, I couldn't decode the QR code. Please try again.")


@dp.inline_query()
async def handle_inline_query(inline_query: InlineQuery):
    """Handle inline queries for QR code generation"""
    if not inline_query.query:
        result = InlineQueryResultArticle(
            id="1",
            title="Generate QR Code",
            input_message_content=InputTextMessageContent(
                message_text="🔹 Enter text or link to generate a QR code!\n"
                f"🔹 Example: {BOT_NAME} Hello, world!",
                parse_mode="HTML"
            ),
            description="Type any text to create a QR code",
            thumb_url="https://www.svgrepo.com/show/334191/qr-scan.svg"
        )
        await inline_query.answer([result])
        return
    
    try:
        qr_generator = QRCodeGenerator()
        qr_image = await qr_generator.generate_qr(inline_query.query)
        
        # Upload QR code to a storage channel and get file_id
        file_id = await fetch_qr(
            bot,
            qr_image.getvalue(),
            storage_chat_id=STORAGE_CHANNEL  # Replace with actual ID
        )
        
        # Create inline result for inline mode
        result = InlineQueryResultCachedPhoto(
            id="1",
            photo_file_id=file_id,
            title="QR Code",
            description=f"QR Code for: {inline_query.query}"
        )
        
        await inline_query.answer([result], cache_time=65536)
        
    except Exception as e:
        logger.error(f"Error handling inline query: {e}")
        await inline_query.answer([])


async def start_bot():
    """Start the bot"""
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()