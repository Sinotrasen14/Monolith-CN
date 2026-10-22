## Rev Head

roles-antag-rev-head-name = 革命领袖
roles-antag-rev-head-objective = 你的目标是通过将人们转化为你的事业并杀死空间站上的所有指挥部人员来接管空间站。

head-rev-role-greeting =
    你是一名革命领袖。
    你的任务是通过死亡、流放或监禁来清除空间站上的所有指挥部人员。
    辛迪加为你赞助了一个闪光弹，可以将船员转化到你这一边。
    注意，这对安保、指挥部或戴着太阳镜的人无效。
    革命万岁！

head-rev-briefing =
    使用闪光弹将人们转化为你的事业。
    清除所有部长以接管空间站。

head-rev-break-mindshield = 心灵护盾被摧毁了！

## Rev

roles-antag-rev-name = 革命者
roles-antag-rev-objective = 你的目标是确保革命领袖的安全并服从他们的命令，同时清除或转化空间站上的所有指挥部人员。

rev-break-control = {$name} 已经记起了他们真正的忠诚！

rev-role-greeting =
    你是一名革命者。
    你的任务是接管空间站并保护革命领袖。
    清除所有指挥部人员。
    革命万岁！

rev-briefing = 帮助你的革命领袖清除每一个部长以接管空间站。

## General

rev-title = 革命者
rev-description = 革命者就在我们中间。

rev-not-enough-ready-players = 没有足够的玩家准备就绪。有 {$readyPlayersCount} 名玩家准备就绪，需要 {$minimumPlayers} 名。无法开始革命。
rev-no-one-ready = 没有玩家准备就绪！无法开始革命。
rev-no-heads = 没有可被选中的革命领袖。无法开始革命。

rev-won = 革命领袖存活并成功夺取了空间站的控制权。

rev-lost = 指挥部存活并杀死了所有革命领袖。

rev-stalemate = 所有革命领袖和指挥部都已死亡。平局。

rev-reverse-stalemate = 指挥部和革命领袖都存活了。

rev-headrev-count = {$initialCount ->
    [one] 有一名革命领袖：
    *[other] 有 {$initialCount} 名革命领袖：
}

rev-headrev-name-user = [color=#5e9cff]{$name}[/color]（[color=gray]{$username}[/color]）转化了 {$count} {$count ->
    [one] 个人
    *[other] 个人
}

rev-headrev-name = [color=#5e9cff]{$name}[/color] 转化了 {$count} {$count ->
    [one] 个人
    *[other] 个人
}

## Deconverted window

rev-deconverted-title = 已解除转化！
rev-deconverted-text =
    随着最后一名革命领袖的死亡，革命结束了。

    你不再是革命者了，所以请友善一点。
rev-deconverted-confirm = 确认