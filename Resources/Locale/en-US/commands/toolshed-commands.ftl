command-description-visualize =
    将输入的实体列表放入一个 UI 窗口中以便浏览。
command-description-runverbas =
    以给定的用户对输入实体运行一个动词。
command-description-acmd-perms =
    返回给定指令的管理员权限（如果有）。
command-description-acmd-caninvoke =
    检查给定玩家是否可以调用给定指令。
command-description-jobs-jobs =
    返回空间站上的所有职位。
command-description-jobs-job =
    返回空间站上的给定职位。
command-description-jobs-isinfinite =
    如果输入的职位是无限的则返回 true，否则返回 false。
command-description-jobs-adjust =
    调整给定职位的槽位数量。
command-description-jobs-set =
    设置给定职位的槽位数量。
command-description-jobs-amount =
    返回给定职位的槽位数量。
command-description-jobs-unlimited =
    使给定职位拥有无限槽位。
command-description-laws-list =
    返回所有受法则约束的实体的列表。
command-description-laws-get =
    返回给定实体的所有法则。
command-description-stations-list =
    返回所有空间站的列表。
command-description-stations-get =
    获取活动空间站，当且仅当只有一个时。
command-description-stations-getowningstation =
    获取给定实体“所属”（位于其中）的空间站。
command-description-stations-grids =
    返回与输入空间站关联的所有网格。
command-description-stations-config =
    返回与输入空间站关联的配置（如果有）。
command-description-stations-addgrid =
    向给定空间站添加一个网格。
command-description-stations-rmgrid =
    从给定空间站移除一个网格。
command-description-stations-rename =
    重命名给定空间站。
command-description-stations-largestgrid =
    返回给定空间站拥有的最大网格（如果有）。
command-description-stations-rerollBounties =
    清除空间站当前的所有赏金并获取新的选择。
command-description-stationevent-lsprob =
    给定一个 BasicStationEventScheduler 原型，列出在当前条件下不同空间站事件在整个事件池中发生的概率。
command-description-stationevent-lsprobtheoretical =
    给定一个 BasicStationEventScheduler 原型、玩家数量和回合时间，根据指定的玩家数量和回合时间列出不同空间站事件发生的概率。
command-description-stationevent-prob =
    给定一个 BasicStationEventScheduler 原型和一个事件原型，返回在当前条件下单个空间站事件在整个事件池中发生的概率。
command-description-admins-active =
    返回活跃管理员的列表。
command-description-admins-all =
    返回所有管理员的列表，包括已被取消管理员权限的。
command-description-marked =
    将 $marked 的值作为 List<EntityUid> 返回。
command-description-rejuvenate =
    使给定实体恢复活力，将其恢复到完全健康、清除状态效果等。
command-description-tag-list =
    列出给定实体上的标签。
command-description-tag-with =
    从管道输入的实体列表中仅返回具有给定标签的实体。
command-description-tag-add =
    向给定实体添加一个标签。
command-description-tag-rm =
    从给定实体移除一个标签。
command-description-tag-addmany =
    向给定实体添加一组标签。
command-description-tag-rmmany =
    从给定实体移除一组标签。
command-description-polymorph =
    使用给定原型对输入实体进行变形。
command-description-unpolymorph =
    还原变形。
command-description-solution-get =
    从给定实体上获取给定溶液。
command-description-solution-adjreagent =
    调整给定溶液上的给定试剂。
command-description-mind-get =
    从实体上获取意识（如果有）。
command-description-mind-control =
    以给定玩家接管一个实体的控制权。
command-description-addaccesslog =
    为此实体添加一条访问日志。请注意，这会绕过日志的默认限制和暂停检查。
command-description-stationevent-simulate =
    给定一个 BasicStationEventScheduler 原型、N 个回合、N 个玩家、平均回合结束时间和回合结束时间的标准差，模拟 N 个会发生事件的回合，并在之后打印每个事件的发生次数。
command-description-xenoartifact-list =
    列出所有已生成异形神器的 EntityUid。
command-description-xenoartifact-printMatrix =
    打印显示节点之间所有边的矩阵。
command-description-xenoartifact-totalResearch =
    获取当前可以从异形神器中提取的所有科研部点数。
command-description-xenoartifact-averageResearch =
    计算异形神器完全激活时平均会输出的科研部点数。
command-description-xenoartifact-unlockAllNodes =
    解锁异形神器的所有节点。
command-description-jobboard-completeJob =
    为空间站完成给定的打捞工作板工作。
command-description-scale-set =
    将实体的贴图大小设置为特定比例（不改变其碰撞体）。
command-description-scale-get =
    获取由 ScaleVisualsComponent 设置的实体贴图比例。不包括直接在 SpriteComponent 中所做的任何更改。
command-description-scale-multiply =
    将实体的贴图大小乘以特定系数（不改变其碰撞体）。
command-description-scale-multiplywithfixture =
    将实体的贴图大小乘以特定系数（包括其碰撞体）。