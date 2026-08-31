armor-plate-break = 你的{$plateName}已碎裂！
armor-plate-examine-with-plate = 已安装[color=yellow]{$plateName}[/color]。耐久度：[color={$durabilityColor}]{$percent}%[/color]
armor-plate-examine-with-plate-simple = 已安装[color=yellow]{$plateName}[/color]。
armor-plate-examine-no-plate = 未安装装甲板。
armor-plate-examine-no-storage = 没有用于安装装甲板的储物槽。

armor-plate-examinable-verb-text = 装甲板属性
armor-plate-examinable-verb-message = 查看防护与耐久特性。

armor-plate-attributes-examine = 此装甲板：
armor-plate-initial-durability = 额定承受[color=yellow]{ $durability }[/color]标准单位的伤害。

armor-plate-item-durability = 耐久度：[color={$durabilityColor}]{$percent}%[/color]

armor-plate-gait-speed = 速度
armor-plate-gait-walk = 行走速度
armor-plate-gait-sprint = 奔跑速度

armor-plate-speed-display =
    { $deltasign ->
        [-1] 将你的{$gait}提高[color=yellow]{$speedPercent}%[/color]。
         [0] 不影响你的速度。
         [1] 将你的{$gait}降低[color=yellow]{$speedPercent}%[/color]。
        *[other] 不应该有这个速度值！
    }

armor-plate-ratios-display =
    { $deltasign ->
        [-1] [color=cyan]吸收[/color][color=yellow]{$dmgType}[/color]的[color=yellow]{$ratioPercent}%[/color]，并承受[color=yellow]x{$multiplier}[/color]耐久伤害。
         [0] 不受{$dmgType}影响
         [1] [color=fuchsia]放大[/color][color=yellow]{$dmgType}[/color][color=yellow]{$ratioPercent}%[/color]，并承受额外伤害的[color=yellow]x{$multiplier}[/color]耐久伤害。
        *[other] {$dmgType}不应该有这个吸收值！
    }
armor-plate-stamina-value = 将[color=yellow]{$multiplier}%[/color]的吸收伤害转化为体力伤害。
