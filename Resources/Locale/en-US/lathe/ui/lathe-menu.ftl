lathe-menu-title = Lathe Menu
lathe-menu-queue = 队列
lathe-menu-server-list = 服务器列表
lathe-menu-sync = 同步
lathe-menu-search-designs = 搜索设计
lathe-menu-category-all = 全部
lathe-menu-search-filter = 过滤:
lathe-menu-amount = 数量：
lathe-menu-loop = Loop
lathe-menu-skip = Skip If Insufficient
lathe-menu-reagent-slot-examine = 它在一侧有一个放烧杯的槽。
lathe-reagent-dispense-no-container = {THE($name)}中的液体倒在地上了！
lathe-menu-result-reagent-display = {$reagent} ({$amount}u)
lathe-menu-material-display = {$material} ({$amount})
lathe-menu-tooltip-display = {$amount} 份 {$material}
lathe-menu-description-display = [italic]{$description}[/italic]
lathe-menu-material-amount = { $amount ->
    [1] {NATURALFIXED($amount, 2)} {$unit}
    *[other] {NATURALFIXED($amount, 2)} {MAKEPLURAL($unit)}
}
lathe-menu-material-amount-missing = { $amount ->
    [1] {NATURALFIXED($amount, 2)} {$unit} of {$material} ([color=red]{NATURALFIXED($missingAmount, 2)} {$unit} missing[/color])
    *[other] {NATURALFIXED($amount, 2)} {MAKEPLURAL($unit)} of {$material} ([color=red]{NATURALFIXED($missingAmount, 2)} {MAKEPLURAL($unit)} missing[/color])
}
lathe-menu-entity-amount-missing = {$amount} 份与 {$material} ([color=red]{$missingAmount} 缺少[/color])
lathe-menu-reagent-amount-missing = {$amount}u 与 {$material} ([color=red]{$missingAmount}u 缺少[/color])
lathe-menu-no-materials-message = 未装载任何材料。
lathe-menu-silo-linked-message = 矿仓已连接
lathe-menu-fabricating-message = 加工中...
lathe-menu-materials-title = 材料
lathe-menu-queue-title = 制造队列
