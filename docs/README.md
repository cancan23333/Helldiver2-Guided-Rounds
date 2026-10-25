# Guided Rounds 说明书

[English](README.en.md) | **简体中文** · [返回项目首页](../README.md)

Guided Rounds 把 **P-92 法令**的制导行为装到武器清单里的每一把枪上。弹丸出膛后
在瞄准锥里挑一个目标并追上去；**伤害、初速、弹道都还是武器自己的数值**。

- 作者：cancan2333 & SoS2430
- 版本：1.9.14
- 需要：Bingus Shared Loader v15+、Vanilla Plus Megapack；HD2Runtime 可选（装了优先交给它——它的资源同步能让没装包的队友也看到弹丸；拒收时自动回退内置装载器）
- 源码：`docs/guided_rounds.lua` · 构建：`build.py`

## 安装

1. 安装 [HD2 Arsenal](https://www.nexusmods.com/helldivers2/mods/4664) 加载器。
2. 用 HD2 Arsenal 导入 `Guided-Rounds-v1.9.14.zip`，并装好
   [Bingus Shared Loader](https://ayakamods.com/mods/bingus-shared-loader.3861/)、
   [Vanilla Plus Megapack](https://www.nexusmods.com/helldivers2/mods/16294)。
   [hd2runtime](https://ayakamods.com/mods/hd2runtime.4260/) 可选：装了优先交给它（它的大厅同步
   能让没装包的队友也看到弹丸）；不装或拒收时，由本 mod 内置装载器加载。
3. 加载顺序自上而下：**Guided Rounds → Vanilla Plus Megapack → Bingus Shared Loader → hd2runtime**（没装 hd2runtime 就省掉最后一项）。
4. 进游戏，**Esc → MODS** 打开设置。

材质由 HD2Runtime 或内置装载器加载；只有当内置装载器不认识当前游戏 build、且没有可用的 HD2Runtime 时，才会显示成紫色问号。

## 菜单地图

打包器按分类名首两个数字排序，所以页面编号固定：

| 页面 | 内容 | 行数上限 |
| --- | --- | ---: |
| `01 · GUIDED ROUNDS` | 总开关、11 个滑条、16 个开关 | 32 |
| `02 · GUIDED EXPLOSIVE FUSE` | 4 个引信滑条 | 32 |
| `03–11 · GUIDED <类型>` | 9 个武器分类，每把枪 4 个选项 | 每页 32 |
| `12 · GUIDED WEAPON PRIORITY` | 选枪，决定优先级页编辑谁的表 | 31 |
| `13 · GUIDED TARGET PRIORITY` | 手动优先级总开关 | 32 |
| `14+ · GUIDED TERMINIDS` | 终结族，32 个/页 | 32 |
| `14+ · GUIDED AUTOMATONS` | 机器人，32 个/页 | 32 |
| `14+ · GUIDED ILLUMINATE` | 光能族 | 32 |
| `14+ · GUIDED OTHER TARGETS` | 载具、建筑、其他 | 32 |

武器分类：突击步枪、炸弹、射手步枪、冲锋枪、霰弹枪、支援武器、能量武器、特殊武器、
手枪。支援武器不论原始类型都进「支援武器」页。名称随游戏语言切换中/英文。

### 03–11 武器页：每把枪四个选项

| 选项 | 作用 |
| --- | --- |
| `OFF` | 这把枪不制导 |
| `AIM FIRST` | 制导，准心最近的目标优先 |
| `BIGGEST HP FIRST` | 制导，最大血量大优先 |
| `SMALLEST HP FIRST` | 制导，最大血量小优先 |

前两项写 `weapons=`，后两项分别写 `prio_targets=` / `prio_small=`。

### 12 单枪优先级页

按分类（`wpcls`）列出已经打开锁定的枪，每行三态：

- `OFF` —— 关掉这把枪自己的表（`wpc_<枪>=0`）。若它正是编辑目标，编辑目标一并清空。
- `CUSTOM` —— 打开这把枪自己的表，**并把 13–19 页切到它的表**。
- `EDIT` —— 同上，并且本轮菜单里行首带 `*` 标记。

`CUSTOM` / `EDIT` 都会强制 `glob_edit=0`，否则优先级页写的是全局表。

## 01 主设置页

| 滑条 | 键 | 范围 | 默认 | 作用 |
| --- | --- | ---: | ---: | --- |
| LOCK ANGLE (deg) | `cone_deg` | 0–60 | 12 | 目标偏离枪口多少度内可锁定；0 = 无圆环 |
| LOCK RANGE (m) | `max_dist` | 0–500 | 250 | 最远锁定距离 |
| ARM TIME AFTER MUZZLE (s) | `bind_delay` | 0–2 | 0.25 | 出膛后多久允许绑定 |
| SCOPE LOCK SCALE | `scope_scale` | 0.05–1 | 0.3 | 仅开镜锁定跟随倍镜时生效 |
| TARGET REFRESH (frames) | `target_interval` | 1–60 | 20 | 每多少帧重建目标列表 |
| BALLISTICS ROW SPEED (mps) | `round_speed` | 0–2000 | 0 | 实弹武器初速，0 = 不改 |
| BALLISTICS ROW GRAVITY | `round_gravity` | -1–3 | -1 | 弹道重力倍数，-1 = 不改 |
| BOMBLET ARM TIME (s) | `cluster_delay` | 0–1 | 0.05 | 子弹药炸开后多久允许绑定 |
| BOMBLET SEEKER (0–7) | `cluster_seeker` | 0–7 | 1 | 子弹药借用的追踪实体 |
| ROCKET SEEKER (0–9) | `launcher_seeker` | 0–9 | 0 | 集束火箭本体借用的追踪实体 |
| GUIDED DARTS PER SHOT | `swarm_count` | 0–64 | 25 | ≥2 时「集束」变成制导霰弹 |

追踪弹实体 0–7：0 = P-92 法令（TargetLock，需要武器锁定），1 = MLS-4X 突击兵导弹，
2 = 爱国者外骨骼火箭，3 = 单兵导弹井导弹，4 = 普通 Guidance，5 = 敌人追踪火箭，
6 = 快速 Behaviour 追踪弹，7 = Vox Engine（等 mod 发布目标）。`launcher_seeker`
另有 8 = P-33 手枪弹、9 = FAF-14 飞矛。

### 开关

| 开关 | 键 | 默认 | 作用 |
| --- | --- | ---: | --- |
| RANGE RING | `range_ring` | 1 | 准心外的索敌圆环 |
| LOCK MARKERS | `lock_reticle` | 1 | 原版锁定标记 |
| TARGET BOX | `target_box` | 1 | 被锁目标外面的线框 |
| LOCK HELLDIVERS ONLY | `lock_helldivers` | 0 | 只锁队友 |
| LOCK ILLUMINATE WARPSHIPS | `lock_shuttle` | 0 | 允许锁穿梭舰与护盾 |
| LOCK AUTOMATON DROPSHIPS | `lock_dropship` | 0 | 允许锁机器人运输舰 |
| ONLY GUIDE THE FLAK ROUND | `flak_only` | 1 | 集束模式保持原厂，只制导高射弹 |
| BIND TARGET OURSELVES | `lua_bind` | 1 | 引擎没锁时由 mod 补绑 |
| REQUIRES LINE OF SIGHT | `los_check` | 1 | 隔掩体不锁 |
| SHOOT THROUGH FOLIAGE | `los_foliage` | 1 | 树叶不算遮挡 |
| NEAREST ENEMY FALLBACK | `cone_fallback` | 0 | 锥内没人时改锁最近敌人 |
| GUIDE RL-77 CLUSTER BOMBLETS | `cluster_guide` | 1 | 给 RL-77 子弹药装制导 |
| KEEP THE WEAPON OWN DAMAGE | `apw_damage` | 1 | 保留武器自己的伤害 |
| LOAD PROJECTILE MATERIALS | `require_assets` | 1 | 保持弹丸材质加载（装了 HD2Runtime 优先，否则内置装载器） |
| FOLLOW THE SCOPE ZOOM | `scope_fix` | 0 | 开镜锁定范围随倍镜放大 |
| ENABLE | `enable` | 1 | 总开关（F7 重启同一开关） |

## 02 爆炸引信页

| 滑条 | 键 | 范围 | 默认 | 作用 |
| --- | --- | ---: | ---: | --- |
| ROUND FUSE TIME (s) | `round_life` | 0–15 | 0 | 实弹弹丸自爆计时，0 = 不改 |
| CLUSTER BOMBLET LIFE (s) | `cluster_life` | 0.1–8 | 3 | 子弹药寿命，原厂 0（永不超时） |
| CLUSTER AIRBURST DELAY (s) | `rocket_life` | 0–5 | 1.5 | 集束弹出膛后多久起爆，原厂 0.25 |
| CLUSTER PROXIMITY FUSE (m) | `rocket_prox` | 0–20 | 0 | 补一个近炸引信，0 = 关闭 |

## 三层目标优先级

锁定时的顺序：先看**目标优先级**（数字小优先），数字相同时才用该枪的**瞄准模式**
（准心 / 最大血量大 / 最大血量小）比较。

### 第一层：每把枪的瞄准模式（03–11 页）

粗粒度四选一，见上文武器页表。没有独立表。

### 第二层：全局优先级表（13–19 页）

`prio_manual=1` 打开。每个目标一个 0–9 滑条：**1 最先锁，9 最后，0 = 未设置**。
写入 `tp_<16位十六进制目标>=<n>`。页面没列出的目标也能手加。

### 第三层：单枪优先级表（12 页 + 13–19 页）

这是重点，也是 v1.9.11 修过的地方：

1. 在 12 页找到枪，选 `CUSTOM`（或 `EDIT`）。mod 记下这把枪作为编辑目标
   （`wprio_sel=0x<枪>`，`wpc_<枪>=1`）并关掉 `glob_edit`。
2. 到 13–19 页拖滑条。此时写的是 **`wpw_<枪>_<目标>=<n>`**，页面名显示这把枪的名字。
3. 换另一把枪：回 12 页选它的 `CUSTOM`，再拖。`wpw_` 行按枪隔离，互不影响。

规则：

- **0 = 未设置**：该枪这张表里拖到 0，锁定时回退到全局 `tp_`（两层都是 0 才真正
  「没有优先级」，交给瞄准模式）。
- 表只影响「手上那把枪」：判定用的是准心指向的武器，而不是背上那把。
- 关掉某把枪的 `CUSTOM`（选 `OFF`）后它立刻回到全局表，`wpw_` 行保留不删。
- `glob_edit=1` 时 13–19 页改回写全局 `tp_`（页面名显示 GLOBAL），单枪表仍在。

## cfg 参数参考

路径：`%LOCALAPPDATA%\Hd2ApwGuidance\apw_guidance.cfg`。菜单会自动写；手改请在游戏
关闭时进行，格式是 `键=值`，一行一个。

| 键 | 默认 | 说明 |
| --- | --- | --- |
| `cfgver` | 16 | 配置版本；不匹配时旧文件改名 `.v<ver>.bak` 并重建默认 |
| `enable` | 1 | 总开关 |
| `autostart` | 1 | 进游戏自动启动 |
| `key` | 118 | F7：重启（还原所有写入后重新接管） |
| `weapons` | `0x89C5493E08CA4207` | 制导武器列表（逗号分隔） |
| `prio_targets` / `prio_small` | 空 | 大/小优先的武器列表 |
| `prio_manual` | 0 | 手动优先级总开关 |
| `tp_<16 hex>` | 无 | 全局目标优先级 0–9 |
| `wpc_<16 hex 武器>` | 无 | 1 = 用这把枪自己的表 |
| `wpw_<武器>_<目标>` | 无 | 单枪优先级 0–9 |
| `wprio_sel` | `0x0` | 13–19 页正在编辑的枪（0x + 16 hex） |
| `wpcls` | 1 | 12 页列出的武器分类 1–9 |
| `glob_on` | 1 | 0 = 整个优先级功能不注册（只留 03–11 的瞄准模式） |
| `glob_edit` | 0 | 1 = 优先级页写全局表 |
| `targets_extra` | 空 | 追加可锁定实体哈希，逗号分隔 |
| `targets_debug` | 0 | 1 = 记录没列名的实体（TARGET CENSUS） |
| `debug` | 0 | 1 = 每 120 帧 WATCH 行 |
| `los_debug` | 0 | 1 = 视线检测诊断 |
| `los_desc` | 0 | 视线检测用的描述索引 |
| `scan_ms` | 1.5 | 数据定位阶段每帧扫描毫秒数 |
| `cluster_guide` | 1 | RL-77 子弹药制导 |
| `cluster_life` | 3 | 子弹药寿命 |
| `cluster_delay` | 0.05 | 子弹药绑定延迟 |
| `cluster_seeker` | 1 | 子弹药追踪实体 0–7 |
| `cluster_autofix` | 1 | 把 0（确定不追踪）自动升级为 1 |
| `launcher_seeker` | 0 | 火箭本体追踪实体 0–9 |
| `rocket_life` | 1.5 | 集束起爆延时 |
| `rocket_prox` | 0 | 集束近炸引信 |
| `swarm_count` | 25 | 每发制导弹数；0/1 保留空爆 |
| `swarm_split` | 1 | 每颗制导弹各自找目标 |

## 排查

**一把枪都不锁**：确认 `enable=1`、按过 F7、加载顺序对、没有关掉 `require_assets`；
再看 `cone_deg` / `max_dist` / `los_check` 是否把目标筛掉。

**个别单位锁不上**（v1.9.12 修的就是这类）：开 `debug=1` 打一场，看日志里的

```
WATCH <名字> seen=.. wanted=.. health=.. dead=.. status=.. faction=.. pose=.. usable=..
```

- `dead` 涨：单位被死亡缓存挡住（只认 `status=2`；仍异常说明有新状态值）。
- `status` 涨：活体却报 `status≠0`（宪法值一类的第二条记录）。
- `health` 不涨：白名单/血量门没过。
- `wanted` 有但 `usable` 不涨：姿态骨骼读不到。

`targets_debug=1` 会为没列名的实体打 `TARGET CENSUS res= hp= max= status= mask= pose_node= flags= unit= listed= in_list=`，拿 `res` 去 `targets_extra` 里硬加。

**v1.9.12 的无票者案例**：无票者身上有一条衰减「宪法值」记录，身体活着时它就报
`status=1`；旧规则把任意 `status≠0` 当死亡，把整个 unit 踢出候选 3600 帧并反复
复发。现在只认 `status=2`，且部件行不会牵连身体。

**弹丸是紫色问号**：`require_assets=0`，或内置装载器不认识当前游戏 build、且没有可用的 HD2Runtime。

**圆环大小不对**：`scope_fix=0` 时任何倍率下圆环屏幕大小一致；打开后按
`scope_scale` 缩放。

## 构建与校验

```powershell
python build.py              # 生成 Addon 与 zip
python build.py --check-against "../BingusSharedLoader-source-v19"
```

打包结果：`Addon/9ba626afa44a3aa3.patch_0`、`Guided-Rounds-v1.9.14.zip`。
`tools/` 里是只读检查脚本（语法、全局变量、局部变量、包结构、持久化），
`tools/README.md` 有各自路径要求。

## 版本历史

| 版本 | 内容 |
| --- | --- |
| v1.9.14 | 修好组队时队友看到粉色问号：内置装载器等游戏启动后再证明并请求，启动期失败不再永久禁用；装了 HD2Runtime 就优先交给它，拒收时自动回退内置装载器 |
| v1.9.12 | 无票者锁不上：死亡缓存只认 `status=2`；全零骨骼视为读不到；WATCH 增加 `dead=`/`status=` |
| v1.9.11 | 单枪优先级改用准心指向的武器；`CUSTOM` 也指向该枪并关 `glob_edit`；换枪后瞄准模式即时；`0 = 未设置` |
| v1.9.10 | 优先级编辑目标跨菜单保持，12 页三态 |
| v1.9.9 | 优先级页滑条显示单枪表的值 |
| v1.9.8 | 死亡缓存、光能族补全、调试开关 |
| v1.9.5 | 分类名加数字前缀，页面固定排序 |
| v1.9.2 | 单枪优先级开始 |
| v1.9.0 | 武器按类型分页、优先级按阵营分页、移除认知干扰器本体、中英双语 |
| v1.8.6 | 手动目标优先级、TARGET CENSUS、光能族单位补全 |
| v1.8.5 | 运输舰默认不锁定、结算崩溃加固 |
| v1.8.3 / v1.8.4 | 开镜与腰射锁定范围一致、倍镜跟随 |
| v1.8.1 / v1.8.2 | 健壮性、目标方框残留修复 |

## 许可

见 [LICENSE](../LICENSE)。仅用于单人 / 私人联机；请遵守游戏与社区规则。
