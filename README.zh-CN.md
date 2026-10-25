# 制导弹药 / Guided Rounds

[English](README.md) | **简体中文**

> 完整说明书：[中文](docs/README.md) · [English](docs/README.en.md)

把《绝地潜兵 2》里 **P-92 法令**的制导行为移植到武器清单里的每一把枪：弹丸出膛后
在瞄准锥里找到目标并追上去，**伤害、初速和弹道仍然使用武器自己的数值**。附带索敌
范围圆环、锁定标记、目标方框，以及一整套游戏内 **MODS** 菜单，全部可实时调整。

- 作者：**cancan2333 & SoS2430**
- 需要：**Bingus Shared Loader v15+**、**Vanilla Plus Megapack**（游戏的 MODS
  菜单由它提供）。**HD2Runtime 可选**：本 mod 在每台装了它的机器上自己加载
  弹丸资源包；装了的 runtime 只额外用来把包同步给大厅。
- 源码：`docs/guided_rounds.lua` · 构建：`build.py`

---

## v1.9.15 更新

**队友也装了本 mod 时，不会再看到粉色问号。** v1.9.14 仍是「装了 runtime 就
优先交给它」，只有它拒收才回退内置；于是全队都装了 mod 的对局，也可能因为
runtime 自己的 build 校验失败而拿不到包。现在内置装载器在每台机器上都会运行，
runtime 只额外用来把包同步给大厅。

- 「加载弹丸材质」（默认开）同时控制这两条路径。
- 不认识的游戏 build 只写一行日志并安静关闭，不影响其他功能。

## v1.9.14 更新

**修好：组队时队友会看到你的弹丸变成粉色问号。** v1.9.13 的内置装载器在游戏还在
启动时就去探测资源包系统，一次失败就被记成永久失败，整局都不会再请求资源包。
现在它会等游戏起来、确认 build，再请求；启动期的瞬时失败会重试。

- 装了 HD2Runtime 且它接受请求时优先交给它——它的 SYNCED ASSETS 才是让没装包的
  队友也看到弹丸的关键；拒收时自动回退内置装载器。
- 完全不装 runtime 时，「加载弹丸材质」照样工作。
- 不认识的游戏 build 仍然只写一行日志、安静关闭，不乱写内存。

## v1.9.12 更新

**个别光能族单位（多数是无票者）锁不上**。对局日志给出了原因：无票者身上有一条
记录它在衰减的「宪法值」的健康记录，这条记录在身体还活着时就报 `status=1`。旧的
死亡缓存把任何非 0 的 status 都当作死亡，于是把整个单位从候选列表里踢掉 60 秒，
并且反复复发。

- 死亡缓存现在只认 **`status=2`**（真正的死亡记录），也不会因为部件行而牵连身体。
- 骨骼读出来恰好是 `(0,0,0)` 时视为读不到，换了骨架的单位不会再把目标钉在世界原点。
- `debug=1` 的 WATCH 行新增 `dead=` 和 `status=`，下次复发一眼就能看出是哪道门。

v1.9.11（单枪优先级）与 v1.9.0（分类页）见[版本历史](docs/README.md#版本历史)。

## 安装

1. 先装 mod 加载器：[HD2 Arsenal](https://www.nexusmods.com/helldivers2/mods/4664)。
2. 在 HD2 Arsenal 里导入 `Guided-Rounds-v1.9.14.zip`，并确认下面几个也装好：
   - [Bingus Shared Loader](https://ayakamods.com/mods/bingus-shared-loader.3861/)
   - [hd2runtime](https://ayakamods.com/mods/hd2runtime.4260/) —— 可选：装了优先交给它
     （它也会把包同步给队友），否则由本 mod 自己加载
   - [Vanilla Plus Megapack](https://www.nexusmods.com/helldivers2/mods/16294) —— 必需，游戏内 MODS 菜单就是它提供的
3. 加载顺序，自上而下（换成别的顺序会不生效）：

   ```
   Guided Rounds
   Vanilla Plus Megapack
   Bingus Shared Loader
   hd2runtime
   ```
4. 进游戏。设置菜单在 **Esc → MODS**，第一页 `01 · GUIDED ROUNDS`。

资源包由 HD2Runtime 或内置装载器请求；只有两者都加载不了（没装 runtime 且不认识当前
游戏 build）时，弹丸才会显示成紫色缺材质图标。

## 菜单一览

| 页面 | 内容 |
| --- | --- |
| `01 · GUIDED ROUNDS` | 总开关、锁定角度、锁定距离、刷新间隔、弹道 |
| `02 · GUIDED EXPLOSIVE FUSE` | 爆炸类弹丸的引信 / 空爆计时 |
| `03–11 · GUIDED <武器类型>` | 每把枪的锁定开关与瞄准模式，9 个分类，每页 32 行 |
| `12 · GUIDED WEAPON PRIORITY` | 选择由哪把枪来编辑优先级页 |
| `13 · GUIDED TARGET PRIORITY` | 手动优先级总开关 |
| `14+ · GUIDED TERMINIDS / AUTOMATONS / ILLUMINATE / OTHER` | 每个敌人一个 0–9 滑条 |

## 三层目标优先级

1. **每把枪的粗粒度**（03–11 页）：关闭 / 准心优先 / 最大血量大优先 / 最大血量小优先。
2. **全局表**（13–19 页，`tp_<目标>=0-9`）：1 最先锁，9 最后。
3. **单枪表**（12 页 + 13–19 页，`wpw_<武器>_<目标>=0-9`）：`wpc_<武器>=1` 时启用；
   该枪没设过的目标回退到全局表。**两层里 0 都表示「未设置」。**

## 配置

`%LOCALAPPDATA%\Hd2ApwGuidance\apw_guidance.cfg`（菜单会自动写，关游戏后也可手改）：

| 键 | 含义 |
| --- | --- |
| `enable=0/1` | 总开关，与菜单开关、F7 同一个 |
| `weapons=0x…,…` | 参与制导的武器（菜单写入） |
| `prio_targets=` / `prio_small=` | 最大血量大优先 / 小优先的武器 |
| `prio_manual=0/1` | 手动优先级总开关 |
| `tp_<16位十六进制>=0-9` | 全局目标优先级 |
| `wpc_<16位武器>=1` | 启用这把枪自己的表 |
| `wpw_<武器>_<目标>=0-9` | 单枪优先级 |
| `glob_on=0` | 仅 cfg：取消注册整个优先级功能 |
| `glob_edit=1` | 优先级页写全局表（页面名会显示 GLOBAL） |
| `targets_extra=0x…,…` | 追加可锁定实体的哈希 |
| `debug=1` | 每 120 帧打 WATCH 行与额外诊断 |

完整参数见[说明书](docs/README.md)。

## 构建

```powershell
python build.py
```

只依赖 Python 3，不需要游戏或 SDK。输出
`Addon/9ba626afa44a3aa3.patch_0` 与 `Guided-Rounds-v1.9.14.zip`。
`--check-against` 可对照 BingusSharedLoader 的参考打包器。

## 版本

- **v1.9.15** —— 内置装载器每台机器都运行；HD2Runtime 仅用来同步大厅
- **v1.9.14** —— 修好 v1.9.13 组队时队友看到的粉色问号（内置装载器等游戏启动后再请求）；HD2Runtime 优先、内置回退
- **v1.9.12** —— 无票者锁不上：死亡缓存只认 `status=2`、全零骨骼视为读不到、WATCH 增加计数
- **v1.9.11** —— 单枪优先级按手上的枪取表；选「自定义」也会把优先级页指向该枪；换枪后瞄准模式即时切换；0 = 未设置
- **v1.9.0** —— 武器按类型分页、优先级按阵营分页、移除认知干扰器本体、中英双语单位名
- **v1.8.6** —— 手动目标优先级、TARGET CENSUS、补全光能族单位
- **v1.8.5** —— 运输舰默认不锁定、结算崩溃加固
- **v1.8.3 / v1.8.4** —— 开镜与腰射锁定范围一致
- **v1.8.1 / v1.8.2** —— 健壮性与目标方框残留修复

## 许可

见 [`LICENSE`](LICENSE)。仅用于单人 / 私人联机；请遵守游戏与社区规则。
