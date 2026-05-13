# Docflow 设计系统

面向 AI 编码助手与前端开发者的视觉规范文档集，技术栈为 **Vue 3 + Element Plus 2.x + Less**，与仓库内 `base/assets/css`、`src/assets/css`、`src/element-rewrite.less` 保持一致。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`DESIGN.md`](./DESIGN.md) | **设计规范主文档**（供 AI agent 与 UI 开发优先阅读）。覆盖氛围、色板、字体、图标、组件覆盖、布局、阴影、Do's & Don'ts、响应式、提示词指南。 |
| [`TOKENS.md`](./TOKENS.md) | **设计 Token 速查表**。与 `base/assets/css/mixin.less`、`src/assets/css/variable.less`、`base/assets/css/reset.less` 等对应关系。 |
| [`preview.html`](./preview.html) | **亮色主题可视化速览**。纯 HTML + 内联 CSS，本地双击打开即可，无需构建。 |
| [`preview-dark.html`](./preview-dark.html) | **暗色主题可视化速览**（与主应用暗色菜单等场景参考一致，非 Element Plus 官方暗色主题完整映射）。 |

## 快速上手

### 给 AI Agent

```
请先阅读 frontend/design/DESIGN.md，并按其中规范编写或修改本仓库前端 UI。
```

需要精确色值或变量名时：

```
颜色与间距以 frontend/design/TOKENS.md 为准；实现时优先使用 Less 变量或 Element Plus CSS 变量，避免硬编码。
```

### 预览设计

在浏览器中直接打开：

```
frontend/design/preview.html
frontend/design/preview-dark.html
```

## 核心 Token 速查

| 用途 | 典型值 | 来源 |
|------|--------|------|
| 主色 · Element 主色 | `#3865f4` | `mixin.less` → `@blue` → `reset.less` 中 `--el-color-primary` |
| 品牌渐变（横幅等） | 见 `TOKENS.md` 渐变节 | `src/assets/css/variable.less` 中 `@gradientBlueImage`（需在样式中显式 `@import`） |
| 成功 / 警告 | `#36B42A` / `#FF9A05` | `variable.less`（语义色与 Jinmo 对齐用法） |
| 表头 / 斑马纹灰底 | `#f5f7fa` | `mixin.less` → `@backgroundColor` |
| 顶栏高度 | `48px` | `mixin.less` → `@navbarHeight` |
| 侧栏宽度 | `210px`（收起 `60px`） | `mixin.less`；`body` 上另有 `--sidebar-width: 200px` 供部分组件使用 |

## 维护约定

- **主色与全局 Less 令牌**：以 `base/assets/css/mixin.less` 及 Vite `additionalData` 注入为准（全量 Less 文件默认已含 mixin）。
- **`src/assets/css/variable.less`**：存放 `@gradientBlueImage`、扩展 `@text` 等；**不会**自动注入每个文件，使用渐变或其中变量时请在对应 `<style lang="less">` 内 `@import '@/assets/css/variable.less'`。
- 修改上述源文件中的颜色或间距后，**同步更新** `TOKENS.md` 与 `DESIGN.md` 中的对应说明。
- 本目录文档为派生说明，**不反向修改**业务样式源文件以外的构建逻辑。
