### Interaction Messages

# When trying to eat food without the required utensil... but you gotta hold it
food-you-need-to-hold-utensil = 你需要手持一个{$utensil}才能吃那个！

food-nom = 咀嚼。{$flavors}
food-swallow = 你吞下了{$food}。{$flavors}

food-has-used-storage = 你无法吃掉里面装有物品的{$food}。

food-system-remove-mask = 你需要先摘下{$entity}。

## System

food-system-you-cannot-eat-any-more = 你吃不下了！
food-system-you-cannot-eat-any-more-other = {CAPITALIZE(SUBJECT($target))}吃不下了！
food-system-try-use-food-is-empty = {CAPITALIZE(THE($entity))}是空的！
food-system-wrong-utensil = 你无法用{INDEFINITE($utensil)}{$utensil}吃{THE($food)}。
food-system-cant-digest = 你无法消化{THE($entity)}！
food-system-cant-digest-other = {CAPITALIZE(SUBJECT($target))}无法消化{THE($entity)}！

food-system-verb-eat = 吃

## Force feeding

food-system-force-feed = {CAPITALIZE(THE($user))}正试图喂你吃东西！
food-system-force-feed-success = {CAPITALIZE(THE($user))}强迫你吃了东西！{$flavors}
food-system-force-feed-success-user = 你成功喂食了{THE($target)}