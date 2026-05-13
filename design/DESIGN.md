# Docflow 平台

全栈文档流程平台前端：空间、字段、模板、数据源、文件类型等业务管理界面。整体为 **企业级 B 端** 风格：白底内容区、浅灰表格与侧栏、**蓝色主色**与可选 **蓝紫渐变** 品牌强调；信息密度偏 **中高**（列表 + 表单为主）。

---

## 1. 视觉主题与氛围

**设计理念**：Docflow 面向私有化部署的文档与模板治理场景，界面需传达 **清晰、可信赖、易扫描**。留白用于分组与层级，避免大面积装饰渐变干扰阅读。

**气质**：专业、克制；主操作通过主色蓝与 Element 主按钮表达，不必每个页面堆叠多种渐变。

**核心审美**：

- 浅灰页面底（`whitesmoke`）+ 白卡片 / 白顶栏
- 主色蓝（`#3865f4`）用于链接、主按钮、菜单激活态
- 表格表头与斑马纹使用浅灰（`#f5f7fa`），与 `element-rewrite` 一致
- 阴影 **少而实用**（顶栏轻阴影、弹层阴影）

**密度**：中高。与 `src/element-rewrite.less` 中表格 **12px** 字号设定一致；长列表注意行高与列宽，避免挤压。

---

## 2. 色板与角色

| 角色 | 取值 / 变量 | 用途 |
|------|-------------|------|
| 主色蓝 | `#3865f4`（`mixin.less` `@blue` → `--el-color-primary`） | 主按钮、链接、侧栏浅色激活文字 |
| 主色浅底 | `#eef2ff`（`@hoverBackgroundColorPlain`） | Primary light 背景、选中弱背景 |
| 主色悬停边 | `#ccd8fe`（`@hoverBorderColor`） | Primary light 边框类衍生 |
| 表头 / 斑马行底 | `#f5f7fa`（`@backgroundColor`） | `el-table` 表头与偶数行 |
| 正文深灰 | `#303133`（`@text-color-primary`） | 标题、菜单主文字 |
| 次要说明 | `#909399`（`@descText`） | 表头文字色（项目内覆盖）、说明 |
| 警告 | `#ff9a05`（`@orange`） | `--el-color-warning` |
| 品牌渐变 | `variable.less` 中 `@gradientBlueImage` | **横幅、运营位**；中间色约 `#337CFF` |

**主色与横幅**：**Element 层** 使用 mixin 的 `#3865f4`；**横幅渐变** 使用 `variable.less` 中的 `@gradientBlueImage`（需在 Less 中显式 import，见 `TOKENS.md`）。

---

## 3. 排版规则

**基准**：`reset.less` 将 `html, body` 设为 **12px**，Element 表单标签等同步为 12px；**顶栏**组件使用 **14px**。新页面应在同一视图内 **统一层级**（不要混用两种基准导致表单与表格视觉跳跃）。

**建议层级**（在 12px 基准上按比例放大局部标题即可）：

| 层级 | 建议 | 用途 |
|------|------|------|
| 页面标题 | 16–18px，字重 600 | `ElPageHeader` / 自定义标题区 |
| 区块标题 | 14–16px，字重 500–600 | 卡片标题 |
| 正文 / 表格 | 12px（已全局倾向） | 数据表、表单 |
| 辅助说明 | 12px，色 `#909399` | 提示、表头 |

**链接**：`reset.less` 默认链接色为 `@turquoise`（`#00d1b2`），与主色蓝不同；**业务内链到文档/模板详情** 若需与主品牌一致，使用 `var(--el-color-primary)` 或 Element 的 `el-link type="primary"`。

---

## 4. 图标系统

1. **菜单与存量页面**：广泛使用 **iconfont**（`kdxfont` + `kdx-*`），入口见 `src/main.ts` 引入的 `./assets/fonts/iconfont/iconfont.css`；侧栏 `sidebar` 使用 `kdxfont` 类名。
2. **Element Plus**：`@element-plus/icons-vue` 与 `<el-icon>` 用于按钮、输入框图标等。
3. **Iconify**：依赖中存在 `@iconify-json/ep`，按需用于与 EP 图标集一致的新组件。

**规范**：

- 同一密集区域避免 **iconfont 与 EP 线性图标混用且无风格统一**。
- 装饰性图标加 `aria-hidden="true"`；仅图标按钮需父级或按钮 `aria-label`。

---

## 5. 组件样式（与仓库覆盖对齐）

### 表格（`el-table`）

以 `src/element-rewrite.less` 为准：

- 表头背景：`@backgroundColor`（`#f5f7fa`）
- 表头单元格文字：`#909399`，字重 500
- 表格字号：**12px**
- 偶数行背景：`@backgroundColor`
- 链接型操作：`el-link`，注意 `is-disabled` 颜色

### 分页

- `el-pagination`：`margin-top: 16px`（项目内已设）

### 对话框 / 抽屉

- `el-dialog` 标题色：`#151B1E`（覆盖）
- `el-drawer`：内边距与标题字号见 `element-rewrite.less`（如标题 14px、字重 500）

### 表单

- `base` 中 `el-form-item--default` 使用 `--font-size: 12px`
- 校验与禁用态遵循 Element Plus，勿另起一套红绿色

---

## 6. 布局原则

**尺寸（mixin）**：

- 顶栏高度：**48px**（`@navbarHeight`）
- 侧栏宽度：**210px** 展开、**60px** 收起（`@sidebarWidth` / `@siderbarCollWidth`）
- `body` 上另有 `--sidebar-width: 200px`，与 mixin 略有差异；**新布局以 mixin 为准**，逐步收敛 CSS 变量

**间距**：推荐 4px 刻度（见 `TOKENS.md`「间距」）。

**三段式**（与 `AGENTS.md` 一致）：顶栏全局导航 + 左侧功能导航 + 右侧主内容；新页面放在统一 Layout 内。

---

## 7. 深度与层级

| 场景 | 建议 |
|------|------|
| 顶栏 | 轻阴影 `0 0 12px rgba(0,0,0,0.12)` |
| 下拉 / 气泡 | 跟随 Element 默认或 `el-popper` 内已调样式 |
| 遮罩 | Element Overlay 默认 |

**Z-Index**：以 Element 层叠为准；业务自定义浮层时不超过 mixin 中 `@maxZindex` 约定范围，避免盖住全局导航 unless 有意为之。

---

## 8. 建议与禁忌

### 建议 ✓

- 主交互与品牌强调使用 **`var(--el-color-primary)`** 或 `@blue`（mixin）
- 大区块品牌渐变仅用于 **横幅 / 少数 CTA**，与 `spaceBanner` 等现有实现一致
- 表格、表单密度跟随 **`element-rewrite.less`** 与 `reset.less`，保持全站一致
- 私有化场景：**禁止硬编码后端 URL**；使用现有 `service.ts` 与 axios 封装

### 禁忌 ✗

- 勿在业务组件中大量硬编码 **与主色冲突的 hex**（应 Less 变量或 CSS 变量）
- 勿把 `gradient.less` 中 **历史红紫渐变** 当作默认主品牌用于新功能模块
- 勿混用多套 UI 组件库
- 勿在表格单元格使用 **小于 12px** 的字号（可读性与无障碍）

---

## 9. 响应式行为

- 顶栏组件设定 **`min-width: 960px`**，极小屏需横向滚动或单独适配（按产品要求）
- 表格列过多时：**隐藏次要列** 或 **固定列** + 横向滚动
- 断点参考见 `TOKENS.md`

---

## 10. 智能体提示词指南

### 快速色值参考

```
主色（Element）: #3865f4
表头/斑马灰: #f5f7fa
正文标题: #303133
次要/表头字: #909399
品牌渐变: 见 variable.less @gradientBlueImage（需 @import '@/assets/css/variable.less'）
顶栏高: 48px | 侧栏: 210px / 收起 60px
表格字号: 12px
```

### 可直接使用的提示词

**列表页：**

> 按 `frontend/design/DESIGN.md` 使用 Vue 3 + Element Plus。筛选区 + `el-table`，表头背景 `#f5f7fa`，表头文字 `#909399`，表格 12px，分页距表格 16px；主按钮用 `type="primary"`。

**表单抽屉：**

> 使用 `el-drawer` + `el-form`，标题 14px 字重 500，内边距参考 `src/element-rewrite.less`；提交用主色按钮，校验错误使用 Element 默认危险色。

**品牌横幅：**

> 背景使用 `@import '@/assets/css/variable.less'` 后的 `@gradientBlueImage`，文字对比度需满足 WCAG；右侧可配插画或 SVG，参考 `src/components/spaceBanner`。
