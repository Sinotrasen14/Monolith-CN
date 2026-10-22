objectives-round-end-result = {$count ->
    [one] 有一个 {$agent}。
    *[other] 有 {$count} 个 {MAKEPLURAL($agent)}。
}

objectives-round-end-result-in-custody = {$count} 个 {MAKEPLURAL($agent)} 中有 {$custody} 个被拘留。

objectives-player-user-named = [color=White]{$name}[/color]（[color=gray]{$user}[/color]）
objectives-player-named = [color=White]{$name}[/color]

objectives-no-objectives = {$custody}{$title} 是一个 {$agent}。
objectives-with-objectives = {$custody}{$title} 是一个 {$agent}，其目标如下：

objectives-objective-success = {$objective} | [color=green]成功！[/color]（{TOSTRING($progress, "P0")}）
objectives-objective-fail = {$objective} | [color=red]失败！[/color]（{TOSTRING($progress, "P0")}）

objectives-in-custody = [bold][color=red]| 被拘留 | [/color][/bold]