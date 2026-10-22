gas-deposit-drill-no-resources = 这里没有可提取的东西！
gas-deposit-drill-system-examined = 提取器设定为 [color={$statusColor}]{PRESSURE($pressure)}[/color]。
gas-deposit-drill-system-examined-amount = 提取器报告剩余 {
    $value ->
        [0] [color={$statusColor}]几乎没有[/color]任何东西。
        *[other] 大约 [color={$statusColor}]{GASQUANTITY($value)}[/color]。
    }
gas-deposit-drill-system-examined-yield = 提取器报告剩余 [color={$statusColor}]{NATURALFIXED($yield, 1)}%[/color]{
    $hitMinimum ->
        [false] 的产量。
        *[other] 的产量，并且已到达深层储量。
    }