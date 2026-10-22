### Interaction Messages

# Shown when player tries to replace light, but there is no lights left
comp-light-replacer-missing-light = {THE($light-replacer)}里没有剩余灯泡了。

# Shown when player inserts light bulb inside light replacer
comp-light-replacer-insert-light =你将{$bulb}插入到{THE($light-replacer)}中。

# Shown when player tries to insert in light replacer brolen light bulb
comp-light-replacer-insert-broken-light = 你不能插入坏掉的灯泡！

# Shown when player refill light from light box
comp-light-replacer-refill-from-storage = 你装填了{THE($light-replacer)}。

### Examine 

comp-light-replacer-no-lights = 它是空的。
comp-light-replacer-has-lights = 它包含以下内容：
comp-light-replacer-light-listing = {$amount ->
    [one] [color=yellow]{$amount}[/color] [color=gray]{$name}[/color]
    *[other] [color=yellow]{$amount}[/color] [color=gray]{$name}[/color]
}