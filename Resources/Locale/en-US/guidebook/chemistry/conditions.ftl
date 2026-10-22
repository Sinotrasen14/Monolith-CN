reagent-effect-condition-guidebook-total-damage =
    { $max ->
        [2147483648] 它至少有 {NATURALFIXED($min, 2)} 点总伤害
        *[other] { $min ->
                    [0] 它最多有 {NATURALFIXED($max, 2)} 点总伤害
                    *[other] 它的总伤害在 {NATURALFIXED($min, 2)} 到 {NATURALFIXED($max, 2)} 之间
                 }
    }

reagent-effect-condition-guidebook-total-hunger =
    { $max ->
        [2147483648] 目标至少有 {NATURALFIXED($min, 2)} 点总饥饿值
        *[other] { $min ->
                    [0] 目标最多有 {NATURALFIXED($max, 2)} 点总饥饿值
                    *[other] 目标的总饥饿值在 {NATURALFIXED($min, 2)} 到 {NATURALFIXED($max, 2)} 之间
                 }
    }

reagent-effect-condition-guidebook-reagent-threshold =
    { $max ->
        [2147483648] 至少有 {NATURALFIXED($min, 2)}u 的{$reagent}
        *[other] { $min ->
                    [0] 最多有 {NATURALFIXED($max, 2)}u 的{$reagent}
                    *[other] 有 {NATURALFIXED($min, 2)}u 到 {NATURALFIXED($max, 2)}u 的{$reagent}
                 }
    }

reagent-effect-condition-guidebook-mob-state-condition =
    生物处于 { $state } 状态

reagent-effect-condition-guidebook-job-condition =
    目标的职业是 { $job }

reagent-effect-condition-guidebook-solution-temperature =
    溶液的温度为 { $max ->
            [2147483648] 至少 {NATURALFIXED($min, 2)}k
            *[other] { $min ->
                        [0] 最多 {NATURALFIXED($max, 2)}k
                        *[other] 在 {NATURALFIXED($min, 2)}k 到 {NATURALFIXED($max, 2)}k 之间
                     }
    }

reagent-effect-condition-guidebook-body-temperature =
    身体的温度为 { $max ->
            [2147483648] 至少 {NATURALFIXED($min, 2)}k
            *[other] { $min ->
                        [0] 最多 {NATURALFIXED($max, 2)}k
                        *[other] 在 {NATURALFIXED($min, 2)}k 到 {NATURALFIXED($max, 2)}k 之间
                     }
    }

reagent-effect-condition-guidebook-organ-type =
    进行代谢的器官 { $shouldhave ->
                                [true] 是
                                *[false] 不是
                           } {INDEFINITE($name)} {$name} 器官

reagent-effect-condition-guidebook-has-tag =
    目标 { $invert ->
                 [true] 没有
                 *[false] 有
                } 标签 {$tag}

reagent-effect-condition-guidebook-blood-reagent-threshold =
    { $max ->
        [2147483648] 至少有 {NATURALFIXED($min, 2)}u 的{$reagent}
        *[other] { $min ->
                    [0] 最多有 {NATURALFIXED($max, 2)}u 的{$reagent}
                    *[other] 有 {NATURALFIXED($min, 2)}u 到 {NATURALFIXED($max, 2)}u 的{$reagent}
                 }
    }

reagent-effect-condition-guidebook-this-reagent = 此试剂