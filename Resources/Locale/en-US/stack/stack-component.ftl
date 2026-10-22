### UI

# Shown when a stack is examined in details range
comp-stack-examine-detail-count = {$count ->
    [one] 这堆物品中有 [color={$markupCountColor}]{$count}[/color] 个
    *[other] 这堆物品中有 [color={$markupCountColor}]{$count}[/color] 个
}。

# Stack status control
comp-stack-status = 数量：[color=white]{$count}[/color]

### Interaction Messages

# Shown when attempting to add to a stack that is full
comp-stack-already-full = 堆叠已满。

# Shown when a stack becomes full
comp-stack-becomes-full = 堆叠现已满。

# Text related to splitting a stack
comp-stack-split = 你拆分了一堆物品。
comp-stack-split-halve = 对半拆分
comp-stack-split-custom = 自定义拆分数量...
comp-stack-split-too-small = 堆叠太小，无法拆分。

# Cherry-picked from space-station-14#32938 courtesy of Ilya246
comp-stack-split-size = 最大：{$size}

ui-custom-stack-split-title = 拆分数量
ui-custom-stack-split-line-edit-placeholder = 数量
ui-custom-stack-split-apply = 拆分
# End cherry-pick from ss14#32938