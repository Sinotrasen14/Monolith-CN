health-scale-display =
    { $deltasign ->
        [-1] { $kind } 伤害乘以 [color=green]x{ $amount }[/color]
         [0] { $kind } 伤害乘以 x{ $amount }
         [1] { $kind } 伤害乘以 [color=red]x{ $amount }[/color]
        *[other] { $kind } 伤害乘以 x{ $amount }
    }

reagent-effect-guidebook-health-scale =
    { $chance ->
        [1] 使现有 { $changes } 翻倍
       *[other] 有 { $chance }% 的几率使现有 { $changes } 翻倍
    }

reagent-effect-guidebook-claws-growth =
    { $chance ->
        [1] 生长
        *[other] 生长
    } 利爪，在代谢期间以 { $amount } 倍速度

reagent-effect-guidebook-claws-growth-suppression =
    { $chance ->
        [1] 抑制
        *[other] 抑制
    } 利爪生长。
