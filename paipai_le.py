import random
import copy

# 所有卡片
cards = "数码卡、办公卡、健康卡、彩妆卡、餐具卡、茶香卡、宠物卡、厨具卡、" \
        "床品卡、服饰卡、户外卡、护肤卡、家电卡、家居卡、家具卡、建材卡、出行卡、" \
        "美酒卡、乐器卡、生鲜卡、美发卡、母婴卡、农具卡、配饰卡、灯具卡、食品卡、书籍卡、" \
        "童装卡、文玩卡、五金卡、洗护卡、植物卡、箱包卡、鞋履卡、药品卡、运动卡、潮玩卡、节庆卡、厨电卡、饮料卡"

# 双十一的开奖
old_lottery = "家居卡、餐具卡、乐器卡、运动卡、出行卡、护肤卡、" \
              "文玩卡、农具卡、茶香卡、节庆卡、厨具卡、餐具卡、" \
              "箱包卡、配饰卡、鞋履卡、药品卡、美酒卡、服饰卡、" \
              "五金卡、数码卡、文玩卡、餐具卡、童装卡、鞋履卡、" \
              "宠物卡、书籍卡、建材卡、服饰卡、配饰卡、节庆卡、" \
              "床品卡、灯具卡、农具卡、健康卡、食品卡、服饰卡、" \
              "厨具卡、植物卡、家具卡、潮玩卡、彩妆卡、床品卡、" \
              "出行卡、植物卡、母婴卡、箱包卡、办公卡、药品卡、" \
              "家电卡、彩妆卡、服饰卡、" \
              "健康卡、茶香卡、厨具卡、厨电卡"

# 双十二的开奖
lottery = '家具卡、灯具卡、茶香卡、药品卡、' \
          '植物卡、厨具卡、床品卡、母婴卡、' \
          '彩妆卡、服饰卡、五金卡、厨电卡、' \
          '厨电卡、护肤卡、茶香卡、美发卡'

cards = cards.split('、')
# print(cards)
# lottery = lottery.split('、')
# print(lottery)
# old_lottery = old_lottery.split('、')
# print(old_lottery)

# times = {key: 0 for key in cards}
# old_times = times
# old_times = copy.deepcopy(times)

# # 双十二开奖次数
# for key in lottery:
#     times[key] += 1
# print(times)
# times = sorted(times.items(), key=lambda kv: kv[1], reverse=True)
# print(times)

# 双十一开奖次数
# for key in old_lottery:
#     old_times[key] += 1
# print(old_times)
# old_times = list(sorted(old_times.items(), key=lambda kv: kv[1], reverse=True))
# print(old_times)

# # 打印双十一高频开奖，双十二未开奖
# for i in old_times:
#     if i[1] == 2:
#         break
#     if i[0] in lottery:
#         continue
#     print(i)

# 卡片选择
card_sel = set()
count = 1
target = 16
# while count <= target:
#     index = random.randint(0, len(old_lottery) - 1)
#     # 双十二还没开奖，并且双十一开奖少于3次
#     # if old_lottery[index] not in lottery and old_times[old_lottery[index]] < 3 and old_lottery[index] not in card_sel:
#     if old_lottery[index] not in lottery and old_lottery[index] not in card_sel:
#         card_sel.add(old_lottery[index])
#         count += 1
# while count <= target:
#     index = random.randint(0, len(cards) - 1)
#     if cards[index] not in card_sel:
#         card_sel.add(cards[index])
#         count += 1
# print(card_sel)
# 每行五个进行输出
# card_sel = list(card_sel)
# print(card_sel)
# for i in range(int(target / 5 + 1)):
#     print(card_sel[i * 5:i * 5 + 5:])

# 2023/01/07	3
liuhecai = [33, 10, 43, 34, 49, 31, 40]
for index in liuhecai:
    index = index % len(cards)
    card_sel.add(cards[index])
print(card_sel)
