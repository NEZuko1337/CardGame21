from tokens import token
from rules import(
    start_message,
    message1, 
    message2, 
    message3
)
from aiogram.exceptions import TelegramBadRequest
from  choose_img_to_card import img_for_card
from links_to_photos import link_to_all_cards 
from keyboards import choose_buttons, rmk, start_new_game
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import random


bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name} , это бот в котором ты сможешь поиграть в игру '21', напиши /startgame, если хочешь сыграть, а если хочешь узнать правила, напиши /help")


@dp.message(Command("help"))
async def how_to_play(message: Message):
    await message.answer("Хорошо, раз ты не знаешь правил, я тебе их расскажу")
    await message.answer(start_message)
    await message.answer_photo(link_to_all_cards)
    await message.answer(message1)
    await message.answer(message2)
    await message.answer(message3)


class Game(StatesGroup):
    zuko_sum_card = State()
    total_player = State()
    third_card = State()
    fourth_card = State()
    fifth_card = State()


@dp.message(Command("startgame"))
async def game(message: Message, state: FSMContext):
    await message.answer("Игра началась!")
    my_choice = ['Еще', 'Хватит']
    # Тут короче идет секция рандома моих карт, чуть доделать рандом сразу тут, без мозгоебли
    zuko_cards = []
    zuko_total = 0
    first_card, second_card = random.randint(2, 11), random.randint(2, 11)
    zuko_cards.append(first_card)
    zuko_cards.append(second_card)
    zuko_total = sum(zuko_cards)

    #Тут позорный выбор карт пользователся
    player_cards = []
    player_total = 0

    first_player_card, second_player_card = random.randint(2, 11), random.randint(2, 11)

    player_cards.append(first_player_card)
    player_cards.append(second_player_card)
    player_total = sum(player_cards)

    photo_to_first_player_card = img_for_card(first_player_card)
    photo_to_second_player_card = img_for_card(second_player_card)

    await message.answer("Вот карты, которые тебе выпали")
    try:
        await message.answer_photo(photo_to_first_player_card)
        await message.answer_photo(photo_to_second_player_card)
    except TelegramBadRequest:
        await message.answer("Начни игру заново пожалуйста, возникла небольшая ошибка", reply_markup=start_new_game)
    else:
        await message.answer(f"Сумма твоих карт: {player_total}")
        await state.update_data(total_player=player_total)
        await state.update_data(zuko_sum_card=zuko_total)
        await state.set_state(Game.third_card)
        await message.answer("Играем еще?", reply_markup=choose_buttons)


@dp.message(Game.third_card)
async def third_row(message: Message, state: FSMContext):
    if message.text.lower() == "еще" or message.text.lower() == 'хватит':
        if message.text.lower() == 'еще':
            data = await state.get_data()
            total = 0
            for key, value in data.items():
                if key == 'total_player':
                    total = value
            th_card = random.randint(2, 11)
            third_photo_for_card = img_for_card(th_card)
            total += th_card
            if total > 21:
                await message.answer(f"Тебе выпала: {th_card}")
                await message.answer_photo(third_photo_for_card)
                await message.answer(f"Увы, но ты проиграл, твоя сумма карт {total} начни новую игру через /startgame", reply_markup=start_new_game)
                await state.clear()
            else:
                await message.answer(f"Тебе выпала: {th_card}")
                await message.answer_photo(third_photo_for_card)
                await state.set_state(Game.fourth_card)
                await message.answer(f"Играем еще?Твоя сумма карт: {total}", reply_markup=choose_buttons)
        else:
            zuko_sum = 0
            total = 0
            data = await state.get_data()
            for key, value in data.items():
                if key == 'total_player':
                    total = value
                elif key == 'zuko_sum_card':
                    zuko_sum = value
            await message.answer(f"Ты решил закончить игру, сумма твоих карт {total}", reply_markup=rmk)
            if zuko_sum>total:
                await message.answer(f"Извини коненчо, но в этой игре победил я, сумма моих карт: {zuko_sum}, сумма твоих карт {total}", reply_markup=rmk)
                await message.answer("Ты можешь начать игру заново /startgame", reply_markup=start_new_game)
            else:
                await message.answer(f"Поздравляю с победой, сумма моих карт составляет: {zuko_sum}, а сумма твоих карт: {total}")
                await message.answer(f"Можешь начать новую игру через /startgame", reply_markup=start_new_game)
            await state.clear()
    else:
        await message.answer("Выбери один из вариантов")


@dp.message(Game.fourth_card)
async def fourth_row(message:Message, state: FSMContext):
    await message.answer("Хватит играть!")
    await state.clear()

            


    


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())