from telegram.ext import ConversationHandler

# Состояния для первой сцены
ARRIVAL, EXPLORE_CITY, BAR_CHOICE, MARKET_CHOICE = range(4)

# Состояния для всего разговора в баре
BAR_INTRODUCTION, BAR_RUMORS, BAR_QUEST = range(4, 7)
