## SuspicionGui.xaml.cs

# Shown when clicking your Role Button in Suspicion
suspicion-ally-count-display = {$allyCount ->
    *[zero] 你没有盟友
    [one] 你的盟友是 {$allyNames}
    [other] 你的盟友是 {$allyNames}
}