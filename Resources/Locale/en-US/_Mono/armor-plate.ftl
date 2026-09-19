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
    { $stringClause ->
         [1] 将你的{$gait}提高[color=yellow]{$speedPercent}%[/color]。
         [-1] 将你的{$gait}降低[color=yellow]{$speedPercent}%[/color]。
        *[other] 不应该有这个速度值！
    }

armor-plate-ratios-display =
    { $stringClause ->
        [1] [color=cyan]吸收[/color] [color=yellow]{$ratioPercent}%[/color] 于 [color=yellow]{$dmgType}[/color]
        [-1] [color=fuchsia]增加[/color] [color=yellow]{$dmgType}[/color] 于 [color=yellow]{$ratioPercent}%[/color]
        [0] 不影响 [color=yellow]{$dmgType}[/color]
       *[other] {$dmgType} 不应该有这个吸收值！
    }

armor-plate-multiplier-display = 并扣除 [color=yellow]{$multiplier}%[/color] 来自耐久度的原始伤害值。
armor-plate-multiplier-none = 并且不会损坏护甲板。

armor-plate-stamina-source-absorb = [color=cyan]吸收[/color]
armor-plate-stamina-concat = 和
armor-plate-stamina-source-amplified = [color=fuchsia]放大[/color]
armor-plate-stamina-source-raw = [color=red]所有正面伤害[/color]
armor-plate-stamina-value = 造成 [color=yellow]{$multiplier}%[/color] 于 {$sources} 作为耐力伤害

