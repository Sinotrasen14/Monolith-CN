## Survivor

roles-antag-survivor-name = 幸存者
# It's a Halo reference
roles-antag-survivor-objective = 当前目标：活下去

survivor-role-greeting =
    你是一名幸存者。
    最重要的是，你必须活着回到纳米传讯。
    收集足够多的火力来保证你的生存。
    不要相信任何人。

survivor-round-end-dead-count =
{
    $deadCount ->
        [one] [color=red]{$deadCount}[/color] 名幸存者死亡。
        *[other] [color=red]{$deadCount}[/color] 名幸存者死亡。
}

survivor-round-end-alive-count =
{
    $aliveCount ->
        [one] [color=yellow]{$aliveCount}[/color] 名幸存者被遗弃在空间站上。
        *[other] [color=yellow]{$aliveCount}[/color] 名幸存者被遗弃在空间站上。
}

survivor-round-end-alive-on-shuttle-count =
{
    $aliveCount ->
        [one] [color=green]{$aliveCount}[/color] 名幸存者活着逃了出来。
        *[other] [color=green]{$aliveCount}[/color] 名幸存者活着逃了出来。
}

## Wizard

objective-issuer-swf = [color=turquoise]太空巫师联合会[/color]

wizard-title = 巫师
wizard-description = 空间站上有一个巫师！你永远不知道他们会做什么。

roles-antag-wizard-name = 巫师
roles-antag-wizard-objective = 给他们一个永生难忘的教训。

wizard-role-greeting =
    你是个巫师！
    太空巫师联合会和纳米传讯之间一直关系紧张。
    所以你被太空巫师联合会选中，去空间站拜访一趟。
    给他们好好展示一下你的力量。
    你想做什么由你决定，只要记住太空巫师们希望你活着回去。

wizard-round-end-name = 巫师

## TODO: Wizard Apprentice (Coming sometime post-wizard release)