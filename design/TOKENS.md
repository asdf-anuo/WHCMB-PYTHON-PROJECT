# Docflow 设计令牌

与仓库内样式源文件对应。Vite 为所有 Less 预置了 `base/assets/css/mixin.less`（见 `base/vite/public.ts` 中 `additionalData`），故多数组件可直接使用下文 **mixin** 列变量。

> **注意**：`src/assets/css/variable.less` 中的 `@blue`（`#337CFF`）与 mixin 中 `@blue`（`#3865f4`）不同；**Element Plus 主色**走的是 `reset.less` 里的 `@blue`，在默认构建顺序下为 **mixin 中的 `#3865f4`**。横幅渐变中间色与 `#337CFF` 一致，见渐变节。

---

## 颜色（主路径：mixin + reset）

| 令牌说明 | Less / CSS | 十六进制或取值 | 用途 |
|----------|-------------|----------------|------|
| 主色蓝 | `@blue`（mixin） | `#3865f4` | `--el-color-primary`、侧栏浅色激活文字、链接强调 |
| 主色蓝（扩展文件） | `@blue`（`variable.less`） | `#337CFF` | 仅在被 `variable.less` 引入的作用域内；与渐变中点一致 |
| 成功绿 | Element 默认（未在 `reset.less` 覆盖） | 以 Element Plus 主题为准 | 业务上可与 `#36B42A`（`variable.less` `@green`）对齐文案/插图 |
| 警告橙 | `@orange`（mixin） | `#ff9a05` | `--el-color-warning` |
| 危险红 | Element 默认 + mixin 中 `@ksRed` 等 | 见 mixin | 破坏性操作以 `el-button type="danger"` / `--el-color-danger` 为准 |
| 正文主色 | `@text-color-primary` | `#303133` | 标题、侧栏浅色模式主文字 |
| 正文（variable） | `@text`（variable.less） | `#3c4449` | 引入 variable 后的正文参考色 |
| 描述 / 次要 | `@descText` | `#909399` | 表格头单元格（`element-rewrite`）、说明 |
| 表头 / 表斑马底 | `@backgroundColor` / `@tableHeader` | `#f5f7fa` | `el-table` 表头与偶数行 |
| 表格边框 | `@tableBorder` | `#e4e8ef` | 表格线框 |
| 主内容背景 | `@mainContentBackgroundColor` | `#ffffff` | 内容区卡片底 |
| 页面灰底 | `reset.less` `@body-background-color` | `whitesmoke` | `html, body` 默认背景 |
| 主按钮底（侧栏激活块等） | `@mainBtnBackgroundColor` | `@ksBlue` → `#3865f4` | 与主色一致 |

**Element Plus 覆盖**（`base/assets/css/reset.less` 中 `body`）：

| CSS 变量 | 来源 |
|----------|------|
| `--el-color-primary` | `@blue`（mixin） |
| `--el-color-primary-light-3` | `@hoverBackgroundColor` → `rgb(119, 151, 253)` |
| `--el-color-primary-light-7` | `@hoverBorderColor` → `#ccd8fe` |
| `--el-color-primary-light-9` | `@hoverBackgroundColorPlain` → `#eef2ff` |
| `--el-color-warning` | `@orange` |
| `--sidebar-width` | `200px`（与 `@sidebarWidth: 210px` 并存，新代码布局请以设计文档「布局」节为准） |
| `--el-font-size-base` 等 | 当前为 **12px** 量级（与 `variable.less` 中 `@baseFontSize: 14px` 并存，表格等在 `src/element-rewrite.less` 中进一步指定） |

---

## 渐变

| 令牌名 | Less 变量 | 取值 | 用途 |
|--------|-------------|------|------|
| 品牌渐变（标准） | `@gradientBlueImage`（`src/assets/css/variable.less`） | `linear-gradient(108.75deg, rgba(87, 182, 255, 0.8) 0%, rgba(51, 124, 255, 0.8) 45.74%, rgba(85, 70, 255, 0.8) 98.5%)` | 横幅、主视觉 CTA 背景（需 `@import '@/assets/css/variable.less'`） |
| 悬停渐变边框 | `@hoverGradientBorder`（同上文件） | `linear-gradient(45deg, rgba(87, 182, 255, 0.8) 0%, rgba(51, 124, 255, 0.8) 45.74%, rgba(85, 70, 255, 0.8) 98.5%)` | 强调边框、装饰 |
| 历史 / 活动渐变工具 | `.liner180Deg`、`.side-bar-liner()` 等 | 见 `base/assets/css/common/gradient.less` | **勿与新页面主品牌混用**；仅旧模块或特定运营样式参考 |

---

## 排版

| 层级 | 典型字号 | 说明 |
|------|----------|------|
| 顶栏 | 14px | `navBarLight` 等 |
| Element 默认 | 12px | `reset.less` 中 `--el-font-size-base` |
| 表格 | 12px | `src/element-rewrite.less` 强制 `el-table` |
| 扩展基准 | 14px | `variable.less`：`@baseFontSize`，`:root { --base-font-size }`（按需使用） |

**字体栈**：`reset.less` 为 `Arial, Helvetica, sans-serif`；中文环境浏览器会回退系统字体。需要与 Jinmo 一致可读性时，可在业务局部使用：`-apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif`。

---

## 间距（推荐刻度，与 Jinmo 对齐便于协作）

| 令牌 | 取值 | 用途 |
|------|------|------|
| xs | 4px | 图标间距 |
| sm | 8px | 紧凑间距 |
| md | 12px | 表单、消息框内边距 |
| base | 16px | 卡片内边距、分页 `margin-top` |
| lg | 20px | 区块水平内边距 |
| xl | 24px | 抽屉 `padding` 等 |
| 2xl | 32px | 大区块间距 |

---

## 圆角

| 场景 | 取值 |
|------|------|
| 输入、小弹层 | 4px（如 `el-popper.is-password`） |
| mixin 常量 | `@borderRadius10`：`10px`；`@borderRadius20`：`20px` |

---

## 阴影

| 用途 | 取值 |
|------|------|
| 顶栏 | `0px 0px 12px rgba(0, 0, 0, 0.12)`（`navBarLight`） |
| 密码提示气泡 | `0px 12px 32px 4px rgba(0, 0, 0, 0.12)` |

---

## Z-Index

| 说明 | 取值 |
|------|------|
| mixin 全局上限参考 | `@maxZindex: 1000` |
| 顶栏 | `@maxZindex + 2` |

---

## 布局尺寸（mixin）

| 变量 | 取值 |
|------|------|
| `@navbarHeight` | 48px |
| `@sidebarWidth` | 210px |
| `@siderbarCollWidth` | 60px |

---

## 断点（建议与 Element 习惯一致）

| 名称 | 最小宽度 | 说明 |
|------|----------|------|
| sm | 768px | 平板 |
| md | 992px | 小桌面 |
| lg | 1200px | **主要目标** |
| xl | 1920px | 宽屏 |

`navBarLight` 使用 `min-width: 960px` 作为整体最小宽度参考。
