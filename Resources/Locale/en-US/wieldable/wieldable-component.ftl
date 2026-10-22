### Locale for wielding items; i.e. two-handing them

wieldable-verb-text-wield = 持握
wieldable-verb-text-unwield = 松开

wieldable-component-successful-wield = 你持握了 { THE($item) }。
wieldable-component-failed-wield = 你松开了 { THE($item) }。
wieldable-component-successful-wield-other = { CAPITALIZE(THE($user)) } 持握了 { THE($item) }。
wieldable-component-failed-wield-other = { CAPITALIZE(THE($user)) } 松开了 { THE($item) }。

wieldable-component-no-hands = 你没有足够的手！
wieldable-component-not-enough-free-hands = {$number ->
    [one] 你需要一只空闲的手来持握 { THE($item) }。
    *[other] 你需要 { $number } 只空闲的手来持握 { THE($item) }。
}
wieldable-component-not-in-hands = { CAPITALIZE(THE($item)) } 不在你手中！

wieldable-component-requires = { CAPITALIZE(THE($item))} 必须被持握！

gunwieldbonus-component-examine = 此武器在持握时精度更高。

gunrequireswield-component-examine = 此武器只能在持握时开火。