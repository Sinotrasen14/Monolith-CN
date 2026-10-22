execution-verb-name = 处决
execution-verb-message = 使用你的武器处决某人。

# All the below localisation strings have access to the following variables
# attacker (the person committing the execution)
# victim (the person being executed)
# weapon (the weapon used for the execution)

execution-popup-melee-initial-internal = 你将{THE($weapon)}抵在{THE($victim)}的喉咙上。
execution-popup-melee-initial-external = { CAPITALIZE(THE($attacker)) }将{POSS-ADJ($attacker)}{$weapon}抵在{THE($victim)}的喉咙上。
execution-popup-melee-complete-internal = 你割开了{THE($victim)}的喉咙！
execution-popup-melee-complete-external = { CAPITALIZE(THE($attacker)) }割开了{THE($victim)}的喉咙！

execution-popup-self-initial-internal = 你将{THE($weapon)}抵在自己的喉咙上。
execution-popup-self-initial-external = { CAPITALIZE(THE($attacker)) }将{POSS-ADJ($attacker)}{$weapon}抵在自己的喉咙上。
execution-popup-self-complete-internal = 你割开了自己的喉咙！
execution-popup-self-complete-external = { CAPITALIZE(THE($attacker)) }割开了自己的喉咙！