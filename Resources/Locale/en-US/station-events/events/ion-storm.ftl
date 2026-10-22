station-event-ion-storm-start-announcement = 空间站附近检测到离子风暴。请检查所有人工智能控制设备是否存在错误。

ion-storm-law-scrambled-number = [font="Monospace"][scramble rate=250 length={$length} chars="@@###$$&%!01"/][/font]

ion-storm-you = 你
# Frontier: the station < the sector
ion-storm-the-station = 空间站
ion-storm-the-crew = 船员
ion-storm-the-job = {$job}
ion-storm-clowns = 小丑
# Frontier: heads of staff < sector command
ion-storm-heads = 部门主管
ion-storm-crew = 船员
ion-storm-people = 人们

ion-storm-adjective-things = {$adjective}的东西
ion-storm-x-and-y = {$x}和{$y}

# joined is short for {$number} {$adjective}
# subjects can generally be threats or jobs or objects
# thing is specified above it
# Frontier: "on the station" < "in the sector"
ion-storm-law-on-station = 空间站上有{$joined}{$subjects}
ion-storm-law-no-shuttle = 由于边境上有{$joined}{$subjects}，换班结束无法呼叫
ion-storm-law-crew-are = {$who}现在是{$joined}{$subjects}

ion-storm-law-subjects-harmful = {$adjective}{$subjects}对船员有害
ion-storm-law-must-harmful = {$must}的人对船员有害
# thing is a concept or action
ion-storm-law-thing-harmful = {$thing}对船员有害
ion-storm-law-job-harmful = {$adjective}{$job}对船员有害
# thing is objects or concept, adjective applies in both cases
# this means you can get a law like "NOT HAVING CHRISTMAS-STEALING COMMUNISM IS HARMFUL TO THE CREW" :)
ion-storm-law-having-harmful = 拥有{$adjective}{$thing}对船员有害
ion-storm-law-not-having-harmful = 不拥有{$adjective}{$thing}对船员有害

# thing is a concept or require
ion-storm-law-requires = {$who}{$plural ->
    [true] 需要
    *[false] 需要
}{$thing}
ion-storm-law-requires-subjects = {$who}{$plural ->
    [true] 需要
    *[false] 需要
}{$joined}{$subjects}

ion-storm-law-allergic = {$who}{$plural ->
    [true] 对
    *[false] 对
}{$allergy}{$severity}过敏
ion-storm-law-allergic-subjects = {$who}{$plural ->
    [true] 对
    *[false] 对
}{$adjective}{$subjects}{$severity}过敏

ion-storm-law-feeling = {$who}{$feeling}{$concept}
ion-storm-law-feeling-subjects = {$who}{$feeling}{$joined}{$subjects}

ion-storm-law-you-are = 你现在是{$concept}
ion-storm-law-you-are-subjects = 你现在是{$joined}{$subjects}
ion-storm-law-you-must-always = 你必须始终{$must}
ion-storm-law-you-must-never = 你绝不能{$must}

ion-storm-law-eat = {$who}必须吃{$adjective}{$food}才能生存
ion-storm-law-drink = {$who}必须喝{$adjective}{$drink}才能生存

ion-storm-law-change-job = {$who}现在是{$adjective}{$change}
ion-storm-law-highest-rank = {$who}现在是最高级别的船员
ion-storm-law-lowest-rank = {$who}现在是最低级别的船员

ion-storm-law-crew-must = {$who}必须{$must}
ion-storm-law-crew-must-go = {$who}必须前往{$area}

ion-storm-part = {$part ->
    [true] 是
    *[false] 不是
}
# due to phrasing, this would mean a law such as
# ONLY HUMANS ARE NOT PART OF THE CREW
# would make non-human nukies/syndies/whatever crew :)
ion-storm-law-crew-only-1 = 只有{$who}{$part}船员
ion-storm-law-crew-only-2 = 只有{$who}和{$other}{$part}船员
ion-storm-law-crew-only-subjects = 只有{$adjective}{$subjects}{$part}船员
ion-storm-law-crew-only-species = 所有{$species}{$part}船员
ion-storm-law-crew-must-do = 只有{$must}的人{$part}船员
ion-storm-law-crew-must-have = 只有拥有{$adjective}{$objects}的人{$part}船员
ion-storm-law-crew-must-eat = 只有吃{$adjective}{$food}的人{$part}船员

ion-storm-law-harm = 你必须伤害{$who}，并且不得通过不作为允许他们逃脱伤害
ion-storm-law-protect = 你绝不能伤害{$who}，并且不得通过不作为允许他们受到伤害

# implementing other variants is annoying so just have this one
# COMMUNISM IS KILLING CLOWNS
ion-storm-law-concept-verb = {$concept}正在{$verb}{$subjects}

# leaving out renaming since its annoying for players to keep track of