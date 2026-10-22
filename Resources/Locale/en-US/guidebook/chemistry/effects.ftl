-create-3rd-person =
    { $chance ->
        [1] 创造
        *[other] 创造
    }

-cause-3rd-person =
    { $chance ->
        [1] 导致
        *[other] 导致
    }

-satiate-3rd-person =
    { $chance ->
        [1] 满足
        *[other] 满足
    }

reagent-effect-guidebook-create-entity-reaction-effect =
    { $chance ->
        [1] 创造
        *[other] 创造
    } { $amount ->
        [1] {INDEFINITE($entname)}
        *[other] {$amount} {MAKEPLURAL($entname)}
    }

reagent-effect-guidebook-explosion-reaction-effect =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 一场爆炸

reagent-effect-guidebook-emp-reaction-effect =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 一次电磁脉冲

reagent-effect-guidebook-flash-reaction-effect =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 一次致盲闪光

reagent-effect-guidebook-foam-area-reaction-effect =
    { $chance ->
        [1] 创造
        *[other] 创造
    } 大量泡沫

reagent-effect-guidebook-smoke-area-reaction-effect =
    { $chance ->
        [1] 创造
        *[other] 创造
    } 大量烟雾

reagent-effect-guidebook-satiate-thirst =
    { $chance ->
        [1] 满足
        *[other] 满足
    } { $relative ->
        [1] 口渴感，以平均速率
        *[other] 口渴感，以 {NATURALFIXED($relative, 3)} 倍平均速率
    }

reagent-effect-guidebook-satiate-hunger =
    { $chance ->
        [1] 满足
        *[other] 满足
    } { $relative ->
        [1] 饥饿感，以平均速率
        *[other] 饥饿感，以 {NATURALFIXED($relative, 3)} 倍平均速率
    }

reagent-effect-guidebook-health-change =
    { $chance ->
        [1] { $healsordeals ->
                [heals] 治疗
                [deals] 造成
                *[both] 修改生命值
             }
        *[other] { $healsordeals ->
                    [heals] 治疗
                    [deals] 造成
                    *[both] 修改生命值
                 }
    } { $changes }

reagent-effect-guidebook-even-health-change =
    { $chance ->
        [1] { $healsordeals ->
            [heals] 均匀治疗
            [deals] 均匀造成
            *[both] 均匀修改生命值
        }
        *[other] { $healsordeals ->
            [heals] 均匀治疗
            [deals] 均匀造成
            *[both] 均匀修改生命值
        }
    } { $changes }


reagent-effect-guidebook-status-effect =
    { $type ->
        [add]   { $chance ->
                    [1] 导致
                    *[other] 导致
                } {LOC($key)}，持续至少 {NATURALFIXED($time, 3)} {MANY("second", $time)}，可累积
        *[set]  { $chance ->
                    [1] 导致
                    *[other] 导致
                } {LOC($key)}，持续至少 {NATURALFIXED($time, 3)} {MANY("second", $time)}，不可累积
        [remove]{ $chance ->
                    [1] 移除
                    *[other] 移除
                } {NATURALFIXED($time, 3)} {MANY("second", $time)} 的 {LOC($key)}
    }

reagent-effect-guidebook-activate-artifact =
    { $chance ->
        [1] 尝试
        *[other] 尝试
    } 激活一件神器

reagent-effect-guidebook-set-solution-temperature-effect =
    { $chance ->
        [1] 将
        *[other] 将
    } 溶液温度精确设置为 {NATURALFIXED($temperature, 2)}k

reagent-effect-guidebook-adjust-solution-temperature-effect =
    { $chance ->
        [1] { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
        *[other]
            { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
    } 溶液中的热量，直到达到 { $deltasign ->
                [1] 最高 {NATURALFIXED($maxtemp, 2)}k
                *[-1] 最低 {NATURALFIXED($mintemp, 2)}k
            }

reagent-effect-guidebook-adjust-reagent-reagent =
    { $chance ->
        [1] { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
        *[other]
            { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
    } {NATURALFIXED($amount, 2)}u 的 {$reagent} { $deltasign ->
        [1] 到
        *[-1] 从
    } 溶液中

reagent-effect-guidebook-adjust-reagent-group =
    { $chance ->
        [1] { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
        *[other]
            { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
    } {NATURALFIXED($amount, 2)}u 的 {$group} 组试剂 { $deltasign ->
            [1] 到
            *[-1] 从
        } 溶液中

reagent-effect-guidebook-adjust-temperature =
    { $chance ->
        [1] { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
        *[other]
            { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
    } {POWERJOULES($amount)} 的热量 { $deltasign ->
            [1] 到
            *[-1] 从
        } 其所在的身体中

reagent-effect-guidebook-chem-cause-disease =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 疾病 { $disease }

reagent-effect-guidebook-chem-cause-random-disease =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 疾病 { $diseases }

reagent-effect-guidebook-jittering =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 颤抖

reagent-effect-guidebook-chem-clean-bloodstream =
    { $chance ->
        [1] 清除
        *[other] 清除
    } 血液中的其他化学物质

reagent-effect-guidebook-cure-disease =
    { $chance ->
        [1] 治愈
        *[other] 治愈
    } 疾病

reagent-effect-guidebook-cure-eye-damage =
    { $chance ->
        [1] { $deltasign ->
                [1] 造成
                *[-1] 治疗
            }
        *[other]
            { $deltasign ->
                [1] 造成
                *[-1] 治疗
            }
    } 眼部损伤

reagent-effect-guidebook-chem-vomit =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 呕吐

reagent-effect-guidebook-create-gas =
    { $chance ->
        [1] 创造
        *[other] 创造
    } { $moles } { $moles ->
        [1] 摩尔
        *[other] 摩尔
    } 的 { $gas }

reagent-effect-guidebook-drunk =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 醉酒

reagent-effect-guidebook-electrocute =
    { $chance ->
        [1] 电击
        *[other] 电击
    } 代谢者，持续 {NATURALFIXED($time, 3)} {MANY("second", $time)}

reagent-effect-guidebook-extinguish-reaction =
    { $chance ->
        [1] 扑灭
        *[other] 扑灭
    } 火焰

reagent-effect-guidebook-flammable-reaction =
    { $chance ->
        [1] 增加
        *[other] 增加
    } 易燃性

reagent-effect-guidebook-ignite =
    { $chance ->
        [1] 点燃
        *[other] 点燃
    } 代谢者

reagent-effect-guidebook-make-sentient =
    { $chance ->
        [1] 使
        *[other] 使
    } 代谢者获得感知

reagent-effect-guidebook-make-polymorph =
    { $chance ->
        [1] 将
        *[other] 将
    } 代谢者变形为 { $entityname }

reagent-effect-guidebook-revert-polymorph =
    { $chance ->
        [1] 将
        *[other] 将
    } 代谢者从 { $entityname } 恢复原形

reagent-effect-guidebook-modify-bleed-amount =
    { $chance ->
        [1] { $deltasign ->
                [1] 引发
                *[-1] 减少
            }
        *[other] { $deltasign ->
                    [1] 引发
                    *[-1] 减少
                 }
    } 出血

reagent-effect-guidebook-modify-blood-level =
    { $chance ->
        [1] { $deltasign ->
                [1] 增加
                *[-1] 减少
            }
        *[other] { $deltasign ->
                    [1] 增加
                    *[-1] 减少
                 }
    } 血液水平

reagent-effect-guidebook-paralyze =
    { $chance ->
        [1] 麻痹
        *[other] 麻痹
    } 代谢者，持续至少 {NATURALFIXED($time, 3)} {MANY("second", $time)}

reagent-effect-guidebook-movespeed-modifier =
    { $chance ->
        [1] 修改
        *[other] 修改
    } 移动速度 {NATURALFIXED($walkspeed, 3)} 倍，持续至少 {NATURALFIXED($time, 3)} {MANY("second", $time)}

reagent-effect-guidebook-reset-narcolepsy =
    { $chance ->
        [1] 暂时阻止
        *[other] 暂时阻止
    } 嗜睡症

reagent-effect-guidebook-wash-cream-pie-reaction =
    { $chance ->
        [1] 洗去
        *[other] 洗去
    } 脸上的奶油派

reagent-effect-guidebook-cure-zombie-infection =
    { $chance ->
        [1] 治愈
        *[other] 治愈
    } 正在进行的丧尸感染

reagent-effect-guidebook-cause-zombie-infection =
    { $chance ->
        [1] 使
        *[other] 使
    } 个体感染丧尸病毒

reagent-effect-guidebook-innoculate-zombie-infection =
    { $chance ->
        [1] 治愈
        *[other] 治愈
    } 正在进行的丧尸感染，并提供对未来感染的免疫力

reagent-effect-guidebook-reduce-rotting =
    { $chance ->
        [1] 恢复
        *[other] 恢复
    } {NATURALFIXED($time, 3)} {MANY("second", $time)} 的腐烂

reagent-effect-guidebook-area-reaction =
    { $chance ->
        [1] 导致
        *[other] 导致
    } 烟雾或泡沫反应，持续 {NATURALFIXED($duration, 3)} {MANY("second", $duration)}

reagent-effect-guidebook-add-to-solution-reaction =
    { $chance ->
        [1] 使
        *[other] 使
    } 施加于物体的化学物质被添加到其内部溶液容器中

reagent-effect-guidebook-plant-attribute =
    { $chance ->
        [1] 调整
        *[other] 调整
    } {$attribute}，幅度为 [color={$colorName}]{$amount}[/color]

reagent-effect-guidebook-plant-cryoxadone =
    { $chance ->
        [1] 使
        *[other] 使
    } 植物逆生长，取决于植物的年龄和生长时间

reagent-effect-guidebook-plant-phalanximine =
    { $chance ->
        [1] 恢复
        *[other] 恢复
    } 因突变而失去活力的植物的活力

reagent-effect-guidebook-plant-diethylamine =
    { $chance ->
        [1] 增加
        *[other] 增加
    } 植物的寿命和/或基础生命值，各有 10% 的概率

reagent-effect-guidebook-plant-robust-harvest =
    { $chance ->
        [1] 增加
        *[other] 增加
    } 植物的效力 {$increase}，最高至 {$limit}。当效力达到 {$seedlesstreshold} 时，植物会失去种子。尝试将效力增加至超过 {$limit} 时，有 10% 的概率导致产量下降

reagent-effect-guidebook-plant-seeds-add =
    { $chance ->
        [1] 恢复植物的
        *[other] 恢复植物的
    } 种子

reagent-effect-guidebook-plant-seeds-remove =
    { $chance ->
        [1] 移除植物的
        *[other] 移除植物的
    } 种子

reagent-effect-guidebook-add-to-chemicals =
    { $chance ->
        [1] { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
        *[other]
            { $deltasign ->
                [1] 添加
                *[-1] 移除
            }
    } {NATURALFIXED($amount, 2)}u 的 {$reagent} { $deltasign ->
        [1] 到
        *[-1] 从
    } 溶液中