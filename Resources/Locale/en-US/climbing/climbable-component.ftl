### UI

# Verb name for climbing
comp-climbable-verb-climb = 翻越

### Interaction Messages

# Shown to you when your character climbs on $climbable
comp-climbable-user-climbs = 你跳上了 { THE($climbable) }！

# Shown to others when $user climbs on $climbable
comp-climbable-user-climbs-other  = { CAPITALIZE(THE($user)) }跳上了 { THE($climbable) }！

# Shown to you when your character forces someone to climb on $climbable
comp-climbable-user-climbs-force = 你强迫 { THE($moved-user) } 爬上了 { THE($climbable) }！

# Shown to others when someone forces other $moved-user to climb on $climbable
comp-climbable-user-climbs-force-other = { CAPITALIZE(THE($user)) }强迫 { THE($moved-user) } 爬上了 { THE($climbable) }！

# Shown to you when your character is far away from climbable
comp-climbable-cant-reach = 你够不到那里！

# Shown to you when your character can't interact with climbable for some reason
comp-climbable-cant-interact = 你无法这样做！

# Shown to you when your character isn't able to climb by their own actions
comp-climbable-cant-climb = 你无法攀爬！

# Shown to you when your character tries to force someone else who can't climb onto a climbable
comp-climbable-target-cant-climb = { CAPITALIZE(THE($moved-user)) }无法到那里去！