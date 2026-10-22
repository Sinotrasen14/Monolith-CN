### Solution transfer component

comp-solution-transfer-fill-normal = 你从{THE($owner)}向{THE($target)}注入{$amount}u。
comp-solution-transfer-fill-fully = 你从{THE($owner)}向{THE($target)}注满{$amount}u。
comp-solution-transfer-transfer-solution = 你向{THE($target)}转移{$amount}u。

## Displayed when trying to transfer to a solution, but either the giver is empty or the taker is full
comp-solution-transfer-is-empty = {CAPITALIZE(THE($target))}是空的！
comp-solution-transfer-is-full = {CAPITALIZE(THE($target))}已满！

## Displayed in change transfer amount verb's name
comp-solution-transfer-verb-custom-amount = 自定义
comp-solution-transfer-verb-amount = {$amount}u
comp-solution-transfer-verb-toggle = 切换为{$amount}u

## Displayed after you successfully change a solution's amount using the BUI
comp-solution-transfer-set-amount = 转移量已设为{$amount}u。
comp-solution-transfer-set-amount-max = 最大：{$amount}u
comp-solution-transfer-set-amount-min = 最小：{$amount}u