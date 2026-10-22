comp-kitchen-spike-deny-collect = { CAPITALIZE(THE($this)) }上面已经有东西了，先把它的肉取下来！
comp-kitchen-spike-deny-butcher = { CAPITALIZE(THE($victim)) }不能在{ THE($this) }上被屠宰。
comp-kitchen-spike-deny-butcher-knife = { CAPITALIZE(THE($victim)) }不能在{ THE($this) }上被屠宰，你需要用刀来屠宰它。
comp-kitchen-spike-deny-not-dead = { CAPITALIZE(THE($victim)) }不能被屠宰。{ CAPITALIZE(SUBJECT($victim)) } { CONJUGATE-BE($victim) }还没死！

comp-kitchen-spike-begin-hook-victim = { CAPITALIZE(THE($user)) }开始把你拖到{ THE($this) }上！
comp-kitchen-spike-begin-hook-self = 你开始把自己拖到{ THE($this) }上！

comp-kitchen-spike-kill = { CAPITALIZE(THE($user)) }把{ THE($victim) }强行按到了肉刺上，当场将其杀死！

comp-kitchen-spike-suicide-other = { CAPITALIZE(THE($victim)) }扑到了肉刺上！
comp-kitchen-spike-suicide-self = 你扑到了肉刺上！

comp-kitchen-spike-knife-needed = 你需要一把刀才能这样做。
comp-kitchen-spike-remove-meat = 你从{ THE($victim) }身上取下了一些肉。
comp-kitchen-spike-remove-meat-last = 你从{ THE($victim) }身上取下了最后一块肉！

comp-kitchen-spike-meat-name = { $name }（{ $victim }）